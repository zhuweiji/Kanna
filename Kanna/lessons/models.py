from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from django.conf import settings
import math
import re
# Create your models here.


class Topic(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Script(models.Model):
    """ """
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, null=True)
    text = models.TextField()
    _flags = models.TextField(blank=True)

    def __str__(self):
        return self.topic.name

    def get_absolute_url(self):
        return reverse('script_analysis', args=[str(self.pk)])

    def default_script_flags(self):
        return [0 for _ in self.text.split()]

    @property
    def flags(self):
        val = self._flags.strip('][').split(', ')
        return val

    @flags.setter
    def flags(self, value):
        self._flags = value

    def clean(self):
        original_text = self.text
        self.text = re.sub(r'[^\x00-\x7F]+', ' ', original_text)
        if self.text != original_text:
            with open('log.txt', 'a+') as f:
                f.write('Script {self} text cleaned from\n{original_text}\nto\n{self.text}')

    def save(self, *args, **kwargs):
        if not self._flags:
            self._flags = str(self.default_script_flags())
        super().save(*args, **kwargs)


class Transcript(models.Model):
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, null=True)
    text = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.topic.name)

    def get_absolute_url(self):
        return reverse('transcript_detail', args=[str(self.pk)])

    def get_cleaned_text(self):
        original_text = self.text
        return re.sub(r"[^a-zA-Z' ]", ' ', original_text)


class CustomUser(AbstractUser):
    pass


class AnalysisObj(models.Model):
    transcript = models.ForeignKey(Transcript, null=True, on_delete=models.CASCADE)
    script = models.ForeignKey(Script, null=True, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    score = models.IntegerField(null=True, blank=True)

    def get_absolute_url(self):
        return reverse('analyse_detail', args=[str(self.pk)])

    def get_highlights(self) -> list:
        """ parses out highlighted key phrases in the script"""
        text = self.script.text.split()
        flags = self.script.flags
        highlights = []
        phrase = ""
        for index, word in enumerate(text):
            if flags[index] == '1':
                phrase += word + ' '
            else:
                if phrase:
                    highlights.append(phrase)
                    phrase = ""
        print('\n\n\n ----------------------- HIGHLIGHTS ------------------')
        print(highlights)
        print('\n\n\n ------------------------------------------------------')
        return highlights

    def analyse_highlight(self, highlight: str) -> float:
        """ analyse a key phrase; checks for presence of whole phrase in phrases that are 3 words or less
            otherwise it searches the whole transcript for the phrase until it can match at least half the phrase"""
        transcript = self.transcript.get_cleaned_text().split()
        highlight = highlight.split()
        print('\n\n\n -------------------------TRANSCRIPT -------------------')
        print(transcript)
        print('\n\n\n------------------------------------------------------')
        print('\n\n\n-------------------- SPLIT HIGHLIGHTS -------------------')
        print(highlight)
        print('\n\n\n---------------------------------------------------')
        score = 0

        if 1 <= len(highlight) <= 3:
            return 1 if all(i in transcript for i in highlight) else 0

        all_starts = [index for index, word in enumerate(transcript) if word == highlight[0]]
        print('\n\n\n--------------------------- ALL STARTS-----------------------------')
        print(all_starts)
        print('\n\n\n----------------------------------------------------------')
        for start in all_starts:
            score = 0
            for index, word in enumerate(highlight):
                if transcript[start+index] == word:
                    score += 1
            if score >= len(highlight)/2:
                return score/len(highlight)
        return score/len(highlight)

    def full_analysis(self):
        score = 0
        last_pos = 0

        highlights = self.get_highlights()
        print(highlights)
        for highlight in highlights:
            score += self.analyse_highlight(highlight)
            print('\n\n\n---------------------SCORE-------------------')
            print(score)
            print('\n\n\n----------------------------------------------')
        self.score = score/len(highlights) * 100

    def naive_analysis(self, buffer_len=20):
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
            print('\n\n\n------------------------KEYWORD HIT----------------------')
            print(keywords_hit)
            print('\n\n\n------------------------------------------------------')
        else:
            pass

