from django.db import models
from django.urls import reverse

# Create your models here.


class Script(models.Model):
    """ """
    name = models.CharField(max_length=50)
    text = models.TextField()
    flags = models.TextField(null=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('script_analysis', args=[str(self.pk)])


class Transcript(models.Model):
    name = models.CharField(max_length=50)
    text = models.TextField()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('transcript_detail', args=[str(self.pk)])


class AnalysisObj(models.Model):
    transcript = models.ForeignKey(Transcript, null=True, on_delete=models.CASCADE)
    script = models.ForeignKey(Script, null=True, on_delete=models.CASCADE)

    def analyse(self):
        if not self.transcript or not self.script:
            return -1

        transcript_text = self.transcript.text


