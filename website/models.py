# -*- coding: utf-8 -*-

from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.utils.timezone import now

import re


class Place(models.Model):

    description = u'A place numbers are shown at and for'

    name = models.CharField(max_length=20, unique=True, verbose_name=_('place'))
    validation = models.CharField(max_length=256, verbose_name=_('pattern'))

    class Meta:
        verbose_name = _('place')
        verbose_name_plural = _('places')

    def validate(self, value):
        if self.validation:
            return re.match(self.validation, value)
        return None

    def __str__(self):
        return u'{}'.format(self.name)

    def __repr__(self):
        return u'{} ({})'.format(self.name, self.validation)


class Number(models.Model):

    description = u'A number shown at a place and entered into dataset'

    number = models.CharField(max_length=30, verbose_name=_('number'))
    timestamp = models.DateTimeField(default=now)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, related_name='+', on_delete=models.SET_NULL)
    location = models.ForeignKey('Place', on_delete=models.PROTECT)
    fingerprint = models.CharField(max_length=32)

    class Meta:
        verbose_name = _('number')
        verbose_name_plural = _('numbers')
        unique_together = (('number', 'fingerprint'),)

    def __str__(self):
        return '{}@{} (Timestamp: {}; User: {})'.format(self.number, self.location if self.location_id else None,
                                                        self.timestamp, self.user if self.user_id else None)
                                                
class Subscription(models.Model):
    description = u'A number connected with a contact information such as email or phone number'
    
    number = models.CharField(max_length=64)
    email = models.CharField(max_length=70, null=True, default=None)
    phone = models.CharField(max_length=15, null=True, default=None)
    telegram = models.CharField(max_length=50, null=True, default=None)
    email_confirmed = models.DateField(null=True, default=None, blank=True)
    phone_confirmed = models.DateField(null=True, default=None, blank=True)
    cancelled = models.DateField(null=True, default=None, blank=True)
    last_notify = models.DateField(null=True, default=None, blank=True)
