# Generated by Django 2.2.7 on 2019-12-05 19:05

import apps.shipments.models
from django.db import migrations, models
import django.db.models.deletion
import enumfields.fields
import shipchain_common.utils


class Migration(migrations.Migration):

    dependencies = [
        ('shipments', '0012_shipment_tags'),
    ]

    operations = [
        migrations.CreateModel(
            name='TelemetryData',
            fields=[
                ('id', models.CharField(default=shipchain_common.utils.random_id, max_length=36, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('timestamp', models.DateTimeField()),
                ('hardware_id', models.CharField(max_length=255)),
                ('sensor_id', models.CharField(max_length=36)),
                ('version', models.CharField(max_length=36)),
                ('value', models.FloatField()),
                ('device', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='shipments.Device')),
                ('shipment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shipments.Shipment')),
            ],
            options={
                'ordering': ('timestamp',),
            },
        ),
    ]
