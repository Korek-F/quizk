# Generated by Django 3.0.6 on 2021-03-24 10:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0010_quiz_finished_sessions'),
    ]

    operations = [
        migrations.AddField(
            model_name='quiz',
            name='public',
            field=models.BooleanField(default=False),
        ),
    ]
