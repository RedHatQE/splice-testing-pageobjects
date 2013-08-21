from basepageobject import BasePageObject
from basepageelement import LinkPageElement
from menupageelement import MenuPageElement
from events import appears
from . import locators
from contextlib import contextmanager
from selenium_wrapper import SE, restore_url


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
        return self._selected_locator().text.strip()

    @current_organisation.setter
    def current_organisation(self, name):
        '''selecting organization switches to dashboard
        restore original page here as the attribute is being accessed'''
        original_url = SE.current_url
        self.select_organisation(name)
        if SE.current_url != original_url:
            SE.get(original_url)

class SamPageObject(BasePageObject):
    organisation_menu = OrganisationMenu()

    def runTest(self):
        pass

def organization_set(name):
    with restore_url():
        sam_page = SamPageObject()
        sam_page.organisation_menu.current_organisation = name

def organisation_get():
    ret = None
    with restore_url():
        ret = SamPageObject().organisation_menu.current_organisation
    return ret

@contextmanager
def organisation_ctx(name):
    '''create a context in which organisation "name" is selected'''
    original_organisation = organisation_get()
    organization_set(name)
    with restore_url():
        yield
    if original_organisation == 'Select an Organization':
        # 'Select an Organization' means no org was originaly selected --- just leave what ever we've set
        return
    organization_set(original_organisation)
