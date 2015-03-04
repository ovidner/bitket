# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tickle', '0010_auto_20150223_0056'),
        ('fungus', '0002_auto_20150222_0002'),
    ]

    operations = [
        migrations.CreateModel(
            name='Functionary',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ice_number', models.CharField(max_length=16, null=True, verbose_name='ICE number', blank=True)),
                ('person', models.OneToOneField(related_name='functionary', to='tickle.Person')),
            ],
            options={
                'verbose_name': 'functionary',
                'verbose_name_plural': 'functionaries',
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='worker',
            name='person',
        ),
        migrations.DeleteModel(
            name='Worker',
        ),
        migrations.CreateModel(
            name='Worker',
            fields=[
            ],
            options={
                'verbose_name': 'worker',
                'proxy': True,
                'verbose_name_plural': 'workers',
            },
            bases=('tickle.person',),
        ),
        migrations.RemoveField(
            model_name='shift',
            name='people_warning',
        ),
        migrations.AddField(
            model_name='shift',
            name='people_alarming',
            field=models.PositiveIntegerField(help_text='The number of workers where the system will report the status as alarming.', null=True, verbose_name='alarming number of workers', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='shiftregistration',
            name='checked_in',
            field=models.DateTimeField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='shiftregistration',
            name='checked_out',
            field=models.DateTimeField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='shift',
            name='people_critical',
            field=models.PositiveIntegerField(help_text='The number of workers where the system will report the status as critical.', null=True, verbose_name='critical number of workers', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='shift',
            name='people_max',
            field=models.PositiveIntegerField(help_text="The maximum number of workers on this shift. This shift's status will be reported as overstaffed if the number of workers are over this value.", null=True, verbose_name='maximum number of workers', blank=True),
            preserve_default=True,
        ),
    ]
