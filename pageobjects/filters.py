from selenium_wrapper import SE

from  . import locators, pages

from basepageelement import InputPageElement, ButtonPageElement, LinkPageElement, BasePageElement
from menupageelement import MenuPageElement
from basepageobject import BasePageObject
from selenium.common.exceptions import NoSuchElementException

import types, time, events

REDHAT_DEFAULT_FILTER_NAME=u'Red Hat Default Report'

class BaseFilterCloseLink(LinkPageElement):
    locator = staticmethod(events.appears(locators['filters.filter.base.close_link']))

class BaseFilterMenu(MenuPageElement):
    '''few common things between New Filter Menu and Filter Menu'''
    _selector = staticmethod(lambda x: x.click())
    close_link = BaseFilterCloseLink()

    def close(self):
        self.close_link.click()

class FilterRemoveLink(LinkPageElement):
    #locator = staticmethod(events.appears(locators['filters.filter.remove_link']))
    pass

class RunButton(BasePageElement):
    locator = staticmethod(events.appears(locators['filters.filter.run_button']))

class EncryptExport(InputPageElement):
    locator = staticmethod(events.appears(locators['filters.filter.encrypt_export']))

class SkipJsonExport(InputPageElement):
    locator = staticmethod(events.appears(locators['filters.filter.skip_json_export']))


class FilterMenu(BaseFilterMenu):
    '''a Filter meant to be selected on a page'''

    run_button = RunButton()
    remove_link = None
    encrypt_export = EncryptExport()
    skip_json_export = SkipJsonExport()

    def __init__(self, name):
        self._name = name
        # instance-level locator; monkeypatching for each filter
        self._locator = events.appears(types.MethodType(lambda self: locators['filters.filter'](self._name), self))
        self._selected_locator = types.MethodType(lambda self: locators['filters.filter.selected'](self._name), self)

    def run_report(self):
        self.run_button.click()

    def export_report(self):
        pass

    def remove(self):
        pass

class NewFilterNameInput(InputPageElement):
    locator = staticmethod(locators['filters.new.name'])

class NewFilterMenu(BaseFilterMenu):
    _locator = staticmethod(events.appears(locators['filters.new']))
    _selected_locator = staticmethod(locators['filters.new.selected'])

    filter_name = NewFilterNameInput() 

class Filters(BasePageObject):
    new_filter_menu = NewFilterMenu()

    def navigate(self):
        try:
            # already on the filters page?
            self.assertIn(pages['filters.url'], SE.current_url)
            self.assertIn(locators["filters.page_title"], SE)

        except AssertionError as e:
            SE.get(SE.current_url + pages['filters.url'])
            self.assertIn(pages['filters.url'], SE.current_url)
            self.assertIn(locators["filters.page_title"], SE)

    def __init__(self):
        self.navigate()

    def get_filter(self, filter_name):
        self.navigate()
        return FilterMenu(filter_name)
