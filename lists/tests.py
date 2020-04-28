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
    def test_uses_home_template(self):
        #pdb.set_trace()
        response_raw = self.client.get('/')
        #response_final = response_raw.content.decode('utf8')
        self.assertTemplateUsed(response_raw, 'home.html')


class ListViewTest(TestCase):
    def test_displays_all_items(self):
        Item.objects.create(text='itemy 1')
        Item.objects.create(text='itemy 2')

        response = self.client.get('/lists/the-only-list-in-the-world/')

        self.assertContains(response, 'itemy 1')
        self.assertContains(response, 'itemy 2')
        #self.assertIn('itemy 1', response.content.decode())
        #self.assertIn('itemy 2', response.content.decode())

    def test_uses_list_template(self):
        response = self.client.get('/lists/the-only-list-in-the-world/')
        self.assertTemplateUsed(response, 'list.html')


class NewListTest(TestCase):
    def test_can_save_a_POST_request(self):
        self.client.post('/lists/new', data={'item_text': 'A new list item'})

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new list item')

    def test_redirects_after_POST(self):
        response = self.client.post('/lists/new', data={'item_text': 'A new list item'})

        #self.assertEqual(response.status_code, 302)
        #self.assertEqual(response['location'], '/lists/the-only-list-in-the-world/')
        self.assertRedirects(response, '/lists/the-only-list-in-the-world/')


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

