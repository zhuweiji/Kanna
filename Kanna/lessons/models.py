from django.db import models

# Create your models here.


class Script(models.Model):
    """ """
    name = models.CharField(max_length=50)
    text = models.TextField()

    def __str__(self):
        return self.name


class ScriptKeywords(models.Model):
    class Meta:
        verbose_name_plural = 'ScriptKeywords'
    text = models.CharField(max_length=250)
    script = models.ForeignKey(Script, on_delete=models.CASCADE)



