# -*- coding: utf-8 -*-

import logging

from django import http
from django.conf import settings
from django.core.urlresolvers import reverse, resolve
from django.db import IntegrityError
from django.db.models import Count
from django.http import JsonResponse
from django.shortcuts import render
from django.template import RequestContext, loader
from django.utils.translation import LANGUAGE_SESSION_KEY, check_for_language

from django.views.generic import TemplateView, RedirectView
from django.views.generic.edit import FormMixin

from datetime import datetime, timedelta, date

from .forms import EnterForm, QueryForm
from .models import Number, Place

logger = logging.getLogger(__name__)


def set_language(request):
    next_view = request.POST.get('next', request.GET.get('next'))
    lang_code = request.POST.get('lang', request.GET.get('lang'))
    response = http.HttpResponseNotAllowed(['POST', 'GET'])

    if request.method == 'POST' or request.method == 'GET':
        if lang_code and check_for_language(lang_code):
            response = http.HttpResponseRedirect('/{}/?redirect_to={}'.format(lang_code, next_view))
            if hasattr(request, 'session'):
                request.session[LANGUAGE_SESSION_KEY] = lang_code
            else:
                response.set_cookie(settings.LANGUAGE_COOKIE_NAME, lang_code,
                                    max_age=settings.LANGUAGE_COOKIE_AGE,
                                    path=settings.LANGUAGE_COOKIE_PATH,
                                    domain=settings.LANGUAGE_COOKIE_DOMAIN)
        else:
            response = http.HttpResponseNotFound()

    return response


class CustomRedirectView(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        # try to get redirect target
        try:
            redir = self.request.GET.get('redirect_to')
            self.url = reverse(redir)

            # remove 'redirect_to' from query string
            query_string = self.request.META.get('QUERY_STRING')
            if query_string:
                query_string = query_string.replace('redirect_to={}'.format(redir), '').replace('^&', '')
                self.request.META.update({'QUERY_STRING': query_string})
        except:
            # if redirect target is not a known view: try path prefixed by lang
            try:
                self.url = reverse(resolve('/en/{}'.format(self.request.get_full_path())))
            except:
                # if we can't get a view from path URL: fall back to default, using 'pattern_name'
                pass

        return super().get_redirect_url(*args, **kwargs)


class QueryView(TemplateView, FormMixin):
    http_method_names = ['get', 'post']
    form_class = QueryForm
    template_name = 'query.html'

    def get_context_data(self, **kwargs):
        if not 'form' in kwargs:
            kwargs['form'] = self.form_class()
        context = super().get_context_data(**kwargs)
        return context

    def post(self, request, *args, **kwargs):
        logger.debug(u'Ajax request: {}'.format(request.is_ajax()))

        response_data = {'result': None, 'timestamps': [], 'invalid': True}

        form = self.get_form()
        if form.is_valid():
            numbers = []
            try:
                numbers = Number.objects.filter(number=form.cleaned_data.get('number'))
            except:
                pass

            response_data.update({
                'result': numbers[0].number if numbers else form.cleaned_data.get('number'),
                'timestamps': [n.timestamp for n in numbers] if numbers else [],
                'invalid': False,
            })

        response = None

        # If this is an ajax request, try to send partial response
        if request.is_ajax():
                response = JsonResponse({'result': loader.render_to_string(
                    '/'.join(['partials', self.template_name.replace('.html', '_result.html')]),
                    context_instance=RequestContext(request), dictionary=response_data)})

        # Classical "full request", render complete template
        if not response:
            response_data.update({'form': form})
            response = render(request, self.template_name, dictionary=response_data)

        return response

    def form_valid(self, form):
        try:
            Number.objects.get(number=form.cleaned_data.get('number'))
        except Number.DoesNotExist:
            pass

        return super().form_valid(form)

    def get_success_url(self):
        return reverse('query', args=self.args, kwargs=self.kwargs)


class DisplayView(TemplateView):
    template_name = 'display.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        oldest_to_be_shown = datetime.combine(date.today() - timedelta(days=settings.APP_SETTINGS['DISPLAY']['MAX_DAYS']), datetime.min.time())

        verified_numbers = Number.objects.filter(timestamp__gte=oldest_to_be_shown, user__isnull=False)\
            .order_by('-timestamp')\
            .values('number')[:settings.APP_SETTINGS['DISPLAY']['SIZE']]
        logger.debug(u'Verified numbers: {}'.format(len(verified_numbers)))

        numbers = Number.objects.filter(timestamp__gte=oldest_to_be_shown)\
            .values('number')\
            .annotate(count=Count('number'))\
            .filter(count__gte=3)\
            .order_by('number')[:settings.APP_SETTINGS['DISPLAY']['SIZE']]
        logger.debug(u'Numbers: {}'.format(len(numbers)))

        result = {}
        for n in numbers:
            result[n['number']] = n['count']
        for n in verified_numbers:
            result[n['number']] = '∞'

        context['numbers'] = []
        for n in sorted(set(result.keys())):
            context['numbers'].append({'number': n, 'count': result[n]})
        context['min_count'] = 3
        context['since'] = oldest_to_be_shown
        return context


