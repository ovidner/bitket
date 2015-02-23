# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0001_initial'),
        ('tickle', '0009_auto_20150215_2009'),
    ]

    operations = [
        migrations.CreateModel(
            name='LiUID',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('liu_id', models.CharField(max_length=10, verbose_name='LiU ID')),
                ('first_name', models.CharField(max_length=256, verbose_name='first name', blank=True)),
                ('last_name', models.CharField(max_length=256, verbose_name='last name', blank=True)),
                ('pid', models.CharField(max_length=11, verbose_name='national identity number', blank=True)),
                ('barcode_number', models.CharField(max_length=32, verbose_name='magnet/barcode card number', blank=True)),
                ('rfid_number', models.CharField(max_length=32, verbose_name='RFID card number', blank=True)),
                ('blocked', models.NullBooleanField(verbose_name='blocked')),
            ],
            options={
                'verbose_name': 'LiU ID',
                'verbose_name_plural': 'LiU IDs',
            },
            bases=(models.Model,),
        ),
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
            name='StudentUnion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=256, verbose_name='name')),
            ],
            options={
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
                ('student_union', models.ForeignKey(related_name='discounts', verbose_name='student union', to='tickle.StudentUnion')),
            ],
            options={
                'verbose_name': 'student union discount',
                'verbose_name_plural': 'student union discounts',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='liuid',
            name='student_union',
            field=models.ForeignKey(related_name='members', verbose_name='student union', blank=True, to='tickle.StudentUnion', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='person',
            name='liu_id',
            field=models.OneToOneField(null=True, blank=True, to='tickle.LiUID', verbose_name='LiU ID'),
            preserve_default=True,
        ),
    ]
