# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tickle', '0010_auto_20150426_1350'),
    ]

    operations = [
        migrations.CreateModel(
            name='PersonalDiscount',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('discount_amount', models.DecimalField(null=True, verbose_name='amount', max_digits=9, decimal_places=2, blank=True)),
                ('discount_percent', models.DecimalField(decimal_places=2, max_digits=3, blank=True, help_text='Use decimal form, e.g. 0,25.', null=True, verbose_name='percent')),
                ('text', models.CharField(max_length=256, verbose_name='text')),
            ],
            options={
                'verbose_name': 'personal discount',
                'verbose_name_plural': 'personal discounts',
            },
        ),
        migrations.AlterModelOptions(
            name='discount',
            options={'ordering': ('content_type', 'object_id'), 'verbose_name': 'discount', 'verbose_name_plural': 'discounts'},
        ),
        migrations.AlterField(
            model_name='person',
            name='birth_date',
            field=models.DateField(null=True, verbose_name='birth date', blank=True),
        ),
        migrations.AddField(
            model_name='personaldiscount',
            name='people',
            field=models.ManyToManyField(related_name='personal_discounts', verbose_name='people', to='tickle.Person'),
        ),
    ]
