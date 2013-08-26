import types
from contextlib import contextmanager
from selenium_wrapper import SE, restore_url
from basepageelement import InputPageElement
from menupageelement import MenuPageElement
from sampageobject import SamPageObject
from . import locators, pages
from events import appears
from nose.tools import assert_in

DEFAULT_USER_NAME='admin'

class UserMenu(MenuPageElement):
    _selector = staticmethod(lambda x: x.click())
    experimental_ui = InputPageElement(locators.users.user_menu.experimental_ui)

    def __init__(self, name):
        self._name = name
        #self._locator = appears(types.MethodType(lambda self: locators.users.user_menu.locator(self._name), self))
        self._locator = appears(types.MethodType(lambda self: locators.users.user_menu.locator(self._name), self))
        self._selected_locator = types.MethodType(lambda self: locators.users.user_menu.selected_locator(self._name), self)


class UsersPage(SamPageObject):
    _sub_url = pages.users.url

    def get_user(self, user_name):
        return UserMenu(user_name)

def user_experimental_ui_enable(name):
    '''return True if status changed'''
    ret = False
    with restore_url():
        users_page = UsersPage()
        user = users_page.get_user(name)
        if not user.experimental_ui.is_selected():
            user.experimental_ui.click()
            ret = True
    return ret

def user_experimental_ui_disable(name):
    '''return True if status changed'''
    ret = False
    with restore_url():
        users_page = UsersPage()
        user = users_page.get_user(name)
        if user.experimental_ui.is_selected():
            user.experimental_ui.click()
            ret = True
    return ret

@contextmanager
def user_experimental_ui_ctx(name):
    if user_experimental_ui_enable(name):
        try:
            with restore_url():
                yield
        finally:
            user_experimental_ui_disable(name) 
    else:
        with restore_url():
            yield
