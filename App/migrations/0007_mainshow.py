# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-06-18 01:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0006_mainshop'),
    ]

    operations = [
        migrations.CreateModel(
            name='MainShow',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('img', models.CharField(max_length=200)),
                ('name', models.CharField(max_length=100)),
                ('trackid', models.CharField(max_length=16)),
                ('categoryid', models.CharField(max_length=16)),
                ('brandname', models.CharField(max_length=12)),
                ('img1', models.CharField(max_length=200)),
                ('childcid1', models.CharField(max_length=20)),
                ('productid1', models.CharField(max_length=16)),
                ('longname1', models.CharField(max_length=128)),
                ('price1', models.FloatField(default=1)),
                ('marketprice1', models.FloatField(default=2)),
                ('img2', models.CharField(max_length=200)),
                ('childcid2', models.CharField(max_length=20)),
                ('productid2', models.CharField(max_length=16)),
                ('longname2', models.CharField(max_length=128)),
                ('price2', models.FloatField(default=1)),
                ('marketprice2', models.FloatField(default=2)),
                ('img3', models.CharField(max_length=200)),
                ('childcid3', models.CharField(max_length=20)),
                ('productid3', models.CharField(max_length=16)),
                ('longname3', models.CharField(max_length=128)),
                ('price3', models.FloatField(default=1)),
                ('marketprice3', models.FloatField(default=2)),
            ],
            options={
                'db_table': 'axf_mainshow',
            },
        ),
    ]