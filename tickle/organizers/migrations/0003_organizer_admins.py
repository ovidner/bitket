# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('organizers', '0002_auto_20151201_1423'),
    ]

    operations = [
        migrations.AddField(
            model_name='organizer',
            name='admins',
            field=models.ManyToManyField(related_name='admin_for_organizers', verbose_name='admins', to=settings.AUTH_USER_MODEL),
        ),
    ]
