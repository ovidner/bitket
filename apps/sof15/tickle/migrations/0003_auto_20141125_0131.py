# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tickle', '0002_auto_20141125_0103'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ownership',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('acquired', models.DateTimeField()),
                ('valid', models.BooleanField(default=True)),
                ('person', models.ForeignKey(to='tickle.Person')),
                ('product', models.ForeignKey(to='tickle.Product')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='ticket',
            name='holder',
        ),
        migrations.RemoveField(
            model_name='ticket',
            name='type',
        ),
        migrations.DeleteModel(
            name='Ticket',
        ),
    ]
