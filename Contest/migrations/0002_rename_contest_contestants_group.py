# Generated by Django 4.2.7 on 2023-11-25 07:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Contest', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='contestants',
            old_name='contest',
            new_name='group',
        ),
    ]
