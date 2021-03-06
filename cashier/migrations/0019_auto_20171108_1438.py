# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-11-08 13:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cashier', '0018_auto_20171108_1429'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='payment',
            name='dateOfRefund',
        ),
        migrations.AlterField(
            model_name='transaction',
            name='typeOfTransaction',
            field=models.CharField(choices=[('debt', 'Debt'), ('expense', 'Expense'), ('pay', 'Payment')], default='debt', max_length=7, verbose_name='Type'),
        ),
    ]
