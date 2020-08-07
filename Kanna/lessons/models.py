from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from django.conf import settings

# Create your models here.


class Topic(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Script(models.Model):
    """ """
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, null=True)
    text = models.TextField()
    flags = models.TextField(null=True)

    def __str__(self):
        return self.topic.name

    def get_absolute_url(self):
        return reverse('script_analysis', args=[str(self.pk)])


class Transcript(models.Model):
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, null=True)
    text = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.topic.name

    def get_absolute_url(self):
        return reverse('transcript_detail', args=[str(self.pk)])


class CustomUser(AbstractUser):
    pass


class AnalysisObj(models.Model):
    transcript = models.ForeignKey(Transcript, null=True, on_delete=models.CASCADE)
    script = models.ForeignKey(Script, null=True, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    score = models.IntegerField(null=True)

    def analyse(self):
        if not self.transcript or not self.script:
            return -1

        transcript_text = self.transcript.text
