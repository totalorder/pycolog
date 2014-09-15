# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('listen', '0002_entry_logger'),
    ]

    operations = [
        migrations.CreateModel(
            name='Logger',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=512)),
                ('regex', models.CharField(default=b'(\\[(error|warning|info|debug)])', max_length=1024)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField('Entry', 'logger'),
        migrations.AddField(
            model_name='entry',
            name='logger',
            field=models.ForeignKey(related_name=b'entries', to='listen.Logger'),
        ),
    ]
