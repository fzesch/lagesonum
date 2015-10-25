from django.views.generic import View
from django.core.mail import EmailMessage
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from website.models import Subscription, Place


class EmailNotificationView(View):

    def send(self, recipient_address, number):
        subject = _('LaGeSoNum Update')
        message = 'Your number is up! Go to LaGeSo for your appointment {}'.format(number)
        from_email = settings.DEFAULT_EMAIL_FROM

        # TODO Error handling
        sendmail = EmailMessage(subject=subject, body=message, from_email=from_email, to=[recipient_address])
        sendmail.send()
