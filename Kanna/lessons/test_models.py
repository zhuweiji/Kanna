from unittest import TestCase
from .models import *

class TestAnalysisObj(TestCase):
    def setUp(self) -> None:
        pass

    def test_get_highlights(self):
        obj = AnalysisObj.objects.get(pk=6)
        self.assertEqual(obj.get_highlights(),)

