# Generated by Django 5.0.2 on 2024-02-15 05:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Contest', '0020_contest_question_created_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='contest_groups',
            name='tabswitch',
            field=models.IntegerField(default=0),
        ),
    ]
