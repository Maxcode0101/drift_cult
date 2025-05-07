from django.shortcuts import render
from django.core.mail import send_mail
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.admin.views.decorators import staff_member_required
from django.conf import settings
from django.template.loader import render_to_string

from store.models import Order, OrderItem, CartItem, User
import stripe
import json

def home(request):
    return render(request, 'home.html')


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
        customer_email = session.get('customer_email') or session.get('customer_details', {}).get('email')

        if not customer_email:
            print("❌ No customer email found.")
            return HttpResponse(status=400)

        user = User.objects.filter(email=customer_email).first()
        if not user:
            print(f"❌ No user found with email {customer_email}")
            return HttpResponse(status=404)

        cart_items = CartItem.objects.filter(user=user)
        if not cart_items.exists():
            print(f"❌ No cart items found for {customer_email}")
            return HttpResponse(status=404)

        order = Order.objects.create(user=user, is_paid=True)

        total = 0
        order_items_data = []
        for item in cart_items:
            order_item = OrderItem.objects.create(
                order=order,
                product_size=item.product_size,
                quantity=item.quantity
            )
            subtotal = item.product_size.product.price * item.quantity
            total += subtotal
            order_items_data.append({
                'product_name': item.product_size.product.name,
                'size': item.product_size.size,
                'quantity': item.quantity,
                'price': f"{item.product_size.product.price:.2f}",
                'subtotal': f"{subtotal:.2f}",
            })

        cart_items.delete()

        print(f"✅ Webhook processed: Order #{order.id} marked as paid.")

        subject = f"Your Drift Cult Order Confirmation (Order #{order.id})"
        html_message = render_to_string('emails/order_confirmation.html', {
            'order': order,
            'user': user,
            'total': f"{total:.2f}",
            'items': order_items_data,
        })

        send_mail(
            subject,
            '',
            settings.DEFAULT_FROM_EMAIL,
            [customer_email],
            html_message=html_message
        )

    return HttpResponse(status=200)


def robots_txt(request):
    lines = [
        "User-Agent: *",
        "Disallow:",
        "Sitemap: https://driftcult.art/sitemap.xml",
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain")
