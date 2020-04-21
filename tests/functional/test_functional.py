# import unittest
import pdb
import pytest
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from subprocess import Popen, PIPE
import shlex

def run_cmd(cmd, returnstring):
    #log.debug('cmd is: {0}'.format(cmd))
    #log.debug('returnstring is: {0}'.format(returnstring))
    cmdplus = shlex.split(cmd)
    #pdb.set_trace()
    try:
        process = Popen(cmdplus, stdout=PIPE)
        #cmdoutput = process.communicate()
    except OSError as err:
        log.error('OS Exception occurred: {}'.format(err))
        return 1
    #exitcode = process.wait()
    #log.debug('cmd output is: {0}'.format(cmdoutput))
    # log.debug('exitcode is: {0}'.format(exitcode))
    return 0
    '''
    if returnstring in str(cmdoutput[0]):
        log.debug('Found success_string in return')
        return 0
    else:
        log.debug('Unable to find success_string "{}" in cmd output'.format(returnstring))
        return 1
    '''

@pytest.fixture()
def srv():
    print('\nFIXTURE SETUP(SRV)')
    #pdb.set_trace()
    cmdline = '/Users/vkrudysz/venvs/tddbook/bin/python /Users/vkrudysz/code/django_tdd/manage.py runserver'
    foo = run_cmd(cmdline, 'foo_string')
    time.sleep(2)

    #browser = webdriver.Firefox()
    yield 0
    print('\nFIXTURE TEARDOWN(SRV)')
    time.sleep(2)
    #browser.quit()

@pytest.fixture()
def browser():
    print('\nFIXTURE SETUP(browser)')
    browser = webdriver.Firefox()
    #browser = 'foo'
    yield browser
    print('\nFIXTURE TEARDOWN(browser)')
    time.sleep(2)
    browser.quit()

class Test_Webpage():
    def assert_in_html_table(self, text, browser2):
        #pdb.set_trace()
        table = browser2.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        assert text in [row.text for row in rows]

    def test_can_start_a_list_and_retrieve_it_later(self, browser, srv):
        #pdb.set_trace()

        # we want to check the homepage
        browser.get('http://localhost:8000')

        # we want the page title and header mention to-do lists
        assert 'To-Do' in browser.title
        #self.assertIn ('To_Do', self.browser.title)

        # we should see header mention todo lists
        header_text = browser.find_element_by_tag_name('h1').text
        assert 'To-Do' in header_text

        # there must be an input form with a text box
        inputbox = browser.find_element_by_id('id_new_item')
        assert inputbox.get_attribute('placeholder') == 'Enter a to-do item'

        # we should be able to type into a text box
        time.sleep(1)
        inputbox.send_keys('Buy peacock feathers')

        # when you hit enter, the page updates and lists the item you entered
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)

        #table = browser.find_element_by_id('id_list_table')
        #rows = table.find_elements_by_tag_name('tr')
        #assert any(row.text == '1: Buy peacock feathers' for row in rows)
        #assert '1: Buy peacock feathers' in [row.text for row in rows]
        self.assert_in_html_table('1: Buy peacock feathers', browser)
        #assert any(row.text == '1: Buy peacock feathers' for row in rows), f"New to-do item did not appear in table. Contents were:\n{table.text}"

        # there is still a text box inviting to add another item.
        # we'll add 'Use peacock feathers to make a fly' (being very methodical)
        inputbox = browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Use peacock feathers to make a fly')
        # when you hit enter, the page updates and lists the item you entered
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)

        #assert any(row.text == '1: Buy peacock feathers' for row in rows)
        self.assert_in_html_table('1: Buy peacock feathers', browser)
        self.assert_in_html_table('2: Use peacock feathers to make a fly', browser)
        #assert '2: Use peacock feathers to make a fly' in [row.text for row in rows]

        # page should list as many items as the user puts int using the form
        assert 'nope' in 'Finish the test!'

        # there should be a unique URL for each list

        # at end of the test, the browser should quit


#if __name__ == '__main__':
#    unittest.main(warnings='ignore')
