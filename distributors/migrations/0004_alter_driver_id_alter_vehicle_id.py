# Generated by Django 4.0.6 on 2022-07-14 14:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('distributors', '0003_auto_20220714_1405'),
    ]

    operations = [
        migrations.AlterField(
            model_name='driver',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='vehicle',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
