# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
import mptt.fields


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0001_initial'),
        ('liu', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TickleUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(default=django.utils.timezone.now, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(unique=True, max_length=256)),
                ('is_active', models.BooleanField(default=True)),
                ('is_admin', models.BooleanField(default=False)),
                ('groups', models.ManyToManyField(related_query_name='user', related_name='user_set', to='auth.Group', blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of his/her group.', verbose_name='groups')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=256)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Delivery',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('delivered', models.DateTimeField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=256, verbose_name='name')),
                ('lft', models.PositiveIntegerField(editable=False, db_index=True)),
                ('rght', models.PositiveIntegerField(editable=False, db_index=True)),
                ('tree_id', models.PositiveIntegerField(editable=False, db_index=True)),
                ('level', models.PositiveIntegerField(editable=False, db_index=True)),
                ('parent', mptt.fields.TreeForeignKey(blank=True, to='tickle.Event', null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Holding',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('quantity', models.PositiveIntegerField(default=1)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('first_name', models.CharField(max_length=256, verbose_name='first name')),
                ('last_name', models.CharField(max_length=256, verbose_name='last name')),
                ('id_number', models.CharField(unique=True, max_length=11, verbose_name='national identification number')),
                ('phone', models.CharField(max_length=24, verbose_name=b'phone number', blank=True)),
                ('email', models.EmailField(unique=True, max_length=256, verbose_name='email address')),
                ('notes', models.TextField(blank=True)),
                ('liu_id', models.OneToOneField(null=True, blank=True, to='liu.LiUID', verbose_name='LiU ID')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=256, verbose_name='name')),
                ('description', models.TextField(verbose_name='description', blank=True)),
                ('price', models.DecimalField(verbose_name='price', max_digits=12, decimal_places=2)),
                ('quantitative', models.BooleanField(default=False, help_text='Can you purchase more than one (1) of this product?')),
                ('categories', models.ManyToManyField(to='tickle.Category', null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Purchase',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('purchased', models.DateTimeField()),
                ('valid', models.BooleanField(default=True)),
                ('holdings', models.ManyToManyField(to='tickle.Holding')),
                ('person', models.ForeignKey(to='tickle.Person')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SpecialNutrition',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=256)),
            ],
            options={
                'ordering': ['name'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TicketType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('events', models.ManyToManyField(to='tickle.Event', verbose_name='events')),
                ('product', models.OneToOneField(related_name='ticket_type', to='tickle.Product')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='person',
            name='special_nutrition',
            field=models.ManyToManyField(to='tickle.SpecialNutrition', null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='holding',
            name='person',
            field=models.ForeignKey(related_name='holdings', to='tickle.Person'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='holding',
            name='product',
            field=models.ForeignKey(related_name='holdings', to='tickle.Product'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='delivery',
            name='holdings',
            field=models.ManyToManyField(to='tickle.Holding'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='tickleuser',
            name='person',
            field=models.OneToOneField(related_name='user', null=True, blank=True, to='tickle.Person'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='tickleuser',
            name='user_permissions',
            field=models.ManyToManyField(related_query_name='user', related_name='user_set', to='auth.Permission', blank=True, help_text='Specific permissions for this user.', verbose_name='user permissions'),
            preserve_default=True,
        ),
    ]
