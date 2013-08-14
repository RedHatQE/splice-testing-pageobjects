from basepageobject import BasePageObject
from basepageelement import LinkPageElement
from menupageelement import MenuPageElement
from events import appears
from . import locators


class OrganisationMenu(MenuPageElement):
    _locator = staticmethod(locators.sam_page.organisation_menu.locator)
    _selected_locator = staticmethod(locators.sam_page.organisation_menu.selected_locator)
    _selector = lambda x: x.click()

    @classmethod
    def get_organisation(name):
        '''return organisation link page element'''
        return LinkPageElement(appears(lambda: locators.sam_page.organisation_menu.organisation_link(name)))

    @classmethod
    def select_organisation(name):
        get_organisation(name).click()

class SamPageObject(BasePageObject):
    organisation_menu = OrganisationMenu()
