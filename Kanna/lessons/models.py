from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from django.conf import settings
import math
# Create your models here.


class Topic(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Script(models.Model):
    """ """
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, null=True)
    text = models.TextField()
    flags = models.TextField()

    def __str__(self):
        return self.topic.name

    def get_absolute_url(self):
        return reverse('script_analysis', args=[str(self.pk)])

    def default_script_flags(self):
        return [0 for _ in self.text]

    def save(self, *args, **kwargs):
        if not self.flags:
            self.flags = self.default_script_flags()
        super().save(*args, **kwargs)

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
    # user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    score = models.IntegerField(null=True, blank=True)

    def analyse(self, buffer_len=20):
        if not self.transcript or not self.script:
            return None

        transcript_text = self.transcript.text
        script_text = self.script.text

        split_transcript = transcript_text.split()
        split_script = script_text.split()

        word_buffer = []
        filler_words_used = []
        keywords_hit = set()
        list_pointer = 0

        if len(split_transcript) >= len(split_script):
            ratio = math.ceil(len(split_transcript)/len(split_script))
            word_buffer += split_transcript[:buffer_len]
            for index, word in enumerate(split_transcript[buffer_len:]):
                word_buffer.append(word)
                if split_script[list_pointer] in word_buffer:
                    keywords_hit.add(split_script[list_pointer])
                if index % ratio == 0:
                    list_pointer += 1
                word_buffer.pop(0)
            print(keywords_hit)
        else:
            pass

