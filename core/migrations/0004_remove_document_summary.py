# Generated by Django 5.1.4 on 2024-12-19 07:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_document_summary'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='document',
            name='summary',
        ),
    ]