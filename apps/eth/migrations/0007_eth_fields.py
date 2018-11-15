# Generated by Django 2.0.9 on 2018-11-15 19:16

import apps.eth.fields
import django.core.validators
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('eth', '0006_auto_20180830_2239'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ethaction',
            name='transaction_hash',
            field=apps.eth.fields.HashField(default='', max_length=66, primary_key=True, serialize=False, validators=[django.core.validators.RegexValidator(message='Invalid hash.', regex='^0x([A-Fa-f0-9]{64})$')]),
        ),
        migrations.AlterField(
            model_name='event',
            name='address',
            field=apps.eth.fields.AddressField(default='0x0', max_length=42, validators=[django.core.validators.RegexValidator(message='Invalid address.', regex='^0x([A-Fa-f0-9]{40})$')]),
        ),
        migrations.AlterField(
            model_name='event',
            name='block_hash',
            field=apps.eth.fields.HashField(default='', max_length=66, validators=[django.core.validators.RegexValidator(message='Invalid hash.', regex='^0x([A-Fa-f0-9]{64})$')]),
        ),
        migrations.AlterField(
            model_name='event',
            name='signature',
            field=apps.eth.fields.HashField(default='', max_length=66, validators=[django.core.validators.RegexValidator(message='Invalid hash.', regex='^0x([A-Fa-f0-9]{64})$')]),
        ),
        migrations.AlterField(
            model_name='event',
            name='transaction_hash',
            field=apps.eth.fields.HashField(default='', max_length=66, validators=[django.core.validators.RegexValidator(message='Invalid hash.', regex='^0x([A-Fa-f0-9]{64})$')]),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='to_address',
            field=apps.eth.fields.AddressField(default='0x0', max_length=42, validators=[django.core.validators.RegexValidator(message='Invalid address.', regex='^0x([A-Fa-f0-9]{40})$')]),
        ),
        migrations.AlterField(
            model_name='transactionreceipt',
            name='block_hash',
            field=apps.eth.fields.HashField(default='', max_length=66, validators=[django.core.validators.RegexValidator(message='Invalid hash.', regex='^0x([A-Fa-f0-9]{64})$')]),
        ),
        migrations.AlterField(
            model_name='transactionreceipt',
            name='contract_address',
            field=apps.eth.fields.AddressField(default='0x0', max_length=42, validators=[django.core.validators.RegexValidator(message='Invalid address.', regex='^0x([A-Fa-f0-9]{40})$')]),
        ),
        migrations.AlterField(
            model_name='transactionreceipt',
            name='from_address',
            field=apps.eth.fields.AddressField(default='0x0', max_length=42, validators=[django.core.validators.RegexValidator(message='Invalid address.', regex='^0x([A-Fa-f0-9]{40})$')]),
        ),
        migrations.AlterField(
            model_name='transactionreceipt',
            name='to_address',
            field=apps.eth.fields.AddressField(default='0x0', max_length=42, validators=[django.core.validators.RegexValidator(message='Invalid address.', regex='^0x([A-Fa-f0-9]{40})$')]),
        ),
    ]
