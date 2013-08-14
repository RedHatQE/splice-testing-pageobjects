from basepageobject import BasePageObject
from basepageelement import LinkPageElement
from menupageelement import MenuPageElement
from events import appears
from . import locators
from contextlib import contextmanager


class OrganisationMenu(MenuPageElement):
    _locator = staticmethod(locators.sam_page.organisation_menu.locator)
    _selected_locator = staticmethod(locators.sam_page.organisation_menu.selected_locator)
    _selector = staticmethod(lambda x: x.click())

    @staticmethod
    def get_organisation(name):
        '''return organisation link page element'''
        return LinkPageElement(appears(lambda: locators.sam_page.organisation_menu.organisation_link(name)))

    @staticmethod
    def select_organisation(name):
        OrganisationMenu.get_organisation(name).click()

    @property
    def current_organisation(self):
        return self._locator().text.strip()

    @current_organisation.setter
    def current_organisation(self, name):
        self.select_organisation(name)

class SamPageObject(BasePageObject):
    organisation_menu = OrganisationMenu()

@contextmanager
def organisation_ctx(name):
    '''create a context in which organisation "name" is selected'''
    original_organisation = SamPageObject.organisation_menu.current_organisation
    SamPageObject.organisation_menu.current_organisation = name
    yield
    SamPageObject.organisation_menu.current_organisation = original_organisation
