# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('invar', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BgMaxImport',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('file_name', models.CharField(max_length=256, verbose_name='file name')),
                ('file_sha1', models.CharField(unique=True, max_length=40, verbose_name='file SHA1')),
                ('import_timestamp', models.DateTimeField(auto_now_add=True, verbose_name='import timestamp')),
                ('creation_timestamp', models.DateTimeField(verbose_name='creation timestamp')),
            ],
            options={
                'verbose_name': 'BgMax import',
                'verbose_name_plural': 'BgMax imports',
            },
        ),
        migrations.AddField(
            model_name='transaction',
            name='uid',
            field=models.CharField(max_length=256, unique=True, null=True, verbose_name='unique identifier', blank=True),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='timestamp',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='timestamp'),
        ),
    ]
