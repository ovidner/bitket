from __future__ import absolute_import, unicode_literals

from django.views.generic import TemplateView


class ClientView(TemplateView):
    template_name = 'base.html'
