# Generated by Django 5.0.2 on 2024-03-06 03:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activation', '0022_alter_appuser_transaction_pin'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='transaction_id',
            field=models.AutoField(primary_key=True, serialize=False, unique=True),
        ),
    ]
