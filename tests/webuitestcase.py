import unittest
import tests as TESTS
from selenium_wrapper import SE, restore_url
from pageobjects.users import user_experimental_ui_enable, user_experimental_ui_disable 
from pageobjects.login import login, logout

KATELLO = TESTS.ROLES.KATELLO

def setUpModule():
    '''Sanity test KATELLO role'''
    try: 
        KATELLO.url, KATELLO.username, KATELLO.password
    except AttributeError as e:
        raise unittest.SkipTest(e.message)

def tearDownModule():
    pass

class WebuiTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        '''all these test cases require experimental web ui enabled and user logged in'''
        SE.reset(url=KATELLO.url)
        SE.maximize_window()
        with restore_url():
            login(KATELLO.username, KATELLO.password)
        with restore_url():
            cls.disable_experimental_web_ui = user_experimental_ui_enable(KATELLO.username)

    @classmethod
    def tearDownClass(cls):
        '''restore experimental web ui setting and logout'''
        SE.get(KATELLO.url)
        if cls.disable_experimental_web_ui:
            with restore_url():
                user_experimental_ui_disable(KATELLO.username)
        logout()

    def assertElementValue(self, element, value):
        '''assert an WebUI element get_attribute('value') equals value'''
        self.assertEqual(element.get_attribute('value'), value)
