# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tickle', '0003_auto_20141125_0131'),
    ]

    operations = [
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
            name='Holding',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('person', models.ForeignKey(to='tickle.Person')),
                ('product', models.ForeignKey(to='tickle.Product')),
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
                ('holdings', models.ManyToManyField(to='tickle.Holding')),
                ('person', models.ForeignKey(to='tickle.Person')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='ownership',
            name='person',
        ),
        migrations.RemoveField(
            model_name='ownership',
            name='product',
        ),
        migrations.DeleteModel(
            name='Ownership',
        ),
        migrations.AddField(
            model_name='delivery',
            name='holding',
            field=models.ManyToManyField(to='tickle.Holding'),
            preserve_default=True,
        ),
    ]
