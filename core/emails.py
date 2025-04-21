from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

def send_registration_email(to_email, username):
    subject = "Welcome to Drift Cult 🌊"
    from_email = "Drift Cult <admin@driftcult.art>"
    context = {"username": username}

    html_content = render_to_string("emails/welcome_email.html", context)
    text_content = f"Hey {username}, thanks for signing up at Drift Cult!"

    msg = EmailMultiAlternatives(subject, text_content, from_email, [to_email])
    msg.attach_alternative(html_content, "text/html")
    msg.send()
