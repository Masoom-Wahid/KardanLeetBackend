# Generated by Django 5.0.2 on 2024-02-17 06:06

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Contest', '0021_contest_groups_tabswitch'),
    ]

    operations = [
        migrations.AddField(
            model_name='contests',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
