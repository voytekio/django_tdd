import unittest
import pdb
import pytest
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException
from django.test import LiveServerTestCase

MAX_WAIT = 10

'''
@pytest.fixture()
def browser():
    print('\nFIXTURE SETUP(browser)')
    browser = webdriver.Firefox()
    yield browser
    print('\nFIXTURE TEARDOWN(browser)')
    time.sleep(2)
    browser.quit()
'''

#class Test_Webpage(unittest.TestCase, LiveServerTestCase):
class Test_Webpage(LiveServerTestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def wait_for_row_in_list_table(self, text):
        start_time = time.time()
        #pdb.set_trace()
        while True:
            try:
                table = self.browser.find_element_by_id('id_list_table')
                rows = table.find_elements_by_tag_name('tr')
                self.assertIn(text, [row.text for row in rows])
                return
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
                print('RETRYING: {}'.format(e.__class__))
                time.sleep(0.5)

    def test_can_start_a_list_and_retrieve_it_later(self):
        #pdb.set_trace()

        # we want to check the homepage
        self.browser.get(self.live_server_url)
        #self.browser.get('http://localhost:8000')

        # we want the page title and header mention to-do lists
        assert 'To-Do' in self.browser.title
        #self.assertIn ('To_Do', self.browser.title)

        # we should see header mention todo lists
        header_text = self.browser.find_element_by_tag_name('h1').text
        assert 'To-Do' in header_text

        # there must be an input form with a text box
        inputbox = self.browser.find_element_by_id('id_new_item')
        assert inputbox.get_attribute('placeholder') == 'Enter a to-do item'

        # we should be able to type into a text box
        inputbox.send_keys('Buy peacock feathers')

        # when you hit enter, the page updates and lists the item you entered
        inputbox.send_keys(Keys.ENTER)

        #table = browser.find_element_by_id('id_list_table')
        #rows = table.find_elements_by_tag_name('tr')
        #assert any(row.text == '1: Buy peacock feathers' for row in rows)
        #assert '1: Buy peacock feathers' in [row.text for row in rows]
        self.wait_for_row_in_list_table('1: Buy peacock feathers')
        #assert any(row.text == '1: Buy peacock feathers' for row in rows), f"New to-do item did not appear in table. Contents were:\n{table.text}"

        # there is still a text box inviting to add another item.
        # we'll add 'Use peacock feathers to make a fly' (being very methodical)
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Use peacock feathers to make a fly')
        # when you hit enter, the page updates and lists the item you entered
        inputbox.send_keys(Keys.ENTER)

        #assert any(row.text == '1: Buy peacock feathers' for row in rows)
        self.wait_for_row_in_list_table('1: Buy peacock feathers')
        self.wait_for_row_in_list_table('2: Use peacock feathers to make a fly')
        #assert '2: Use peacock feathers to make a fly' in [row.text for row in rows]

        # page should list as many items as the user puts int using the form
        assert 'nope' in 'Finish the test!'

        # there should be a unique URL for each list

        # at end of the test, the browser should quit


#if __name__ == '__main__':
#    unittest.main(warnings='ignore')
