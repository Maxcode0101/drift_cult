from django.shortcuts import render
from django.core.mail import send_mail
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.admin.views.decorators import staff_member_required
from django.conf import settings
from django.template.loader import render_to_string
from store.models import Order, User

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
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except (ValueError, stripe.error.SignatureVerificationError):
        return HttpResponse(status=400)

    # ✅ Handle the checkout.session.completed event
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']

        # 🔍 Try both methods to get the customer's email
        customer_email = session.get('customer_email') or session.get('customer_details', {}).get('email')
        if not customer_email:
            print("❌ Webhook: No customer email found in session.")
            return HttpResponse(status=400)

        user = User.objects.filter(email=customer_email).first()
        if not user:
            print(f"❌ Webhook: No user found with email {customer_email}")
            return HttpResponse(status=404)

        order = Order.objects.filter(user=user, is_paid=False).last()
        if order:
            order.is_paid = True
            order.save()

            print("✅ Webhook received and order marked as paid.")

            # 📧 Send confirmation email
            subject = "Your Drift Cult Order Confirmation"
            html_message = render_to_string('emails/order_confirmation.html', {
                'order': order,
                'user': user
            })
            send_mail(
                subject,
                '',
                settings.DEFAULT_FROM_EMAIL,
                [customer_email],
                html_message=html_message
            )

    return HttpResponse(status=200)
