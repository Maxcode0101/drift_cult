# store/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView
from django.db.models import Q
from django.contrib import messages
from django.conf import settings
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

import stripe

from .models import Product, ProductSize, CartItem, Order, OrderItem


stripe.api_key = settings.STRIPE_SECRET_KEY


class ProductListView(ListView):
    model = Product
    template_name = 'store/product_list.html'
    context_object_name = 'products'
    paginate_by = 20

    def get_queryset(self):
        queryset = Product.objects.all()
        query = self.request.GET.get('q')
        category = self.request.GET.get('category')

        if query:
            queryset = queryset.filter(
                Q(name__icontains=query) |
                Q(description__icontains=query)
            )

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

    line_items = []
    for item in cart_items:
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

    order = Order.objects.create(user=request.user)

    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        customer_email=request.user.email,
        line_items=line_items,
        mode='payment',
        success_url=request.build_absolute_uri(reverse('order_confirmation')),
        cancel_url=request.build_absolute_uri(reverse('view_cart')),
        metadata={'order_id': order.id},
    )

    request.session['pending_order_id'] = order.id
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
