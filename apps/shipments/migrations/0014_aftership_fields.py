# Generated by Django 2.2.12 on 2020-04-08 15:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shipments', '0013_telemetrydata'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicalshipment',
            name='aftership_tracking',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='shipment',
            name='aftership_tracking',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
