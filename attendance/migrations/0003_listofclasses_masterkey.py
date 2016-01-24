# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0002_listofclasses'),
    ]

    operations = [
        migrations.AddField(
            model_name='listofclasses',
            name='masterKey',
            field=models.CharField(default='ztqCMrTWAL95OpUfQDYD6K9igRtTdJgM922M1TSp', max_length=100),
            preserve_default=False,
        ),
    ]
