# Generated by Django 2.0.2 on 2018-02-05 22:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cashier', '0022_transaction_archived'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='room',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='cashier.Room'),
        ),
    ]
