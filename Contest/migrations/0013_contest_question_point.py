# Generated by Django 4.2.7 on 2023-12-11 12:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Contest', '0012_contests_finished'),
    ]

    operations = [
        migrations.AddField(
            model_name='contest_question',
            name='point',
            field=models.IntegerField(default=10),
            preserve_default=False,
        ),
    ]