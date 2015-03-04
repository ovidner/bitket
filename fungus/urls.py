# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
from django.views.generic import TemplateView

from .views import RegisterShiftsView

urlpatterns = patterns(
    '',
    url(r'^shiftreg/$', RegisterShiftsView.as_view(), name='register_shifts'),
    url(r'^shiftreg/success/$', TemplateView.as_view(template_name='fungus/register_shifts_success.html'),
        name='register_shifts_success'),
)
