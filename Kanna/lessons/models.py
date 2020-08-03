from django.db import models
from django.urls import reverse

# Create your models here.


class Script(models.Model):
    """ """
    name = models.CharField(max_length=50)
    text = models.TextField()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('script_analysis', args=[str(self.pk)])


class ScriptKeywords(models.Model):
    class Meta:
        verbose_name_plural = 'ScriptKeywords'
    text = models.CharField(max_length=250)
    script = models.ForeignKey(Script, on_delete=models.CASCADE)


class Transcript(models.Model):
    name = models.CharField(max_length=50)
    text = models.TextField()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('transcript_detail', args=[str(self.pk)])



