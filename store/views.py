import stripe

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.views.generic import ListView
from django.db.models import Q, Prefetch
from django.contrib import messages
from django.conf import settings
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.forms import modelformset_factory
from django.views.decorators.csrf import csrf_exempt
from .forms import ProductForm
from .models import Product, ProductSize, CartItem, Order, OrderItem, NewsletterSubscriber
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

stripe.api_key = settings.STRIPE_SECRET_KEY


class ProductListView(ListView):
    model = Product
    template_name = 'store/shop.html'
    context_object_name = 'products'
    paginate_by = 20

    def get_queryset(self):
        queryset = Product.objects.all()
        query = self.request.GET.get('q')
        category = self.request.GET.get('category')

        if query:
            queryset = queryset.filter(Q(name__icontains=query) | Q(description__icontains=query))

        if category:
            queryset = queryset.filter(category__iexact=category)

        return queryset.order_by('name')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Product.objects.values_list('category', flat=True).distinct()
        return context


def home_view(request):
    return render(request, 'store/home.html')


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == "POST":
        size_id = request.POST.get('size_id')
        return redirect('add_to_cart', product_id=product.id, size_id=size_id)
    return render(request, 'store/product_detail.html', {'product': product})


def product_list(request):
    products = Product.objects.all()
    return render(request, 'store/product_list.html', {'products': products})


def shop_view(request):
    products = Product.objects.all()
    return render(request, 'store/shop.html', {'products': products})


@login_required
def profile_view(request):
    orders = Order.objects.filter(user=request.user, is_paid=True).order_by('-created_at')
    return render(request, 'store/profile.html', {'orders': orders})


@login_required
def view_cart(request):
    cart_items = CartItem.objects.filter(user=request.user)
    total = sum(item.product_size.product.price * item.quantity for item in cart_items)
    return render(request, 'store/cart.html', {'cart_items': cart_items, 'total': total})


@login_required
def add_to_cart(request, product_id, size_id):
    product = get_object_or_404(Product, pk=product_id)
    product_size = get_object_or_404(ProductSize, pk=size_id, product=product)
    cart_item, created = CartItem.objects.get_or_create(user=request.user, product_size=product_size)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    messages.success(request, 'Item added to cart!')
    return redirect('view_cart')


@login_required
def remove_from_cart(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, user=request.user)
    item.delete()
    messages.success(request, 'Item removed from cart.')
    return redirect('view_cart')


@login_required
def update_cart_quantity(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, user=request.user)

    if request.method == 'POST':
        new_quantity = int(request.POST.get('quantity', 1))

        if new_quantity > 0:
            item.quantity = new_quantity
            item.save()
            messages.success(request, 'Cart updated.')
        else:
            item.delete()
            messages.success(request, 'Item removed from cart.')

    return redirect('view_cart')


@login_required
def checkout(request):
    cart_items = CartItem.objects.filter(user=request.user)
    if not cart_items.exists():
        messages.info(request, "Your cart is empty.")
        return redirect('view_cart')
    total = sum(item.product_size.product.price * item.quantity for item in cart_items)
    return render(request, 'store/checkout.html', {
        'cart_items': cart_items,
        'total': total,
        'stripe_public_key': settings.STRIPE_PUBLIC_KEY
    })


@login_required
def create_checkout_session(request):
    cart_items = CartItem.objects.filter(user=request.user)
    if not cart_items.exists():
        messages.info(request, "Your cart is empty.")
        return redirect('view_cart')

    # Create Order
    order = Order.objects.create(user=request.user)
    line_items = []

    for item in cart_items:
        # Save each item to the order
        OrderItem.objects.create(
            order=order,
            product_size=item.product_size,
            quantity=item.quantity
        )

        line_items.append({
            'price_data': {
                'currency': 'eur',
                'unit_amount': int(item.product_size.product.price * 100),
                'product_data': {
                    'name': f"{item.product_size.product.name} (Size: {item.product_size.size})",
                },
            },
            'quantity': item.quantity,
        })

    # Create Stripe checkout session
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        customer_email=request.user.email,
        line_items=line_items,
        mode='payment',
        success_url=request.build_absolute_uri(reverse('order_confirmation')),
        cancel_url=request.build_absolute_uri(reverse('view_cart')),
        metadata={'order_id': order.id},
    )

    order.stripe_checkout_id = session.id
    order.save()

    return HttpResponseRedirect(session.url)



@login_required
def order_confirmation(request):
    order = Order.objects.filter(user=request.user, is_paid=True).order_by('-created_at').first()

    if not order:
        messages.error(request, "No recent order found.")
        return redirect('product_list')

    total = sum(
        item.product_size.product.price * item.quantity for item in order.items.all()
    )

    return render(request, 'store/order_confirmation.html', {
        'order': order,
        'order_total': total
    })


@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    order_items = order.items.select_related('product_size', 'product_size__product')
    return render(request, 'store/order_detail.html', {
        'order': order,
        'order_items': order_items,
    })


