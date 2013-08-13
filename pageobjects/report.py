from basepageobject import BasePageObject
from basepageelement import BasePageElement
from containerpageelement import ContainerPageElement
from events import appears
from . import locators, pages

class InvalidSubscriptions(ContainerPageElement):
    _locator = staticmethod(appears(locators.report.invalid_subscriptions.locator))
    count = BasePageElement(locators.report.insufficient_subscriptions.count)

class InsufficientSubscriptions(ContainerPageElement):
    _locator = staticmethod(appears(locators.report.insufficient_subscriptions.locator))
    count = BasePageElement(locators.report.insufficient_subscriptions.count) 

class CurrentSubscriptions(ContainerPageElement):
    _locator = staticmethod(appears(locators.report.current_subscriptions.locator))
    count = BasePageElement(locators.report.current_subscriptions.count)


class ReportPageObject(BasePageObject):
    header = BasePageElement(locators.report.header)
    invalid_subscriptions = InvalidSubscriptions()
    insufficient_subscriptions = InsufficientSubscriptions()
    current_subscriptions = CurrentSubscriptions()

    def __init__(self, filter_name=""):
        self.filter_name = filter_name


