# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2018-11-19 16:02
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myadmin', '0002_auto_20181115_2342'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cates',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('pid', models.IntegerField()),
                ('path', models.CharField(max_length=30)),
                ('isDelete', models.BooleanField(default=True)),
            ],
        ),
    ]
