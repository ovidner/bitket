# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orchard', '0004_remove_orchestramembership_purchase_object'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orchestramember',
            name='accommodation',
        ),
        migrations.RemoveField(
            model_name='orchestramember',
            name='anniversary_dinner',
        ),
        migrations.RemoveField(
            model_name='orchestramember',
            name='food',
        ),
        migrations.AlterField(
            model_name='orchestra',
            name='members',
            field=models.ManyToManyField(related_name='orchestras', through='orchard.OrchestraMembership', to='tickle.Person'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='orchestramembership',
            name='member',
            field=models.ForeignKey(related_name='memberships', to='tickle.Person'),
            preserve_default=True,
        ),
    ]
