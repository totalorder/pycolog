# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('listen', '0003_auto_20140915_2000'),
    ]

    operations = [
        migrations.AddField(
            model_name='logger',
            name='ip_address',
            field=models.CharField(default='127.0.0.1:8002', max_length=21),
            preserve_default=False,
        ),
    ]
