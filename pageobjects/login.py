from selenium_wrapper import SE, restore_url
from  . import locators, pages
from basepageelement import InputPageElement, ButtonPageElement, LinkPageElement
from basepageobject import BasePageObject
from selenium.common.exceptions import NoSuchElementException
from nose.tools import assert_in, assert_raises

from contextlib import contextmanager

class LoginPageObject(BasePageObject):
    _sub_url = pages.login.url
    username = InputPageElement(locators.login.username)
    password = InputPageElement(locators.login.password)
    submit_button = ButtonPageElement(locators.login.submit)

    
    def submit(self):
        # assumes successful log-in by the Sign "Out link" presence
        self.submit_button.click()
        SE.refresh()
        assert_in(locators.login.logout, SE)

class LogoutPageObject(BasePageObject):
    _sub_url = pages.logout.url
    logout_link = LinkPageElement(locators.login.logout)

 
    def submit(self):
        self.logout_link.click()
        # assert the logout link isn't there anymore
        with assert_raises(NoSuchElementException):
            self.logout_link

def login(username, password):
    '''Performs a log in'''
    with restore_url():
        login_object = LoginPageObject()
        login_object.username = username
        login_object.password = password
        login_object.submit()

def logout():
    '''Performs a log out'''
    with restore_url():
        logout_object = LogoutPageObject()
        logout_object.submit()

@contextmanager
def login_ctx(username, password):
    '''log-in + yield + log-out; SE.current_url restored'''
    login(username, password)
    with restore_url():
        yield
    logout()
