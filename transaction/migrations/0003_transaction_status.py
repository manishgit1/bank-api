# Generated by Django 5.0.2 on 2024-05-21 15:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transaction', '0002_rename_category_transaction_remarks'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='status',
            field=models.BooleanField(default=False),
        ),
    ]
