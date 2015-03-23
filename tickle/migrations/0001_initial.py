# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
import mptt.fields


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0001_initial'),
        ('contenttypes', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TickleUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(default=django.utils.timezone.now, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(max_length=256, unique=True, null=True, verbose_name='LiU ID or email address', blank=True)),
                ('is_active', models.BooleanField(default=True, verbose_name='is active')),
                ('is_admin', models.BooleanField(default=False, verbose_name='is admin')),
                ('groups', models.ManyToManyField(related_query_name='user', related_name='user_set', to='auth.Group', blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of his/her group.', verbose_name='groups')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=256, verbose_name='name')),
            ],
            options={
                'verbose_name': 'category',
                'verbose_name_plural': 'categories',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Delivery',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('delivered', models.DateTimeField(verbose_name='delivered')),
            ],
            options={
                'verbose_name': 'delivery',
                'verbose_name_plural': 'deliveries',
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
                'verbose_name': 'event',
                'verbose_name_plural': 'events',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Holding',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('quantity', models.PositiveIntegerField(default=1, verbose_name='quantity')),
            ],
            options={
                'verbose_name': 'holding',
                'verbose_name_plural': 'holdings',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('first_name', models.CharField(max_length=256, verbose_name='first name')),
                ('last_name', models.CharField(max_length=256, verbose_name='last name')),
                ('birth_date', models.DateField(null=True, blank=True)),
                ('pid_code', models.CharField(help_text='Last 4 digits in Swedish national identity number.', max_length=4, null=True, verbose_name='national identity code', blank=True)),
                ('liu_id', models.CharField(default='', max_length=10, verbose_name='LiU ID', blank=True)),
                ('liu_id_blocked', models.NullBooleanField(verbose_name='LiU ID blocked')),
                ('liu_card_magnet', models.CharField(max_length=32, verbose_name='magnet/barcode card number', blank=True)),
                ('liu_card_rfid', models.CharField(max_length=32, verbose_name='RFID card number', blank=True)),
                ('phone', models.CharField(max_length=24, verbose_name='phone number', blank=True)),
                ('email', models.EmailField(unique=True, max_length=256, verbose_name='email address')),
                ('notes', models.TextField(help_text='Want us to know something else?', verbose_name='other information', blank=True)),
                ('our_notes', models.TextField(help_text='Internal notes. Cannot be seen by this person.', verbose_name='our notes', blank=True)),
            ],
            options={
                'ordering': ('first_name', 'last_name'),
                'verbose_name': 'person',
                'verbose_name_plural': 'people',
                'permissions': (('view_person', 'Can view person'),),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=256, verbose_name='name')),
                ('_public_name', models.CharField(max_length=256, null=True, verbose_name='public name', blank=True)),
                ('description', models.TextField(verbose_name='description', blank=True)),
                ('price', models.DecimalField(verbose_name='price', max_digits=12, decimal_places=2)),
                ('quantitative', models.BooleanField(default=False, help_text='Can you purchase more than one (1) of this product?', verbose_name='quantitative')),
                ('published', models.BooleanField(default=True, verbose_name='published')),
            ],
            options={
                'ordering': ('name',),
                'verbose_name': 'product',
                'verbose_name_plural': 'products',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ProductDiscount',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('discount_object_id', models.PositiveIntegerField()),
                ('discount_content_type', models.ForeignKey(to='contenttypes.ContentType')),
            ],
            options={
                'verbose_name': 'product discount',
                'verbose_name_plural': 'product discounts',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Purchase',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('purchased', models.DateTimeField(verbose_name='purchased')),
                ('valid', models.BooleanField(default=True, verbose_name='valid')),
                ('person', models.ForeignKey(verbose_name='person', to='tickle.Person')),
            ],
            options={
                'verbose_name': 'purchase',
                'verbose_name_plural': 'purchases',
            },
            bases=(models.Model,),
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
        migrations.CreateModel(
            name='TicketType',
            fields=[
                ('product', models.OneToOneField(parent_link=True, related_name='ticket_type', primary_key=True, serialize=False, to='tickle.Product', verbose_name='product')),
                ('events', models.ManyToManyField(to='tickle.Event', verbose_name='events')),
            ],
            options={
                'verbose_name': 'ticket type',
                'verbose_name_plural': 'ticket types',
            },
            bases=('tickle.product',),
        ),
        migrations.AddField(
            model_name='productdiscount',
            name='product',
            field=models.ForeignKey(related_name='discounts', to='tickle.Product'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='product',
            name='categories',
            field=models.ManyToManyField(to='tickle.Category', null=True, verbose_name='categories', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='person',
            name='liu_student_union',
            field=models.ForeignKey(related_name='members', verbose_name='student union', blank=True, to='tickle.StudentUnion', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='person',
            name='special_nutrition',
            field=models.ManyToManyField(help_text='Specify any special nutritional needs or habits.', to='tickle.SpecialNutrition', null=True, verbose_name='special nutrition', blank=True),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='person',
            unique_together=set([('birth_date', 'pid_code')]),
        ),
        migrations.AddField(
            model_name='holding',
            name='person',
            field=models.ForeignKey(related_name='holdings', verbose_name='person', to='tickle.Person'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='holding',
            name='product',
            field=models.ForeignKey(related_name='holdings', verbose_name='product', to='tickle.Product'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='holding',
            name='purchase',
            field=models.ForeignKey(related_name='holdings', verbose_name='purchase', blank=True, to='tickle.Purchase', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='delivery',
            name='holdings',
            field=models.ManyToManyField(to='tickle.Holding', verbose_name='holdings'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='tickleuser',
            name='person',
            field=models.OneToOneField(related_name='user', verbose_name='person', to='tickle.Person'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='tickleuser',
            name='user_permissions',
            field=models.ManyToManyField(related_query_name='user', related_name='user_set', to='auth.Permission', blank=True, help_text='Specific permissions for this user.', verbose_name='user permissions'),
            preserve_default=True,
        ),
    ]
