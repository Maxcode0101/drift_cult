from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.contrib.admin.views.decorators import staff_member_required
from django.template.loader import render_to_string
from django.contrib import messages
from django.conf import settings
from store.models import Order, OrderItem, CartItem, User
import stripe

@staff_member_required
def test_email(request):
    send_mail(
        subject="🚀 Drift Cult SMTP Email Test",
        message="This is a plain text fallback for the Drift Cult test email.",
        from_email="Drift Cult <admin@driftcult.art>",
        recipient_list=["maximilian.kaening@gmail.com"],
        html_message="""
            <div style="font-family: Arial, sans-serif; padding: 20px;">
                <h2 style="color: #111;">SMTP is LIVE 💥</h2>
                <p>Your Django project is now sending email via <strong>admin@driftcult.art</strong> using Namecheap Pro Mail SMTP.</p>
                <p>This confirms your SMTP setup is working 100%.</p>
                <p style="margin-top: 30px;">– Drift Cult Tech</p>
            </div>
        """,
    )
    return HttpResponse("✅ Test email sent! Check your inbox.")

@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
    endpoint_secret = settings.STRIPE_WEBHOOK_SECRET

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
    except (ValueError, stripe.error.SignatureVerificationError):
        return HttpResponse(status=400)

    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        order_id = session.get('metadata', {}).get('order_id')
        customer_email = session.get('customer_email') or session.get('customer_details', {}).get('email')

        order = Order.objects.filter(id=order_id).first()
        user = User.objects.filter(email=customer_email).first()

        if not order or not user:
            return HttpResponse(status=404)

        order.is_paid = True
        order.save()

        # Send order confirmation email
        order_items = order.items.select_related('product_size__product')
        order_items_data = []

        total = 0
        for item in order_items:
            subtotal = item.product_size.product.price * item.quantity
            total += subtotal
            order_items_data.append({
                'product_name': item.product_size.product.name,
                'size': item.product_size.size,
                'quantity': item.quantity,
                'price': f"{item.product_size.product.price:.2f}",
                'subtotal': f"{subtotal:.2f}",
            })

        html_message = render_to_string('emails/order_confirmation.html', {
            'order': order,
            'user': user,
            'total': f"{total:.2f}",
            'items': order_items_data,
        })

        send_mail(
            subject=f"Your Drift Cult Order Confirmation (Order #{order.id})",
            message="",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[customer_email],
            html_message=html_message
        )

        # Clear the cart
        CartItem.objects.filter(user=user).delete()

    return HttpResponse(status=200)


def robots_txt(request):
    lines = [
        "User-Agent: *",
        "Disallow:",
        "Sitemap: https://driftcult.art/sitemap.xml",
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain")


def custom_404_view(request, exception):
    return render(request, '404.html', status=404)


@require_http_methods(["GET", "POST"])
def contact_view(request):
    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        email = request.POST.get("email", "").strip()
        message = request.POST.get("message", "").strip()

        if not name or not email or not message:
            messages.error(request, "All fields are required.")
            return redirect('contact')

        subject = f"New Contact Form Message from {name}"
        body = f"""
You’ve received a new message via the contact form:

Name: {name}
Email: {email}

Message:
{message}
        """

        try:
            send_mail(
                subject,
                body,
                "Drift Cult <admin@driftcult.art>",
                ["admin@driftcult.art"],
                fail_silently=False,
            )
            messages.success(request, "Thanks for reaching out! We’ll get back to you soon.")
            return redirect('contact')
        except Exception:
            messages.error(request, "Something went wrong while sending your message. Please try again.")
            return redirect('contact')

    return render(request, "core/contact.html")