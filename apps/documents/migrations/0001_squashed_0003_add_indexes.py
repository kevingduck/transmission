# Generated by Django 3.0.8 on 2020-10-08 22:03

import apps.documents.models
import apps.simple_history
import apps.utils
from django.db import migrations, models
import django.db.models.deletion
import enumfields.fields
import shipchain_common.utils
import simple_history.models
import uuid


class Migration(migrations.Migration):

    replaces = [('documents', '0001_initial'), ('documents', '0002_historical_document'), ('documents', '0003_add_indexes')]

    initial = True

    dependencies = [
        ('shipments', '0001_squashed_091919'),
    ]

    operations = [
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.CharField(default=shipchain_common.utils.random_id, max_length=36, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=36)),
                ('description', models.CharField(blank=True, max_length=250, null=True)),
                ('owner_id', models.CharField(max_length=36)),
                ('document_type', enumfields.fields.EnumIntegerField(default=0, enum=apps.documents.models.DocumentType)),
                ('file_type', enumfields.fields.EnumIntegerField(default=0, enum=apps.documents.models.FileType)),
                ('upload_status', enumfields.fields.EnumIntegerField(default=0, enum=apps.utils.UploadStatus)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('shipment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shipments.Shipment')),
            ],
            options={
                'ordering': ('-created_at',),
            },
        ),
        migrations.CreateModel(
            name='HistoricalDocument',
            fields=[
                ('id', models.CharField(db_index=True, default=shipchain_common.utils.random_id, max_length=36)),
                ('name', models.CharField(max_length=36)),
                ('description', models.CharField(blank=True, max_length=250, null=True)),
                ('owner_id', models.CharField(max_length=36)),
                ('document_type', enumfields.fields.EnumIntegerField(default=0, enum=apps.documents.models.DocumentType)),
                ('file_type', enumfields.fields.EnumIntegerField(default=0, enum=apps.documents.models.FileType)),
                ('upload_status', enumfields.fields.EnumIntegerField(default=0, enum=apps.utils.UploadStatus)),
                ('updated_at', models.DateTimeField(blank=True, editable=False)),
                ('created_at', models.DateTimeField(blank=True, editable=False)),
                ('history_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField(db_index=True)),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.CharField(blank=True, max_length=36, null=True)),
                ('shipment', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='shipments.HistoricalShipment')),
            ],
            options={
                'verbose_name': 'historical document',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
            bases=(simple_history.models.HistoricalChanges, models.Model, apps.simple_history.HistoricalChangesMixin),
        ),
    ]
