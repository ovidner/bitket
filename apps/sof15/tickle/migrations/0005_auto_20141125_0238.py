# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tickle', '0004_auto_20141125_0158'),
    ]

    operations = [
        migrations.CreateModel(
            name='SpecialNutrition',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=256)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='person',
            name='address_row_2',
            field=models.CharField(default='', max_length=128),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='person',
            name='city',
            field=models.CharField(default='', max_length=64),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='person',
            name='postal_code',
            field=models.CharField(default='', max_length=8),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='person',
            name='special_nutrition',
            field=models.ManyToManyField(to='tickle.SpecialNutrition'),
            preserve_default=True,
        ),
    ]
