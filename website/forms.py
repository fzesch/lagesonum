# -*- coding: utf-8 -*-

import logging

from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from .models import Number, Place, Subscription

logger = logging.getLogger(__name__)


class EnterForm(forms.ModelForm):
    error_css_class = 'error'
    required_css_class = 'required'

    numbers_text = forms.CharField(widget=forms.Textarea(
        attrs={'id': 'numbers_text', 'required': True, 'placeholder': _('inputexample'), 'rows': 10,
               'class': 'form-control', }))
    location = forms.ModelChoiceField(Place.objects.all(), required=True)

    class Meta:
        model = Number
        fields = ['numbers_text', 'location']

    def _post_clean(self):
        super()._post_clean()
        if self.is_valid():
            numbers = []
            loc = self.cleaned_data['location']
            numbers_text = self.cleaned_data['numbers_text'].split()
            errors = []

            for n in numbers_text:
                if loc.validate(n):
                    numbers.append(n)
                else:
                    # TODO i18n
                    errors.append(ValidationError(_('errinvalinput'), code='invalid', params={'number': n}))

            if any(errors):
                logger.error(u'Post validation raises the following error(s): %s', errors)
                # self.cleaned_data.update({'failed': errors})
                self.add_error('numbers_text', errors)

            if any(numbers):
                self.cleaned_data.update({'numbers': numbers})


class QueryForm(forms.ModelForm):
    error_css_class = 'error'
    required_css_class = 'required'

    number = forms.CharField(widget=forms.TextInput(
        attrs={'id': 'numberfield', 'required': True, 'label': _('txtnumber'), 'placeholder': _('queryexample'),
               'class': 'form-control', 'role': 'search'}
    ))

    class Meta:
        model = Number
        fields = ['number']
        """
        widgets = {
            'number': forms.TextInput(
                attrs={'id': 'numberfield', 'required': True,
                       'label': _('txtnumber'), 'placeholder': _('queryexample'),
                       'class': 'form-control',
                       }
            ),
        }
        """


class SubscribeForm(forms.ModelForm):
    error_css_class = 'error'
    required_css_class = 'required'
    
    number = forms.CharField(widget=forms.TextInput(
        attrs={'id': 'numberfield', 'required': True, 'label': _('txtnumber'),
               'class': 'form-control',}
    ))
    
    # TODO make this good
    # TODO make email an HTML5 email field
    email = forms.CharField(required=False)
    phone = forms.CharField(required=False)
    telegram = forms.CharField(required=False)
    
    # validate that at least ONE of the contact fields is fulled
    def _post_clean(self):
        cleaned_data = super(SubscribeForm, self).clean()
        email = cleaned_data.get('email')
        phone = cleaned_data.get('phone')
        telegram = cleaned_data.get('telegram')

        if not email and not phone and not telegram:
            # TODO enable translation
            self.add_error(None, 
                forms.ValidationError('You need to fill out at least one of the contact possibilities: '
                                      'email, phone or telegram!'))
    
    class Meta:
        model = Subscription
        fields = ['number', 'email', 'phone', 'telegram']

    
