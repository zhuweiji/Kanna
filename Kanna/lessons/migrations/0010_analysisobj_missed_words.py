# Generated by Django 3.0.8 on 2020-09-06 16:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lessons', '0009_analysisobj_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='analysisobj',
            name='missed_words',
            field=models.TextField(blank=True, null=True),
        ),
    ]
