# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView

from .views import ApproveOrchestraMemberView, RegisterOrchestraMemberView, ViewOrchestraInvoiceDataView

urlpatterns = patterns(
    '',

    url(r'^oldies/add/$', RegisterOrchestraMemberView.as_view(template_name='orchard/register_oldie.html'), name='register_oldie'),

    url(r'^orchestras/(?P<pk>\d+)/members/$', ApproveOrchestraMemberView.as_view(),
        name='approve_orchestra_members'),
    url(r'^orchestras/(?P<pk>\d+)/invoice-data/$', ViewOrchestraInvoiceDataView.as_view(),
        name='view_orchestra_invoice_data'),

    url(r'^members/add/$', TemplateView.as_view(template_name='orchard/register_member_closed.html'),
        name='register_orchestra_member'),
    url(r'^members/add/late/f4kp/$', RegisterOrchestraMemberView.as_view(), name='register_orchestra_member_secret'),
    url(r'^members/add/success/$', TemplateView.as_view(template_name='orchard/register_member_success.html'),
        name='register_orchestra_member_success'),
)
