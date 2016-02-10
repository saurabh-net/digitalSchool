# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0003_listofclasses_masterkey'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='listofclasses',
            name='masterKey',
        ),
    ]
