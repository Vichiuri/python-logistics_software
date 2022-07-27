# Generated by Django 4.0.6 on 2022-07-26 14:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('distributors', '0003_valuer'),
    ]

    operations = [
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('doc_name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='ConsignmentNote',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reference_no', models.CharField(blank=True, max_length=100, null=True)),
                ('description', models.CharField(max_length=100)),
                ('quantity', models.PositiveIntegerField()),
                ('bundle', models.PositiveIntegerField()),
                ('rate', models.PositiveIntegerField()),
                ('per', models.CharField(max_length=100)),
                ('amount', models.CharField(max_length=100)),
                ('tax', models.CharField(blank=True, max_length=100, null=True)),
                ('inclusive', models.CharField(blank=True, max_length=100, null=True)),
                ('tracking_no', models.PositiveIntegerField(default=0)),
                ('is_delivered', models.BooleanField(default=False)),
                ('date_created', models.DateField(blank=True, null=True)),
                ('consignee', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='consignee', to='distributors.customerrelation')),
                ('document', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='distributors.document')),
                ('route', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='distributors.route')),
                ('sender_name', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='sender_name', to='distributors.customerrelation')),
                ('town', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='distributors.town')),
                ('valuer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='distributors.valuer')),
            ],
            options={
                'db_table': 'consignment_note',
            },
        ),
    ]