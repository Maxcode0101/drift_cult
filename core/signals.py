from allauth.account.signals import user_signed_up
from django.dispatch import receiver
from core.emails import send_registration_email


@receiver(user_signed_up)
def handle_user_signed_up(request, user, **kwargs):
    send_registration_email(user.email, user.username)
