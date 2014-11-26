# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tickle', '0006_auto_20141125_0518'),
    ]

    operations = [
        migrations.CreateModel(
            name='Orchestra',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=256)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='OrchestraMember',
            fields=[
                ('person_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='tickle.Person')),
                ('orchestras', models.ManyToManyField(to='orchard.Orchestra')),
            ],
            options={
            },
            bases=('tickle.person',),
        ),
    ]
