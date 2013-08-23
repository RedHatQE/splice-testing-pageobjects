from basepageelement import BasePageElement
from menupageelement import MenuPageElement
from containerpageelement import ContainerPageElement
from events import appears
from . import locators, pages
from sampageobject import SamPageObject
from selenium_wrapper import SE
from nose.tools import assert_in
import re, filters

import types, time, events, report, namespace

class InvalidSubscriptions(ContainerPageElement):
    _locator = staticmethod(appears(locators.report.invalid_subscriptions.locator))
    count = BasePageElement(locators.report.invalid_subscriptions.count)

class InsufficientSubscriptions(ContainerPageElement):
    _locator = staticmethod(appears(locators.report.insufficient_subscriptions.locator))
    count = BasePageElement(locators.report.insufficient_subscriptions.count) 

class CurrentSubscriptions(ContainerPageElement):
    _locator = staticmethod(appears(locators.report.current_subscriptions.locator))
    count = BasePageElement(locators.report.current_subscriptions.count)

class InfoReportField(ContainerPageElement):
    _locator = lambda: None
    _substr = ""
    
    @property
    def field(self):
        return self.element.text[len(self._substr):]

class FilterNameField(InfoReportField):
    _locator = staticmethod(appears(locators.report.info_menu.filter_name))
    
    _substr = "Filter: "

class DescriptionField(InfoReportField):
    _locator = staticmethod(appears(locators.report.info_menu.filter_description))
    
    _substr = "Description: "
    
class SubscriptionField(InfoReportField):
    _locator = staticmethod(appears(locators.report.info_menu.subscription_status))
    
    _substr = "Subscription Status: "
    
class OrganizationsField(InfoReportField):
    _locator = staticmethod(appears(locators.report.info_menu.organizations))
    
    _substr = "Organizations: "
    
class HoursField(InfoReportField):
    _locator = staticmethod(appears(locators.report.info_menu.hours))
    
    _substr = "Hours: "
    
class LifecycleField(InfoReportField):
    _locator = staticmethod(appears(locators.report.info_menu.lifecycle_state))
    
    _substr = "LifeCycle State: "

class InfoReportMenu(MenuPageElement):
    _locator = staticmethod(events.appears(locators.report.info_menu.locator))
    _selected_locator = staticmethod(locators.report.info_menu.selected_locator)
    _selector = staticmethod(lambda x: x.click())
    
    filter_name = FilterNameField()
    filter_description = DescriptionField()
    subscription_status = SubscriptionField()
    organizations = OrganizationsField()
    hours = HoursField()
    lifecycle_state = LifecycleField()

class ReportPageObject(SamPageObject):
    _sub_url = None # to be figured out
    _filter_name = None
    header = BasePageElement(locators.report.header)
    invalid_subscriptions = InvalidSubscriptions()
    insufficient_subscriptions = InsufficientSubscriptions()
    current_subscriptions = CurrentSubscriptions()
    
    info_report = InfoReportMenu()

    def _navigate(self):
        '''Ensure this particular filter report is always selected by "guessing" the _sub_url here'''
        # FIXME: magic here
        if re.match(pages.reports.url_pattern, SE.current_url) is None:
            # not on the reports page -> create a report for this filter name
            filters.Filters().get_filter(self._filter_name).run_report()

        # https://sam.example.com/sam/splice_reports/filters/2/reports -> sam/splice_reports/filters/2/reports
        self._sub_url = '/'.join(SE.current_url.split('/')[3:])

        super(ReportPageObject, self)._navigate() 
        
    def __init__(self, filter_name):
        self._filter_name = filter_name
        super(ReportPageObject, self).__init__()

