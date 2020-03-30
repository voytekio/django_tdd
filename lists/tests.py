import os
import pdb
import pytest
import sys

#os.environ.setdefault("DJANGO_SETTINGS_MODULE", "superlists.settings")
from django.test import TestCase
from django.urls import resolve
from django.http import HttpRequest
#import django
#django.setup()

from lists.views import home_page
from lists.models import Item

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

class ItemModelTest(TestCase):
    def test_saving_and_retrieving_items(self):
        first_item = Item()
        first_item.text = 'The first (ever) list item'
        first_item.save()

        second_item = Item()
        second_item.text = 'Item the second'
        second_item.save()

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.text, 'The first (ever) list item')
        self.assertEqual(second_saved_item.text, 'Item the second')

