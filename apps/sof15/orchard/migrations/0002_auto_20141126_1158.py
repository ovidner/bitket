# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orchard', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrchestraMembership',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('member', models.ForeignKey(to='orchard.OrchestraMember')),
                ('orchestra', models.ForeignKey(to='orchard.Orchestra')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='orchestra',
            name='bulk_invoicing',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='orchestramember',
            name='orchestras',
            field=models.ManyToManyField(to='orchard.Orchestra', null=True, through='orchard.OrchestraMembership', blank=True),
            preserve_default=True,
        ),
    ]
