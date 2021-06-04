# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2018-06-12 21:27
from __future__ import unicode_literals

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion
import zentral.contrib.mdm.models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0037_auto_20180213_1407'),
        ('mdm', '0016_auto_20180612_1949'),
    ]

    operations = [
        migrations.CreateModel(
            name='MDMEnrollmentPackage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('builder', models.CharField(max_length=256)),
                ('enrollment_pk', models.PositiveIntegerField()),
                # zentral.contrib.mdm.models.enrollment_package_path removed
                ('file', models.FileField(blank=True, upload_to=None)),
                ('manifest', django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True)),
                ('version', models.PositiveIntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('trashed_at', models.DateTimeField(editable=False, null=True)),
                ('meta_business_unit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventory.MetaBusinessUnit')),
            ],
        ),
    ]
