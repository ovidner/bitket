from django.dispatch import receiver
from django.contrib.auth.signals import user_logged_in


@receiver(user_logged_in)
def create_default_cart(sender, request, user, **kwargs):
    user.create_default_cart()
