# Generated by Django 5.0.2 on 2024-03-05 03:55

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activation', '0009_rename_user_id_appuser_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='transaction',
            name='id',
        ),
        migrations.AddField(
            model_name='appuser',
            name='transaction_pin',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='transaction',
            name='transaction_id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True),
        ),
    ]
