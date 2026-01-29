from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings


@receiver(post_save, sender=User)
def sendWelcomeMail(sender, instance, created, **kwargs):
    if created:
        sub = f"Welcome {instance.first_name} To our Platform"
        bodymess = render_to_string(
            "email/welcomeEmail.html",
            {
                "fname": instance.first_name,
                "lname": instance.last_name,
            },
        )

        from_email = settings.DEFAULT_FROM_EMAIL
        recipient = [instance.email]

        email = EmailMessage(sub, bodymess, from_email, recipient)
        email.content_subtype = "html"
        email.send()