@csrf_exempt
def newsletter_signup_ajax(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        if email:
            subscriber, created = NewsletterSubscriber.objects.get_or_create(email=email)
            if created:
                send_mail(
                    'Thanks for subscribing!',
                    'You are now subscribed to Drift Cult updates.',
                    'noreply@driftcult.art',
                    [email],
                    fail_silently=True,
                )
            return JsonResponse({'success': True})
    return JsonResponse({'success': False})


from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

@csrf_exempt
def newsletter_signup_ajax(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        if email:
            subscriber, created = NewsletterSubscriber.objects.get_or_create(email=email)
            if created:
                subject = "🔥 Welcome to Drift Cult – You're In!"
                from_email = 'noreply@driftcult.art'
                to = [email]

                context = {'email': email}
                html_content = render_to_string('emails/newsletter_welcome.html', context)

                msg = EmailMultiAlternatives(subject, '', from_email, to)
                msg.attach_alternative(html_content, "text/html")
                msg.send()

            return JsonResponse({'success': True})
    return JsonResponse({'success': False})


def about_view(request):
    return render(request, 'store/about.html')


def community_view(request):
    return render(request, 'store/community.html')


def robots_txt(request):
    lines = [
        "User-Agent: *",
        "Disallow:",
        "Sitemap: https://driftcult.art/sitemap.xml"
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain")

# Admin Dashboard Views
@staff_member_required
def admin_dashboard(request):
    products = Product.objects.all().prefetch_related('sizes')
    return render(request, 'store/admin_dashboard.html', {'products': products})


@staff_member_required
def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()
            return redirect('add_product_sizes', product_id=product.id)
    else:
        form = ProductForm()
    return render(request, 'store/product_form.html', {
        'form': form,
        'title': 'Add Product'
    })


@staff_member_required
def product_edit(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('admin_dashboard')
    else:
        form = ProductForm(instance=product)
    return render(request, 'store/product_form.html', {
    'form': form,
    'title': 'Edit Product',
    'product': product
})


@staff_member_required
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.delete()
        return redirect('admin_dashboard')
    return render(request, 'store/product_confirm_delete.html', {'product': product})


@staff_member_required
def add_product_sizes(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    SizeFormSet = modelformset_factory(ProductSize, fields=('size', 'stock'), extra=6, can_delete=True)

    if request.method == 'POST':
        formset = SizeFormSet(request.POST, request.FILES, queryset=ProductSize.objects.filter(product=product))
        if formset.is_valid():
            instances = formset.save(commit=False)
            for instance in instances:
                instance.product = product
                instance.save()
            for obj in formset.deleted_objects:
                obj.delete()
            return redirect('admin_dashboard')
    else:
        formset = SizeFormSet(queryset=ProductSize.objects.filter(product=product))

    return render(request, 'store/add_product_sizes.html', {'formset': formset, 'product': product})


@staff_member_required
def admin_order_list(request):
    orders = Order.objects.all().order_by('-created_at')
    return render(request, 'store/admin_order_list.html', {'orders': orders})


@staff_member_required
def admin_order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    order_items = order.items.select_related('product_size', 'product_size__product')

    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in dict(Order.STATUS_CHOICES):
            previous_status = order.status
            order.status = new_status
            order.save()

            if previous_status == 'processing' and new_status == 'shipped':
                subject = f"📦 Your Drift Cult Order #{order.id} Has Shipped"
                from_email = 'noreply@driftcult.art'
                to_email = [order.user.email]
                context = {'user': order.user, 'order': order}
                html_message = render_to_string('emails/order_shipped.html', context)
                msg = EmailMultiAlternatives(subject, '', from_email, to_email)
                msg.attach_alternative(html_message, "text/html")
                msg.send()

            messages.success(request, f"Order status updated to {new_status.title()}")
            return redirect('admin_order_detail', order_id=order.id)

    return render(request, 'store/admin_order_detail.html', {
        'order': order,
        'order_items': order_items,
        'status_choices': Order.STATUS_CHOICES,
    })

    
    
@staff_member_required
def admin_order_delete(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    if request.method == 'POST':
        order.delete()
        messages.success(request, "Order successfully deleted.")
        return redirect('admin_order_list')

    return render(request, 'store/admin_order_confirm_delete.html', {'order': order})


@staff_member_required
def bulk_order_action(request):
    if request.method == 'POST':
        action = request.POST.get('action')
        selected_ids = request.POST.getlist('order_ids')

        if not selected_ids:
            messages.warning(request, "No orders selected.")
            return redirect('admin_order_list')

        orders = Order.objects.filter(id__in=selected_ids)
        affected = 0

        for order in orders:
            if action == 'delete':
                order.delete()
                affected += 1
            elif action in ['processing', 'shipped', 'delivered']:
                if order.status != action:
                    previous_status = order.status
                    order.status = action
                    order.save()
                    affected += 1

                    # Trigger email ONLY if going from processing → shipped
                    if previous_status == 'processing' and action == 'shipped':
                        subject = f"📦 Your Drift Cult Order #{order.id} Has Shipped"
                        from_email = 'noreply@driftcult.art'
                        to_email = [order.user.email]
                        context = {'user': order.user, 'order': order}
                        html_message = render_to_string('emails/order_shipped.html', context)
                        msg = EmailMultiAlternatives(subject, '', from_email, to_email)
                        msg.attach_alternative(html_message, "text/html")
                        msg.send()

        if action == 'delete':
            messages.success(request, f"{affected} orders deleted.")
        else:
            messages.success(request, f"{affected} orders updated to {action}.")

    return redirect('admin_order_list')