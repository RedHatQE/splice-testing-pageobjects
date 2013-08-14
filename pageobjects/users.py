import types
from selenium_wrapper import SE
from basepageelement import InputPageElement
from menupageelement import MenuPageElement
from sampageobject import SamPageObject
from . import locators, pages
from events import appears

DEFAULT_USER_NAME='admin'

class UserMenu(MenuPageElement):
    _selector = staticmethod(lambda x: x.click())
    experimental_ui = InputPageElement(locators.users.user_menu.experimental_ui)

    def __init__(self, name):
        self._name = name
        #self._locator = appears(types.MethodType(lambda self: locators.users.user_menu.locator(self._name), self))
        self._locator = types.MethodType(lambda self: locators.users.user_menu.locator(self._name), self)
        self._selected_locator = types.MethodType(lambda self: locators.users.user_menu.selected_locator(self._name), self)


class UsersPage(SamPageObject):
    def navigate(self):
        try:
            # already on the users page?
            self.assertIn(pages.users.url, SE.current_url)
        except AssertionError as e:
            SE.get(SE.current_url + pages.users.url)
            self.assertIn(pages.users.url, SE.current_url)

    def get_user(self, user_name):
        self.navigate()
        return UserMenu(user_name)
