# Generated by Django 3.0.8 on 2020-08-14 09:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lessons', '0006_auto_20200812_1525'),
    ]

    operations = [
        migrations.RenameField(
            model_name='script',
            old_name='flags',
            new_name='_flags',
        ),
    ]
