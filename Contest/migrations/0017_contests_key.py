# Generated by Django 4.2.7 on 2024-01-21 10:00

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('Contest', '0016_alter_contests_started_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='contests',
            name='key',
            field=models.TextField(default=django.utils.timezone.now, unique=True),
            preserve_default=False,
        ),
    ]
