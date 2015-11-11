# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import tickle.common.db.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Organizer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('stripe_authorized', models.DateTimeField(verbose_name='Stripe authorization timestamp', null=True, editable=False, blank=True)),
                ('stripe_live_mode', models.BooleanField(default=False, verbose_name='Stripe live mode', editable=False)),
                ('stripe_account_id', models.CharField(verbose_name='Stripe account ID', max_length=64, editable=False, blank=True)),
                ('stripe_refresh_token', models.CharField(verbose_name='Stripe refresh token', max_length=64, editable=False, blank=True)),
                ('stripe_public_key', models.CharField(max_length=64, verbose_name='Stripe public key', blank=True)),
                ('stripe_secret_key', models.CharField(max_length=64, verbose_name='Stripe secret key', blank=True)),
                ('stripe_read_only', models.BooleanField(default=True, verbose_name='Stripe read only access')),
                ('name', tickle.common.db.fields.NameField(unique=True, max_length=64, verbose_name='name')),
                ('slug', tickle.common.db.fields.SlugField(unique=True, max_length=64, verbose_name='slug')),
            ],
        ),
    ]
