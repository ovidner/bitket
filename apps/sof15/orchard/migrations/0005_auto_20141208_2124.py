# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orchard', '0004_orchestraproduct'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='orchestra',
            options={'permissions': (('approve_members', 'Approve members'), ('approve_members_for_invoicing', 'Approve members for invoicing'))},
        ),
        migrations.RemoveField(
            model_name='orchestramember',
            name='orchestras',
        ),
        migrations.AddField(
            model_name='orchestra',
            name='members',
            field=models.ManyToManyField(related_name='orchestras', through='orchard.OrchestraMembership', to='orchard.OrchestraMember'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='orchestramembership',
            name='approved',
            field=models.NullBooleanField(),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='orchestramembership',
            name='approved_for_invoicing',
            field=models.NullBooleanField(),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='orchestramembership',
            name='member',
            field=models.ForeignKey(related_name='memberships', to='orchard.OrchestraMember'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='orchestramembership',
            name='orchestra',
            field=models.ForeignKey(related_name='memberships', to='orchard.Orchestra'),
            preserve_default=True,
        ),
    ]
