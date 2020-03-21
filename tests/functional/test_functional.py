# import unittest
import pdb
import pytest
import time


@pytest.fixture()
def browser():
    print('\nFIXTURE SETUP(browser)')
    from selenium import webdriver
    browser = webdriver.Firefox()
    yield browser
    print('\nFIXTURE TEARDOWN(browser)')
    #time.sleep(1)
    browser.quit()

class Test_Webpage():
    def test_can_start_a_list_and_retrieve_it_later(self, browser):
        #pdb.set_trace()

        # we want to check the homepage
        browser.get('http://localhost:8000')

        # we want the page title and header mention to-do lists
        assert 'To-Do' in browser.title
        #self.assertIn ('To_Do', self.browser.title)
        assert 'nope' in 'Finish the test!'

        # there must be an input form with a text box

        # when you hit enter, the page updates and lists the item you entered

        # page should list as many items as the user puts int using the form

        # there should be a unique URL for each list

        # at end of the test, the browser should quit


#if __name__ == '__main__':
#    unittest.main(warnings='ignore')
