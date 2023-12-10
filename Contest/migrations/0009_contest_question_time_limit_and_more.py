# Generated by Django 4.2.7 on 2023-12-10 08:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Contest', '0008_contests_started'),
    ]

    operations = [
        migrations.AddField(
            model_name='contest_question',
            name='time_limit',
            field=models.IntegerField(default=10),
        ),
        migrations.AddField(
            model_name='contest_submissiosn',
            name='solved',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='contest_submissiosn',
            name='status',
            field=models.CharField(default='solved', max_length=30),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='Contest_solutions',
        ),
    ]
