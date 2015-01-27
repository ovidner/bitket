# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tickle', '0003_auto_20150118_1609'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='person',
            options={'verbose_name': 'person', 'verbose_name_plural': 'people'},
        ),
        migrations.AlterModelOptions(
            name='specialnutrition',
            options={'ordering': ['name'], 'verbose_name': 'special nutrition', 'verbose_name_plural': 'special nutritions'},
        ),
        migrations.AlterModelOptions(
            name='tickleuser',
            options={'verbose_name': 'user', 'verbose_name_plural': 'users'},
        ),
        migrations.AlterField(
            model_name='person',
            name='pid_code',
            field=models.CharField(help_text='Last 4 digits in Swedish national identity number.', max_length=4, null=True, verbose_name='national identity code', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='specialnutrition',
            name='name',
            field=models.CharField(max_length=256, verbose_name='name'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='tickleuser',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='is active'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='tickleuser',
            name='is_admin',
            field=models.BooleanField(default=False, verbose_name='is admin'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='tickleuser',
            name='person',
            field=models.OneToOneField(related_name='user', null=True, blank=True, to='tickle.Person', verbose_name='person'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='tickleuser',
            name='username',
            field=models.CharField(unique=True, max_length=256, verbose_name='username'),
            preserve_default=True,
        ),
    ]
