# -*- coding: utf-8 -*-

"""lagesonum URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.contrib.auth import views as auth_views
#from django.views.i18n import set_language

import website.views
import django.conf.urls.i18n
import django.views.generic

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^auth/login/$', auth_views.login, name='login', kwargs={'template_name': 'login.html'}),
    url(r'^auth/logout/$', auth_views.logout, name='logout', kwargs={'template_name': 'logged_out.html'}),
    url(r'^$', website.views.CustomRedirectView.as_view(permanent=False, pattern_name='query'), name='home'),
    url(r'^about$', django.views.generic.TemplateView.as_view(template_name='about.html'), name='about'),
    url(r'^imprint$', django.views.generic.TemplateView.as_view(template_name='imprint.html'), name='imprint'),
    url(r'^setlang/$', website.views.set_language, name='set_lang'),
    url(r'^i18n/', include('django.conf.urls.i18n')),
]

urlpatterns += i18n_patterns(
    url(r'^$', website.views.CustomRedirectView.as_view(permanent=False, pattern_name='enter'), name='home'),
    url(r'^query$', website.views.QueryView.as_view(), name='query'),
    url(r'^display$', website.views.DisplayView.as_view(), name='display'),
)
