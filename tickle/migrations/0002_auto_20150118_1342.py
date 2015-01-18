# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('tickle', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='birth_date',
            field=models.DateField(default=datetime.datetime(2015, 1, 18, 13, 42, 56, 945407, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='person',
            name='our_notes',
            field=models.TextField(help_text='Internal notes. Cannot be seen by this person.', verbose_name='our notes', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='person',
            name='pid_code',
            field=models.CharField(help_text='Last 4 chars in Swedish national identity number.', max_length=4, null=True, verbose_name='national identity suffix', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='product',
            name='_public_name',
            field=models.CharField(max_length=256, null=True, verbose_name='public name', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='person',
            name='notes',
            field=models.TextField(help_text='Want us to know something else?', verbose_name='other information', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='person',
            name='special_nutrition',
            field=models.ManyToManyField(help_text='Specify any special nutritional needs or habits.', to='tickle.SpecialNutrition', null=True, verbose_name='special nutrition', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='purchase',
            name='holdings',
            field=models.ManyToManyField(to='tickle.Holding', null=True),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='person',
            unique_together=set([('birth_date', 'pid_code')]),
        ),
        migrations.RemoveField(
            model_name='person',
            name='id_number',
        ),
    ]
