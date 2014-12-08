# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tickle', '0001_initial'),
        ('orchard', '0003_auto_20141208_1527'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrchestraProduct',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('product', models.OneToOneField(related_name='orchestra_product', to='tickle.Product')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
