# Generated by Django 2.1.7 on 2019-03-21 20:20

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shipments', '0032_location_country_data_migration'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='location',
            name='owner_id',
        ),
        migrations.AlterField(
            model_name='location',
            name='country',
            field=models.CharField(blank=True, max_length=2, null=True, validators=[django.core.validators.RegexValidator(message='Invalid ISO 3166-1 alpha-2 country code.', regex='^A[^ABCHJKNPVY]|B[^CKPUX]|C[^BEJPQST]|D[EJKMOZ]|E[CEGHRST]|F[IJKMOR]|G[^CJKOVXZ]|H[KMNRTU]|I[DEL-OQ-T]|J[EMOP]|K[EGHIMNPRWYZ]|L[ABCIKR-VY]|M[^BIJ]|N[ACEFGILOPRUZ]|OM|P[AE-HK-NRSTWY]|QA|R[EOSUW]|S[^FPQUW]|T[^ABEIPQSUXY]|U[AGMSYZ]|V[ACEGINU]|WF|WS|YE|YT|Z[AMW]')]),
        ),
        migrations.AlterField(
            model_name='shipment',
            name='bill_to_location',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='shipment_bill', to='shipments.Location'),
        ),
        migrations.AlterField(
            model_name='shipment',
            name='final_destination_location',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='shipment_dest', to='shipments.Location'),
        ),
        migrations.AlterField(
            model_name='shipment',
            name='ship_from_location',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='shipment_from', to='shipments.Location'),
        ),
        migrations.AlterField(
            model_name='shipment',
            name='ship_to_location',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='shipment_to', to='shipments.Location'),
        ),
    ]
