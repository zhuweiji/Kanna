# Generated by Django 3.0.8 on 2020-08-16 08:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('lessons', '0008_auto_20200815_1841'),
    ]

    operations = [
        migrations.AddField(
            model_name='analysisobj',
            name='user',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]