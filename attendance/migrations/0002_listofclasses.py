# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('attendance', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ListOfClasses',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('someClass', models.CharField(max_length=20)),
                ('appKey', models.CharField(max_length=100)),
                ('restKey', models.CharField(max_length=100)),
                ('javaKey', models.CharField(max_length=100)),
                ('schoolUser', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
