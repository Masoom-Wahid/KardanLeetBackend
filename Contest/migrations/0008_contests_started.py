# Generated by Django 4.2.7 on 2023-12-04 17:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Contest', '0007_contests_starred'),
    ]

    operations = [
        migrations.AddField(
            model_name='contests',
            name='started',
            field=models.BooleanField(default=False),
        ),
    ]
