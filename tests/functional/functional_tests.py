from selenium import webdriver
import unittest

class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def test_can_start_a_list_and_retrieve_it_later(self):
        # we want to check the homepage
        self.browser.get('http://localhost:8000')

        # we want the page title and header mention to-do lists
        self.assertIn ('To_Do', self.browser.title)
        self.fail('Finish the test!')

        # there must be an input form with a text box

        # when you hit enter, the page updates and lists the item you entered

        # page should list as many items as the user puts int using the form

        # there should be a unique URL for each list

        # at end of the test, the browser should quit

if __name__ == '__main__':
    unittest.main(warnings='ignore')
