# Generated by Django 4.2.7 on 2024-01-14 13:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Contest', '0014_contests_started_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contest_submissiosn',
            name='submit_time',
            field=models.IntegerField(),
        ),
    ]
