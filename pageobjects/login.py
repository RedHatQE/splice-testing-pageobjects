from selenium_wrapper import SE
from  . import locators, pages
from basepageelement import InputPageElement, ButtonPageElement, LinkPageElement
from basepageobject import BasePageObject
from selenium.common.exceptions import NoSuchElementException

from contextlib import contextmanager

class UsernameElement(InputPageElement):
    locator = staticmethod(locators["login.username"])

class PasswordElement(InputPageElement):
    locator = staticmethod(locators["login.password"])

class SubmitButton(ButtonPageElement):
    locator = staticmethod(locators["login.submit"])

class LogoutLink(LinkPageElement):
    locator = staticmethod(locators["login.logout"])

class LoginPageObject(BasePageObject):
    username = UsernameElement()
    password = PasswordElement()
    submit_button = SubmitButton()

    def __init__(self):
        try:
            # are we already there?
            self.assertEqual(pages['login.title'], SE.title)
        except AssertionError as e:
            SE.get(SE.current_url + pages['login.url'])
            self.assertEqual(pages['login.title'], SE.title)

    def submit(self):
        # assumes successful log-in by the Sign "Out link" presence
        self.submit_button.click()
        SE.refresh()
        self.assertIn(locators['login.logout'], SE)

class LogoutPageObject(BasePageObject):
    logout_link = LogoutLink()
    def __init__(self):
        try:
            self.assertEqual(pages['login.title'], SE.title)
        except AssertionError as e:
            SE.get(SE.current_url + pages['login.url'])
            self.assertEqual(pages['login.title'], SE.title)

    def submit(self):
        self.logout_link.click()
        self.assertIn(locators["login.logout_notice"], SE)

def login(username, password):
    '''Performs a log in'''
    login_object = LoginPageObject()
    login_object.username = username
    login_object.password = password
    login_object.submit()

def logout():
    '''Performs a log out'''
    logout_object = LogoutPageObject()
    logout_object.submit()

@contextmanager
def login_ctx(url, username, password):
    '''log-in + yield + log-out; SE.current_url restored'''
    original_url = SE.current_url
    SE.get(url)
    login(username, password)
    yield
    SE.get(url)
    logout()
    SE.get(original_url)
