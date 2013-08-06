from selenium_wrapper import SE

from  . import locators, pages

from basepageelement import InputPageElement, ButtonPageElement, LinkPageElement, BasePageElement
from menupageelement import MenuPageElement
from basepageobject import BasePageObject
from selenium.common.exceptions import NoSuchElementException
from selectpageelement import SelectPageElement

import types, time, events

REDHAT_DEFAULT_FILTER_NAME=u'Red Hat Default Report'

class BaseFilterMenu(MenuPageElement):
    '''few common things between New Filter Menu and Filter Menu'''
    _selector = staticmethod(lambda x: x.click())
    close_link = LinkPageElement(events.appears(locators.filters.base_menu.close_link))

    def close(self):
        self.close_link.click()

class FilterMenu(BaseFilterMenu):
    '''a Filter meant to be selected on a page'''

    run_button = ButtonPageElement(events.appears(locators.filters.menu.run_button))
    remove_link = LinkPageElement()
    encrypt_export = InputPageElement(events.appears(locators.filters.menu.encrypt_export))
    skip_json_export = InputPageElement(events.appears(locators.filters.menu.skip_json_export))

    def __init__(self, name):
        self._name = name
        # instance-level locator; monkeypatching for each filter
        self._locator = events.appears(types.MethodType(lambda self: locators.filters.menu.locator(self._name), self))
        self._selected_locator = types.MethodType(lambda self: locators.filters.menu.selected_locator(self._name), self)

    def run_report(self):
        self.run_button.click()

    def export_report(self):
        pass

    def remove(self):
        pass


class HoursField(SelectPageElement):
    _locator = staticmethod(locators.filters.hours_menu.hours_field.locator)

    option_blank = InputPageElement(locators.filters.hours_menu.hours_field.option_blank)
    option_4 = InputPageElement(locators.filters.hours_menu.hours_field.option_4)
    option_8 = InputPageElement(locators.filters.hours_menu.hours_field.option_8)
    option_24 = InputPageElement(locators.filters.hours_menu.hours_field.option_24)
    option_48 = InputPageElement(locators.filters.hours_menu.hours_field.option_48)


class HoursMenu(MenuPageElement):
    _locator = staticmethod(events.appears(locators.filters.hours_menu.locator))
    _selected_locator = staticmethod(locators.filters.hours_menu.selected_locator)
    _selector = staticmethod(lambda x: x.click())

    hours_field = HoursField()

class DateRangeMenu(MenuPageElement):
    _locator = staticmethod(events.appears(locators.filters.date_range_menu.locator))
    _selected_locator = staticmethod(locators.filters.date_range_menu.selected_locator)
    _selector = staticmethod(lambda x: x.click())

    start_date = InputPageElement(locators.filters.date_range_menu.start_date)
    end_date = InputPageElement(locators.filters.date_range_menu.end_date)

class StatusField(SelectPageElement):
    _locator = staticmethod(locators.filters.new_menu.status_field.locator)
    option_current = InputPageElement(locators.filters.new_menu.status_field.option_current)
    option_invalid = InputPageElement(locators.filters.new_menu.status_field.option_invalid)
    option_insufficient = InputPageElement(locators.filters.new_menu.status_field.option_insufficient)

class OrganizationsField(SelectPageElement):
    _locator = staticmethod(locators.filters.new_menu.organizations_field.locator)

class LifeCycleField(SelectPageElement):
    _locator = staticmethod(locators.filters.new_menu.lifecycle_field.locator)

    option_active = InputPageElement(locators.filters.new_menu.lifecycle_field.option_active)
    option_inactive = InputPageElement(locators.filters.new_menu.lifecycle_field.option_inactive)
    option_deleted = InputPageElement(locators.filters.new_menu.lifecycle_field.option_deleted)

class NewFilterMenu(BaseFilterMenu):
    _locator = staticmethod(events.appears(locators.filters.new_menu.locator))
    _selected_locator = staticmethod(locators.filters.new_menu.selected_locator)

    filter_name = InputPageElement(events.appears(locators.filters.new_menu.filter_name))
    filter_description = InputPageElement(events.appears(locators.filters.new_menu.filter_description))
    status_field = StatusField()
    organizations_field = OrganizationsField()
    hours_menu = HoursMenu()
    date_range_menu = DateRangeMenu()
    lifecycle_field = LifeCycleField()
    save_filter = InputPageElement(locators.filters.new_menu.save_filter)

class Filters(BasePageObject):
    new_filter_menu = NewFilterMenu()

    def navigate(self):
        try:
            # already on the filters page?
            self.assertIn(pages.filters.url, SE.current_url)
            self.assertIn(locators.filters.page_title, SE)

        except AssertionError as e:
            SE.get(SE.current_url + pages.filters.url)
            self.assertIn(pages.filters.url, SE.current_url)
            self.assertIn(locators.filters.page_title, SE)

    def __init__(self):
        self.navigate()

    def get_filter(self, filter_name):
        self.navigate()
        return FilterMenu(filter_name)
