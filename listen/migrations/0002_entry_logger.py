# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('listen', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='entry',
            name='logger',
            field=models.CharField(default='asdgweg', max_length=512),
            preserve_default=False,
        ),
    ]
