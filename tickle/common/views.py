from __future__ import absolute_import, unicode_literals

from django.conf import settings
from django.views.generic import TemplateView

from dry_rest_permissions.generics import (DRYPermissions,
                                           DRYGlobalPermissions,
                                           DRYObjectPermissions)
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly


class ClientView(TemplateView):
    template_name = 'base.html'

    def get_context_data(self, **kwargs):
        context = super(ClientView, self).get_context_data(**kwargs)
        context['sentry_release'] = settings.RAVEN_CONFIG['release']
        return context


class ModelViewSet(viewsets.ModelViewSet):
    parent_lookups = {}
    permission_classes = (DRYPermissions,)

    def get_queryset(self):
        queryset = super(ModelViewSet, self).get_queryset()
        select_related_args = []
        filter_kwargs = {}

        for kwarg, orm_lookup in self.parent_lookups.iteritems():
            try:
                filter_kwargs[orm_lookup] = self.kwargs[kwarg]

                # pk fields can't be select_related
                select_related_args.append(orm_lookup.rstrip('__pk'))
            except KeyError:
                continue

        return queryset.filter(**filter_kwargs).select_related(*select_related_args)
