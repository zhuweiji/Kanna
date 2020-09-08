from django.test import TestCase
from .models import *
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "lessons.settings")


class TestAnalysisObj(TestCase):
    def setUp(self) -> None:
        pass

    def test_get_highlights(self):
        obj = AnalysisObj.objects.get(pk=7)
        print(obj.get_highlights())
        self.assertEqual(obj.get_highlights(),
                         [1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1])


