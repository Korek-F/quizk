# Generated by Django 3.0.6 on 2021-03-25 10:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0013_auto_20210325_1054'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='quizzies',
            field=models.ManyToManyField(blank=True, related_name='_profile_quizzies_+', to='quiz.Quiz'),
        ),
    ]