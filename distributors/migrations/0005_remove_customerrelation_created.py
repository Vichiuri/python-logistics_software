# Generated by Django 4.0.6 on 2022-07-27 08:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('distributors', '0004_document_consignmentnote'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customerrelation',
            name='created',
        ),
    ]
