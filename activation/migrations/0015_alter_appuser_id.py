# Generated by Django 5.0.2 on 2024-03-05 05:29

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activation', '0014_alter_appuser_transaction_pin'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appuser',
            name='id',
            field=models.AutoField( primary_key=True, serialize=False),
        ),
    ]