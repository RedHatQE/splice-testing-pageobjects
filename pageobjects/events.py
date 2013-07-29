from selenium.webdriver.support.ui import WebDriverWait
from selenium_wrapper import SE

def appears(locator, timeout=5.0, message=""):
    '''a decorator to wait till the locator is able to locate the element
    i.e. till element appears. Assumes locator doesn't need the driver
    instance passed as attribute. Locators are supposed to use
    selenium_wrapper.SE instead.
    '''
    def waitnlocate(*args, **kvargs):
        e = WebDriverWait(SE, timeout=timeout).until(lambda x: locator(*args, **kvargs), message=message)
        WebDriverWait(SE, timeout=timeout).until(lambda x: e.is_displayed(), message=message)
        return e

    return waitnlocate
