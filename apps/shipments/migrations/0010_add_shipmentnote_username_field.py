# Generated by Django 2.2.7 on 2020-03-02 16:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shipments', '0009_add_shipment_assignee_field'),
    ]

    operations = [
        migrations.AddField(
            model_name='shipmentnote',
            name='username',
            field=models.CharField(max_length=150, null=True),
        ),
    ]
