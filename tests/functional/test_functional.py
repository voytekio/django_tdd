# import unittest
import os
import pdb
import pytest
import re
import time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException

import psutil
from subprocess import Popen, PIPE, check_output
import shlex

MAX_WAIT = 5

def run_cmd(cmd, blocking=True):
    #log.debug('cmd is: {0}'.format(cmd))
    cmdplus = shlex.split(cmd)

    if blocking:
        return check_output(cmdplus)
    else:
        process = Popen(cmdplus, stdout=PIPE)
        return process.pid

@pytest.fixture(scope='module')
def srv():
    print('\nFIXTURE SETUP(SRV)')
    cwd = os.getcwd()

    # delete and re-migrate the db
    res = run_cmd('rm {}/db.sqlite3'.format(cwd))
    res = run_cmd('python {}/manage.py migrate --noinput'.format(cwd))
    time.sleep(1)

    # start web server
    cmdline = 'python {}/manage.py runserver'.format(cwd)
    pid = run_cmd(cmdline, blocking=False)
    time.sleep(1)
    yield 0

    print('\nFIXTURE TEARDOWN(SRV)')
    parent = psutil.Process(pid)
    for child in parent.children():
        child.terminate()
    time.sleep(1)

@pytest.fixture()
def browser():
    print('\nFIXTURE SETUP(browser)')
    browser = webdriver.Firefox()
    #browser = 'foo'
    yield browser
    print('\nFIXTURE TEARDOWN(browser)')
    time.sleep(2)
    browser.quit()

@pytest.fixture()
def target_url():
    staging_server = os.environ.get('STAGING_SERVER') if os.environ.get('STAGING_SERVER') else 'localhost:8000'
    yield 'http://{}'.format(staging_server)


class Test_Webpage():
    def _wait_for_row_in_list_table(self, text, browser2):
        start_time = time.time()
        #pdb.set_trace()
        while True:
            try:
                table = browser2.find_element_by_id('id_list_table')
                rows = table.find_elements_by_tag_name('tr')
                assert text in [row.text for row in rows]
                return
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
                print('RETRYING: {}'.format(e.__class__))
                time.sleep(0.5)

    #@pytest.mark.skip(reason='temprarily exclude for perf reasons')
    def test_can_start_a_list_for_one_user(self, browser, srv, target_url):
        #pdb.set_trace()

        # we want to check the homepage
        browser.get(target_url)

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
        #pdb.set_trace()
        inputbox.send_keys('Buy peacock feathers')

        # when you hit enter, the page updates and lists the item you entered
        inputbox.send_keys(Keys.ENTER)

        self._wait_for_row_in_list_table('1: Buy peacock feathers', browser)
        #assert any(row.text == '1: Buy peacock feathers' for row in rows), f"New to-do item did not appear in table. Contents were:\n{table.text}"

        # there is still a text box inviting to add another item.
        # we'll add 'Use peacock feathers to make a fly' (being very methodical)
        inputbox = browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Use peacock feathers to make a fly')
        # when you hit enter, the page updates and lists the item you entered
        inputbox.send_keys(Keys.ENTER)

        self._wait_for_row_in_list_table('1: Buy peacock feathers', browser)
        self._wait_for_row_in_list_table('2: Use peacock feathers to make a fly', browser)

        # page should list as many items as the user puts int using the form

    #@pytest.mark.skip(reason='temprarily exclude for perf reasons')
    def test_user_gets_separate_url(self, srv, target_url):
        # edith starts a new to-do list

        #pdb.set_trace()

        # since we want to quit browser in the middle of tests
        # we cannot use a fixture, so we create all the browser 
        # objects ourselves here inside the test. 
        # as a result we don't benefit from fixture advantages
        # such as when exception happens during the test, then the
        # fixture is not cleaned
        browser3 = webdriver.Firefox()
        browser3.get(target_url)
        inputbox = browser3.find_element_by_id('id_new_item')
        inputbox.send_keys('Buy peacock feathers')
        inputbox.send_keys(Keys.ENTER)
        self._wait_for_row_in_list_table('1: Buy peacock feathers', browser3)
        time.sleep(1)

        # she notices that her list has a unique URL
        edith_list_url = browser3.current_url
        assert re.search(r'/lists/.+', edith_list_url)
        #self.assertRegex(edith_list_url, '/lists/.+')

        # now a new user, Francis, comes along to the site.
        browser3.quit()
        browser3 = webdriver.Firefox()
        browser3.get(target_url)

        page_text = browser3.find_element_by_tag_name('body').text
        assert 'Buy peackock feathers' not in page_text
        assert 'make a fly' not in page_text

        # francis starts a new list by entering a new item
        inputbox = browser3.find_element_by_id('id_new_item')
        inputbox.send_keys('Buy milk')
        inputbox.send_keys(Keys.ENTER)
        self._wait_for_row_in_list_table('1: Buy milk', browser3)

        # francis gets his own uniqure URL
        francis_list_url = browser3.current_url
        assert re.search(r'/lists/.+', francis_list_url)
        assert francis_list_url != edith_list_url

        page_text = browser3.find_element_by_tag_name('body').text
        assert 'Buy peackock feathers' not in page_text
        assert 'Buy milk' in page_text

        #assert 'Complete' in 'Finish the test!'
        browser3.quit()


    def test_layout_and_styling(self, browser, srv, target_url):
        # edith goes to the home page
        browser.get(target_url)
        #pdb.set_trace()
        win_size_x = 1024
        win_size_y = 768
        browser.set_window_size(win_size_x, win_size_y)
        inputbox = browser.find_element_by_id('id_new_item')

        # she notices the input box is nicely centered
        centered_x = win_size_x/2 - inputbox.size['width']/2
        assert int(abs(inputbox.location['x'] - centered_x)) < 10 # allow
        # for few pixels in case scrollbars show up

        # she starts a new list and sees the input is
        # nicely centered there too
        inputbox.send_keys('testing')
        inputbox.send_keys(Keys.ENTER)
        self._wait_for_row_in_list_table('1: testing', browser)
        inputbox_for_list = browser.find_element_by_id('id_new_item')

        actual_center = inputbox_for_list.location['x'] + inputbox_for_list.size['width']/2
        assert int(abs(actual_center - (win_size_x/2))) < 10

#if __name__ == '__main__':
#    unittest.main(warnings='ignore')
