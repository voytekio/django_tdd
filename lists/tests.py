import os
import pdb
import pytest
import sys

#os.environ.setdefault("DJANGO_SETTINGS_MODULE", "superlists.settings")
from django.test import TestCase
#import django
#django.setup()

from django.urls import resolve
from lists.views import home_page
from django.http import HttpRequest


# Create your tests here.

#class SmokeTest(TestCase):
class Test_HomePageTest(TestCase):
    def test_returns_desired_page_title(self):
        #pdb.set_trace()
        response_raw = self.client.get('/')
        #response_final = response_raw.content.decode('utf8')
        self.assertTemplateUsed(response_raw, 'home.html')

    def test_can_save_a_POST_request(self):
        response = self.client.post('/', data={'item_text': 'A new list item'})
        self.assertIn('A new list item', response.content.decode())
        self.assertTemplateUsed(response, 'home.html')

