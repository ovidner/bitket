# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0001_initial'),
        ('liu', '0001_initial'),
        ('tickle', '0009_auto_20150215_2009'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductDiscount',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('discount_object_id', models.PositiveIntegerField()),
                ('discount_content_type', models.ForeignKey(to='contenttypes.ContentType')),
                ('product', models.ForeignKey(related_name='discounts', to='tickle.Product')),
            ],
            options={
                'verbose_name': 'product discount',
                'verbose_name_plural': 'product discounts',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='StudentUnionDiscount',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=256, verbose_name='name')),
                ('discount_amount', models.DecimalField(null=True, verbose_name='amount', max_digits=9, decimal_places=2, blank=True)),
                ('discount_percent', models.DecimalField(null=True, verbose_name='percent', max_digits=3, decimal_places=2, blank=True)),
                ('student_union', models.ForeignKey(related_name='discounts', verbose_name='student union', to='liu.StudentUnion')),
            ],
            options={
                'verbose_name': 'student union discount',
                'verbose_name_plural': 'student union discounts',
            },
            bases=(models.Model,),
        ),
    ]
