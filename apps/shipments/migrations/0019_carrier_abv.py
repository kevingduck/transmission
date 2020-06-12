# Generated by Django 2.2.14 on 2020-07-14 13:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shipments', '0018_db_indexes'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicalshipment',
            name='carrier_abbv',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='shipment',
            name='carrier_abbv',
            field=models.CharField(max_length=100, null=True),
        ),
    ]