# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
from django.views.generic import TemplateView

from .views import RegisterFunctionaryView

urlpatterns = patterns(
    '',
    # url(r'^functionaries/add/$', RegisterFunctionaryView.as_view(), name='register_functionary'),
    # url(r'^functionaries/add/success/$', TemplateView.as_view(template_name='fungus/register_functionary_success.html'),
    #     name='register_functionary_success'),
)
