# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tickle', '0011_auto_20150428_0259'),
        ('karthago', '0005_entry_approved'),
    ]

    operations = [
        migrations.CreateModel(
            name='EntryMembership',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('entry', models.ForeignKey(related_name='memberships', verbose_name='entry', to='karthago.Entry')),
                ('person', models.ForeignKey(related_name='kartege_memberships', verbose_name='person', to='tickle.Person')),
            ],
            options={
                'verbose_name': 'entry membership',
                'verbose_name_plural': 'entry memberships',
            },
        ),
        migrations.CreateModel(
            name='KartegeMemberDiscount',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('discount_amount', models.DecimalField(null=True, verbose_name='amount', max_digits=9, decimal_places=2, blank=True)),
                ('discount_percent', models.DecimalField(decimal_places=2, max_digits=3, blank=True, help_text='Use decimal form, e.g. 0,25.', null=True, verbose_name='percent')),
            ],
            options={
                'verbose_name': 'K\xe5rtege member discount',
                'verbose_name_plural': 'K\xe5rtege member discounts',
            },
        ),
        migrations.AlterUniqueTogether(
            name='entrymembership',
            unique_together=set([('person', 'entry')]),
        ),
    ]
