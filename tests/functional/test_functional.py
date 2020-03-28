# import unittest
import pdb
import pytest
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


@pytest.fixture()
def browser():
    print('\nFIXTURE SETUP(browser)')
    browser = webdriver.Firefox()
    yield browser
    print('\nFIXTURE TEARDOWN(browser)')
    time.sleep(2)
    browser.quit()

class Test_Webpage():
    def test_can_start_a_list_and_retrieve_it_later(self, browser):
        #pdb.set_trace()

        # we want to check the homepage
        browser.get('http://localhost:8000')

        # we want the page title and header mention to-do lists
        assert 'To-Do' in browser.title
        #time.sleep(5)
        #self.assertIn ('To_Do', self.browser.title)

        # we should see header mention todo lists
        header_text = browser.find_element_by_tag_name('h1').text
        assert 'To-Do' in header_text

        # there must be an input form with a text box
        inputbox = browser.find_element_by_id('id_new_item')
        assert inputbox.get_attribute('placeholder') == 'Enter a to-do item'

        # we should be able to type into a text box
        inputbox.send_keys('Buy peacock feathers')

        # when you hit enter, the page updates and lists the item you entered
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)

        table = browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        assert any(row.text == '1: Buy peacock feathers' for row in rows)

        # there is still a text box inviting to add another item.
        # we'll add 'Use peacock feathers to make a fly' (being very methodical)
        assert 'nope' in 'Finish the test!'

        # page should list as many items as the user puts int using the form

        # there should be a unique URL for each list

        # at end of the test, the browser should quit


#if __name__ == '__main__':
#    unittest.main(warnings='ignore')
