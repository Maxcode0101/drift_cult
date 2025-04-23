from django.shortcuts import render
from django.core.mail import send_mail
from django.http import HttpResponse
from django.contrib.admin.views.decorators import staff_member_required

# Stripe + webhook imports
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from store.models import Order
from django.template.loader import render_to_string
from django.contrib.auth.models import User
import stripe

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

    if sig_header is None:
        return HttpResponse("Missing Stripe Signature", status=400)

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError:
        return HttpResponse("Invalid payload", status=400)
    except stripe.error.SignatureVerificationError:
        return HttpResponse("Invalid signature", status=400)

    # Handle successful checkout session
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        customer_email = session.get('customer_email')
        user = User.objects.filter(email=customer_email).first()
        if user:
            order = Order.objects.filter(user=user, is_paid=False).last()
            if order:
                order.is_paid = True
                order.save()

                print("✅ Webhook received and order marked as paid.")

                # Send order confirmation email
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
