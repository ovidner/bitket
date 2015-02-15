# -*- coding: utf-8 -*-

from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic import TemplateView

from .views import EntryCreate

urlpatterns = patterns(
    '',
    url(r'^entries/add$', EntryCreate.as_view()),
    url(r'^entries/add/success$', EntryCreate.as_view()),
    url(r'^materials$', EntryCreate.as_view()),
)
