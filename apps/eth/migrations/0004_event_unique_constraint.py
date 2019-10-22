# Generated by Django 2.2.4 on 2019-10-22 15:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eth', '0003_deduplicate_events'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='event',
            constraint=models.UniqueConstraint(fields=('eth_action', 'log_index'), name='unique event'),
        ),
    ]
