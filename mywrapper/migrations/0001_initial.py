# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Attendance',
            fields=[
                ('studentID', models.CharField(max_length=100, serialize=False, primary_key=True)),
                ('dateOfAttendance', models.DateField()),
                ('timeAttendanceWasMarked', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Grade',
            fields=[
                ('fullGradeID', models.CharField(max_length=25, serialize=False, primary_key=True)),
                ('StandardID', models.CharField(max_length=25)),
                ('SectionID', models.CharField(max_length=25)),
            ],
        ),
        migrations.CreateModel(
            name='Notice',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('category', models.CharField(max_length=50)),
                ('message', models.CharField(max_length=800)),
                ('timeNoticeWasMarked', models.DateTimeField(auto_now_add=True)),
                ('classToSendNotice', models.ForeignKey(to='mywrapper.Grade')),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('studentID', models.CharField(max_length=100, serialize=False, primary_key=True)),
                ('fullgrade', models.ForeignKey(to='mywrapper.Grade')),
            ],
        ),
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('subjectID', models.CharField(max_length=25, serialize=False, primary_key=True)),
                ('fullgrade', models.ForeignKey(to='mywrapper.Grade')),
            ],
        ),
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('teacherID', models.CharField(max_length=100, serialize=False, primary_key=True)),
                ('fullgrade', models.ForeignKey(to='mywrapper.Grade')),
            ],
        ),
        migrations.AddField(
            model_name='attendance',
            name='fullgrade',
            field=models.ForeignKey(to='mywrapper.Grade'),
        ),
    ]
