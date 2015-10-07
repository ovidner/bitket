# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import tickle.common.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
    ]

    operations = [
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(null=True, verbose_name='last login', blank=True)),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('birth_date', models.DateField(null=True, verbose_name='birth date', blank=True)),
                ('pid_code', models.CharField(help_text='Last 4 digits in Swedish national identity number.', max_length=4, null=True, verbose_name='national identity code', blank=True)),
                ('pid_coordination', models.BooleanField(default=False, help_text='Designates if national identity number is a <em>samordningsnummer</em>.', verbose_name='coordination number')),
                ('first_name', tickle.common.db.fields.NameField(max_length=64, verbose_name='first name')),
                ('last_name', tickle.common.db.fields.NameField(max_length=64, verbose_name='last name')),
                ('stripe_customer_id', models.CharField(max_length=64, verbose_name='Stripe customer ID')),
                ('liu_id', models.CharField(null=True, default=None, max_length=10, blank=True, unique=True, verbose_name='LiU ID')),
                ('liu_id_blocked', models.NullBooleanField(verbose_name='LiU ID blocked')),
                ('liu_card_magnet', models.CharField(max_length=32, verbose_name='magnet/barcode card number', blank=True)),
                ('liu_card_rfid', models.CharField(max_length=32, verbose_name='RFID card number', blank=True)),
                ('email', models.EmailField(unique=True, max_length=256, verbose_name='email address')),
                ('is_active', models.BooleanField(default=True, verbose_name='is active')),
                ('is_staff', models.BooleanField(default=False, verbose_name='is staff')),
                ('groups', models.ManyToManyField(related_query_name='user', related_name='user_set', to='auth.Group', blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', verbose_name='groups')),
            ],
            options={
                'ordering': ['first_name', 'last_name'],
                'verbose_name': 'person',
                'verbose_name_plural': 'people',
            },
        ),
        migrations.CreateModel(
            name='SpecialNutrition',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=256, verbose_name='name')),
            ],
            options={
                'ordering': ['name'],
                'verbose_name': 'special nutrition',
                'verbose_name_plural': 'special nutritions',
            },
        ),
        migrations.CreateModel(
            name='StudentUnion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', tickle.common.db.fields.NameField(unique=True, max_length=64, verbose_name='name')),
                ('slug', tickle.common.db.fields.SlugField(unique=True, max_length=64, verbose_name='slug')),
            ],
        ),
        migrations.AddField(
            model_name='person',
            name='liu_student_union',
            field=models.ForeignKey(related_name='members', verbose_name='student union', blank=True, to='people.StudentUnion', null=True),
        ),
        migrations.AddField(
            model_name='person',
            name='special_nutrition',
            field=models.ManyToManyField(help_text='Specify any special nutritional needs or habits.', to='people.SpecialNutrition', verbose_name='special nutrition', blank=True),
        ),
        migrations.AddField(
            model_name='person',
            name='user_permissions',
            field=models.ManyToManyField(related_query_name='user', related_name='user_set', to='auth.Permission', blank=True, help_text='Specific permissions for this user.', verbose_name='user permissions'),
        ),
        migrations.AlterUniqueTogether(
            name='person',
            unique_together=set([('birth_date', 'pid_code', 'pid_coordination')]),
        ),
    ]
