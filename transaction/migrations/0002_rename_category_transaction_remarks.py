# Generated by Django 5.0.2 on 2024-03-13 05:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('transaction', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='transaction',
            old_name='category',
            new_name='remarks',
        ),
    ]