import os
import pdb
import pytest
import sys

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "superlists.settings")
from django.test import TestCase

from django.urls import resolve
from lists.views import home_page
from django.http import HttpRequest


# Create your tests here.

#class SmokeTest(TestCase):
class Test_HomePageTest(TestCase):
    def test_root_url_resolves_to_home_page_view(self):
        found = resolve('/')
        assert found.func == home_page

    def test_returns_desired_page_title(self):
        request = HttpRequest()
        response_raw = home_page(request)
        response_final = response_raw.content.decode('utf8')

        assert response_final.startswith('<html>')
        assert '<title>To-Do lists</title>' in response_final
        assert response_final.endswith('</html>')

'''
@pytest.fixture() #, autouse=True)
def djan():
    print('DJAN FIXTURE SETUP')
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "superlists.settings")
    from django.test import TestCase
    yield TestCase
    print('DJAN FIXTURE TEARDOWN')
'''
