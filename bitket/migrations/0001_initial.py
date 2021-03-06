# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2016-12-07 05:24
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import bitket.db.fields
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0008_alter_user_username_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('id', bitket.db.fields.IdField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', bitket.db.fields.NameField(max_length=64, verbose_name='name')),
                ('email', models.EmailField(max_length=256, unique=True, verbose_name='email address')),
                ('nin', bitket.db.fields.NullCharField(blank=True, default=None, max_length=12, null=True, verbose_name='national identity number')),
                ('is_active', models.BooleanField(default=True, verbose_name='is active')),
                ('is_staff', models.BooleanField(default=False, verbose_name='is staff')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
            ],
            options={
                'ordering': ['name'],
                'verbose_name_plural': 'users',
                'verbose_name': 'user',
            },
        ),
        migrations.CreateModel(
            name='AccessCode',
            fields=[
                ('id', bitket.db.fields.IdField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'verbose_name_plural': 'access codes',
                'verbose_name': 'access code',
            },
        ),
        migrations.CreateModel(
            name='Condition',
            fields=[
                ('id', bitket.db.fields.IdField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='ID')),
                ('active', models.BooleanField(default=True, help_text='Determines whether the condition should be displayed and included in queries.', verbose_name='active')),
            ],
            options={
                'verbose_name_plural': 'conditions',
                'verbose_name': 'condition',
            },
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', bitket.db.fields.IdField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', bitket.db.fields.NameField(max_length=64, verbose_name='name')),
                ('slug', bitket.db.fields.SlugField(editable=True, max_length=64, populate_from='name', unique_with=('organization__slug',), verbose_name='slug')),
                ('description', bitket.db.fields.DescriptionField(blank=True, verbose_name='description')),
                ('published', models.BooleanField(default=True, verbose_name='published')),
            ],
            options={
                'ordering': ('name',),
                'verbose_name_plural': 'events',
                'verbose_name': 'event',
            },
        ),
        migrations.CreateModel(
            name='Modifier',
            fields=[
                ('id', bitket.db.fields.IdField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='ID')),
                ('delta', bitket.db.fields.MoneyField(decimal_places=2, help_text='For discount, enter a negative value.', max_digits=12, verbose_name='delta')),
            ],
            options={
                'verbose_name_plural': 'modifiers',
                'verbose_name': 'modifier',
            },
        ),
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('id', bitket.db.fields.IdField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', bitket.db.fields.NameField(max_length=64, unique=True, verbose_name='name')),
                ('slug', bitket.db.fields.SlugField(editable=False, max_length=64, populate_from='name', unique=True, verbose_name='slug')),
                ('stripe_authorized', models.DateTimeField(blank=True, null=True, verbose_name='Stripe authorization timestamp')),
                ('stripe_live_mode', models.BooleanField(default=False, verbose_name='Stripe live mode')),
                ('stripe_account_id', models.CharField(blank=True, max_length=64, verbose_name='Stripe account ID')),
                ('stripe_refresh_token', models.CharField(blank=True, max_length=64, verbose_name='Stripe refresh token')),
                ('stripe_public_key', models.CharField(blank=True, max_length=64, verbose_name='Stripe public key')),
                ('stripe_secret_key', models.CharField(blank=True, max_length=64, verbose_name='Stripe secret key')),
                ('stripe_read_only', models.BooleanField(default=True, verbose_name='Stripe read only access')),
                ('admins', models.ManyToManyField(related_name='admin_for_organizers', to=settings.AUTH_USER_MODEL, verbose_name='admins')),
            ],
            options={
                'permissions': [['manage_organization_stripe', 'Can manage Stripe for organization']],
            },
        ),
        migrations.CreateModel(
            name='StudentUnion',
            fields=[
                ('id', bitket.db.fields.IdField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', bitket.db.fields.NameField(max_length=64, unique=True, verbose_name='name')),
            ],
            options={
                'verbose_name_plural': 'student unions',
                'verbose_name': 'student union',
            },
        ),
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', bitket.db.fields.IdField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='ID')),
                ('pending', models.BooleanField(default=False, verbose_name='pending')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='created')),
                ('utilized', models.DateTimeField(blank=True, null=True, verbose_name='utilized')),
                ('access_code', models.ForeignKey(blank=True, help_text='The access code used to buy this ticket, if any.', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='tickets', to='bitket.AccessCode', verbose_name='access code')),
            ],
            options={
                'verbose_name_plural': 'tickets',
                'verbose_name': 'ticket',
            },
        ),
        migrations.CreateModel(
            name='TicketOwnership',
            fields=[
                ('id', bitket.db.fields.IdField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='ID')),
                ('switch_code', models.UUIDField(default=uuid.uuid4, verbose_name='switch code')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='created')),
                ('modifiers', models.ManyToManyField(related_name='ticket_ownerships', to='bitket.Modifier', verbose_name='utilized modifiers')),
                ('ticket', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ownerships', to='bitket.Ticket', verbose_name='ticket')),
            ],
            options={
                'verbose_name_plural': 'ticket ownerships',
                'verbose_name': 'ticket ownership',
                'get_latest_by': 'created',
            },
        ),
        migrations.CreateModel(
            name='TicketType',
            fields=[
                ('id', bitket.db.fields.IdField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', bitket.db.fields.NameField(max_length=64, verbose_name='name')),
                ('description', bitket.db.fields.DescriptionField(blank=True, verbose_name='description')),
                ('price', bitket.db.fields.MoneyField(decimal_places=2, max_digits=12, verbose_name='price')),
                ('is_published', models.BooleanField(default=True, verbose_name='published')),
                ('is_generally_available', models.BooleanField(default=False, verbose_name='generally available for purchase')),
                ('max_personal_quantity', models.PositiveIntegerField(blank=True, default=1, help_text='Blank means no limit.', null=True, verbose_name='maximum personal quantity')),
                ('max_total_quantity', models.PositiveIntegerField(blank=True, help_text='Blank means no limit.', null=True, verbose_name='maximum total quantity')),
                ('conflicts_with', models.ManyToManyField(blank=True, related_name='_tickettype_conflicts_with_+', to='bitket.TicketType', verbose_name='conflicts with')),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ticket_types', to='bitket.Event', verbose_name='event')),
            ],
            options={
                'ordering': ['name'],
                'verbose_name_plural': 'products',
                'verbose_name': 'product',
            },
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(default=django.utils.timezone.now, verbose_name='created')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=9, verbose_name='amount')),
                ('stripe_charge', models.CharField(max_length=64, verbose_name='Stripe charge')),
            ],
            options={
                'verbose_name_plural': 'transactions',
                'verbose_name': 'transaction',
            },
        ),
        migrations.CreateModel(
            name='Variation',
            fields=[
                ('id', bitket.db.fields.IdField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', bitket.db.fields.NameField(max_length=64, verbose_name='name')),
                ('ticket_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='variations', to='bitket.TicketType', verbose_name='ticket type')),
            ],
            options={
                'ordering': ['name'],
                'verbose_name_plural': 'product variations',
                'verbose_name': 'product variation',
            },
        ),
        migrations.CreateModel(
            name='VariationChoice',
            fields=[
                ('id', bitket.db.fields.IdField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', bitket.db.fields.NameField(max_length=64, verbose_name='name')),
                ('delta', bitket.db.fields.MoneyField(decimal_places=2, default=0, help_text='For discount, enter a negative value.', max_digits=12, verbose_name='delta')),
                ('variation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='choices', to='bitket.Variation', verbose_name='variation')),
            ],
            options={
                'verbose_name_plural': 'product variation choices',
                'verbose_name': 'product variation choice',
            },
        ),
        migrations.CreateModel(
            name='StudentUnionMemberCondition',
            fields=[
                ('condition_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='bitket.Condition')),
                ('student_union', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='bitket.StudentUnion', verbose_name='student union')),
            ],
            options={
                'verbose_name_plural': 'student union member conditions',
                'verbose_name': 'student union member condition',
            },
            bases=('bitket.condition',),
        ),
        migrations.AddField(
            model_name='ticketownership',
            name='transactions',
            field=models.ManyToManyField(related_name='ticket_ownerships', to='bitket.Transaction', verbose_name='transactions'),
        ),
        migrations.AddField(
            model_name='ticketownership',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ticket_ownerships', to=settings.AUTH_USER_MODEL, verbose_name='user'),
        ),
        migrations.AddField(
            model_name='ticket',
            name='ticket_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tickets', to='bitket.TicketType', verbose_name='ticket type'),
        ),
        migrations.AddField(
            model_name='ticket',
            name='variation_choices',
            field=models.ManyToManyField(blank=True, related_name='tickets', to='bitket.VariationChoice', verbose_name='variation choices'),
        ),
        migrations.AddField(
            model_name='modifier',
            name='condition',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='modifiers', to='bitket.Condition', verbose_name='condition'),
        ),
        migrations.AddField(
            model_name='modifier',
            name='ticket_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='modifiers', to='bitket.TicketType', verbose_name='product'),
        ),
        migrations.AddField(
            model_name='event',
            name='organization',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='events', to='bitket.Organization', verbose_name='organization'),
        ),
        migrations.AddField(
            model_name='accesscode',
            name='ticket_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bitket.TicketType'),
        ),
        migrations.AddField(
            model_name='user',
            name='student_union',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='members', to='bitket.StudentUnion', verbose_name='student union'),
        ),
        migrations.AddField(
            model_name='user',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions'),
        ),
        migrations.AlterUniqueTogether(
            name='variationchoice',
            unique_together=set([('name', 'variation')]),
        ),
        migrations.AlterUniqueTogether(
            name='variation',
            unique_together=set([('name', 'ticket_type')]),
        ),
        migrations.AlterUniqueTogether(
            name='modifier',
            unique_together=set([('condition', 'ticket_type')]),
        ),
        migrations.AlterUniqueTogether(
            name='event',
            unique_together=set([('organization', 'slug'), ('organization', 'name')]),
        ),
    ]
