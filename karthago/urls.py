# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView

from .views import EntryCreate

urlpatterns = patterns(
    '',
    # url(r'^entries/add/$', EntryCreate.as_view(), name='create_kartege_entry'),
    url(r'^entries/add/$', TemplateView.as_view(template_name='karthago/entries/create_closed.html'), name='create_kartege_entry'),
    url(r'^entries/add/late/7d3c/$', EntryCreate.as_view(), name='create_kartege_entry_secret'),
    url(r'^entries/add/success/$', TemplateView.as_view(template_name='karthago/entries/create_success.html'), name='create_kartege_entry_success'),
)
