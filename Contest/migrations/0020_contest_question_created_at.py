# Generated by Django 4.2.7 on 2024-01-25 08:59

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('Contest', '0019_remove_contest_question_contest_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='contest_question',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
