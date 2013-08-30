from selenium_wrapper import SE, restore_url
from  . import locators, pages, events
from basepageelement import InputPageElement, ButtonPageElement, LinkPageElement
from basepageobject import RedirectingPageObject
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from nose.tools import assert_in, assert_raises

from contextlib import contextmanager

class LoginPageObject(RedirectingPageObject):
    _sub_url = pages.login.url

    username = InputPageElement(locators.login.username)
    password = InputPageElement(locators.login.password)
    default_org_link = LinkPageElement(events.appears(locators.login.default_org_link))
    submit_button = ButtonPageElement(locators.login.submit)

    def _assertUrl(self):
        # overriding to handle signo--non-signo redirects
        if not pages.login.check_url in SE.current_url and not pages.login.signo.url in SE.current_url:
            raise AssertionError("page %s not loaded" % self.__class__.__name__)    

    def submit(self):
        if pages.login.signo.url in SE.current_url:
            # using signo
            self.submit_button.click()
        else:
            self.submit_button.click()
            # non-signo: selecting the default org required
            # it also kinda asserts log-in succeeded
            self.default_org_link.click()
        # assumes successful log-in by the dashboard page navigation
        assert_in(pages.dashboard.url, SE.current_url)

class LogoutPageObject(RedirectingPageObject):
    _sub_url = pages.logout.url

    def _assertUrl(self):
        # overriding to handle signo--non-signo redirects
        try:
            events.appears(locators.login.submit, timeout=1) in SE
        except TimeoutException:
            raise AssertionError("page %s not loaded" % self.__class__.__name__)
       
    def submit(self):
        # calling is preceeded by _navigate-ing self; just pass
        pass

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
    try:
        with restore_url():
            yield
    finally:
        logout()
