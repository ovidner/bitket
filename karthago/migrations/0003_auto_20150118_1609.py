# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('karthago', '0002_create_default_data'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='material',
            options={'ordering': ('name',)},
        ),
        migrations.AlterField(
            model_name='entrycustommaterial',
            name='amount',
            field=models.DecimalField(verbose_name='amount', max_digits=9, decimal_places=3),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='entrycustommaterial',
            name='entry',
            field=models.ForeignKey(verbose_name='entry', to='karthago.Entry'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='entrycustommaterial',
            name='material',
            field=models.CharField(max_length=256, verbose_name='material'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='entrycustommaterial',
            name='role',
            field=models.ForeignKey(verbose_name='role', to='karthago.MaterialRole'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='entrycustommaterial',
            name='unit',
            field=models.CharField(max_length=8, verbose_name='unit'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='entrymaterial',
            name='amount',
            field=models.DecimalField(verbose_name='amount', max_digits=9, decimal_places=3),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='entrymaterial',
            name='entry',
            field=models.ForeignKey(verbose_name='entry', to='karthago.Entry'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='entrymaterial',
            name='material',
            field=models.ForeignKey(verbose_name='material', to='karthago.Material'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='entrymaterial',
            name='role',
            field=models.ForeignKey(verbose_name='role', to='karthago.MaterialRole'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='entrytype',
            name='description',
            field=models.CharField(max_length=256, verbose_name='description'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='entrytype',
            name='max_members',
            field=models.PositiveIntegerField(verbose_name='max members'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='entrytype',
            name='name',
            field=models.CharField(max_length=256, verbose_name='name'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='material',
            name='name',
            field=models.CharField(unique=True, max_length=256, verbose_name='name'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='material',
            name='unit',
            field=models.CharField(max_length=16, verbose_name='unit'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='materialrole',
            name='name',
            field=models.CharField(max_length=256, verbose_name='name'),
            preserve_default=True,
        ),
    ]
