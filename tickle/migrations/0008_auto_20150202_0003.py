# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tickle', '0007_auto_20150126_1652'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='holding',
            options={'verbose_name': 'holding', 'verbose_name_plural': 'holdings'},
        ),
        migrations.AlterModelOptions(
            name='person',
            options={'ordering': ('first_name', 'last_name'), 'verbose_name': 'person', 'verbose_name_plural': 'people', 'permissions': (('view_person', 'Can view person'),)},
        ),
        migrations.RemoveField(
            model_name='purchase',
            name='holdings',
        ),
        migrations.AddField(
            model_name='holding',
            name='purchase',
            field=models.ForeignKey(related_name='holdings', verbose_name='purchase', blank=True, to='tickle.Purchase', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(max_length=256, verbose_name='name'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='delivery',
            name='delivered',
            field=models.DateTimeField(verbose_name='delivered'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='delivery',
            name='holdings',
            field=models.ManyToManyField(to='tickle.Holding', verbose_name='holdings'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='holding',
            name='person',
            field=models.ForeignKey(related_name='holdings', verbose_name='person', to='tickle.Person'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='holding',
            name='product',
            field=models.ForeignKey(related_name='holdings', verbose_name='product', to='tickle.Product'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='holding',
            name='quantity',
            field=models.PositiveIntegerField(default=1, verbose_name='quantity'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='product',
            name='categories',
            field=models.ManyToManyField(to='tickle.Category', null=True, verbose_name='categories', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='product',
            name='quantitative',
            field=models.BooleanField(default=False, help_text='Can you purchase more than one (1) of this product?', verbose_name='quantitative'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='purchase',
            name='person',
            field=models.ForeignKey(verbose_name='person', to='tickle.Person'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='purchase',
            name='purchased',
            field=models.DateTimeField(verbose_name='purchased'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='purchase',
            name='valid',
            field=models.BooleanField(default=True, verbose_name='valid'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='tickettype',
            name='product',
            field=models.OneToOneField(parent_link=True, related_name='ticket_type', primary_key=True, serialize=False, to='tickle.Product', verbose_name='product'),
            preserve_default=True,
        ),
    ]
