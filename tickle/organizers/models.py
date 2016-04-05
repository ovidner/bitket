from __future__ import absolute_import, unicode_literals

from django.conf import settings
from django.db import models
from django.utils.timezone import now
from django.utils.translation import ugettext_lazy as _

import requests

from tickle.common.behaviors import NameSlugMixin
from tickle.common.db.fields import NameField, SlugField
from tickle.common.models import Model


class OrganizerStripeMixin(models.Model):
    stripe_authorized = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_('Stripe authorization timestamp'))
    stripe_live_mode = models.BooleanField(
        default=False,
        verbose_name=_('Stripe live mode'))
    stripe_account_id = models.CharField(
        max_length=64,
        blank=True,
        verbose_name=_('Stripe account ID'))
    stripe_refresh_token = models.CharField(
        max_length=64,
        blank=True,
        verbose_name=_('Stripe refresh token'))
    stripe_public_key = models.CharField(
        max_length=64,
        blank=True,
        verbose_name=_('Stripe public key'))
    stripe_secret_key = models.CharField(
        max_length=64,
        blank=True,
        verbose_name=_('Stripe secret key'))
    stripe_read_only = models.BooleanField(
        default=True,
        verbose_name=_('Stripe read only access'))

    class Meta:
        abstract = True

        permissions = [
            ['manage_organizer_stripe', _('Can manage Stripe for organizer')]
        ]

    def authorize_stripe(self, code):
        response = requests.post(settings.STRIPE_OAUTH_TOKEN_URL, {
            'client_secret': settings.STRIPE_SECRET_KEY,
            'grant_type': 'authorization_code',
            'code': code})

        # Makes sure we won't miss any error.
        response.raise_for_status()

        response_data = response.json()
        self.stripe_authorized = now()
        self.stripe_live_mode = response_data['livemode']
        self.stripe_account_id = response_data['stripe_user_id']
        self.stripe_refresh_token = response_data['refresh_token']
        self.stripe_public_key = response_data['stripe_publishable_key']
        self.stripe_secret_key = response_data['access_token']
        self.stripe_read_only = response_data['scope'] == 'read_only'
        self.save()


class Organizer(NameSlugMixin, OrganizerStripeMixin, Model):
    name = NameField(
        unique=True)
    slug = SlugField(
        unique=True,
        populate_from='name')

    admins = models.ManyToManyField(
        'people.Person',
        related_name='admin_for_organizers',
        verbose_name=_('admins'))

    class Meta:
        pass
