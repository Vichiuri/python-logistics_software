# Generated by Django 3.1 on 2022-07-14 14:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('distributors', '0002_driver'),
    ]

    operations = [
        migrations.AlterField(
            model_name='driver',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='vehicle',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
