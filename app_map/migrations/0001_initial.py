# Generated by Django 4.0.4 on 2022-05-23 01:58

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='placa',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, help_text='ID de la placa', primary_key=True, serialize=False)),
                ('imprint', models.CharField(max_length=6)),
            ],
        ),
    ]
