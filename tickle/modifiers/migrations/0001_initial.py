# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-04-21 22:10
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import tickle.common.db.fields
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('conditions', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Modifier',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='ID')),
                ('delta_amount', tickle.common.db.fields.MoneyField(decimal_places=2, help_text='For discount, enter a negative value.', max_digits=12, verbose_name='delta (amount)')),
                ('condition', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_modifiers', to='conditions.Condition', verbose_name='condition')),
            ],
            options={
                'verbose_name': 'modifier',
                'verbose_name_plural': 'modifiers',
            },
        ),
    ]
