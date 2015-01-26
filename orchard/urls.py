# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView

from .views import ApproveOrchestraMemberView, RegisterOrchestraMemberView

urlpatterns = patterns(
    '',


    url(r'^orchestras/(?P<pk>\d+)/members/$', ApproveOrchestraMemberView.as_view(),
        name='approve_orchestra_members'),
    url(r'^members/add/$', RegisterOrchestraMemberView.as_view(), name='register_orchestra_member'),
    url(r'^members/add/success/$', TemplateView.as_view(template_name='orchard/register_member_success.html'),
        name='register_orchestra_member_success'),
)
