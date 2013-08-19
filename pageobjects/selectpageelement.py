from containerpageelement import ContainerPageElement
from contextlib import contextmanager
from basepageelement import InputPageElement
from selenium.webdriver.support.select import Select

class SelectPageElement(ContainerPageElement):
    _locator = staticmethod(lambda: None)

    def get_option_element_by_value(self, value):
        return self._locator().find_element_by_xpath("//option[@value = '%s']" % value)

    def get_option_element_by_text(self, text):
        return self._locator().find_element_by_xpath("//option[text() = '%s']" % text)

    @property
    def select(self):
        '''the selenium idea of the Select'''
        return Select(self.element)

    @select.setter
    def select(self, values=[]):
        '''select given values; eg: ['val1', 'val2']'''
        select = Select(self.element)
        map(lambda x: select.select_by_visible_text(x), values)

@contextmanager
def select_ctx(locator, value_options=[], text_options=[]):
    '''locator: the Select page element locator (staticmethod)
       value_options: [(opt_name, opt_value), (opt_name, opt_value), ...]
       text_options: [(opt_name, opt_text), (opt_name, opt_value), ...]
       return: ParticularSelectPageElement class instance
    '''
    class ParticularSelectPageElement(SelectPageElement):
        _locator = locator

    for opt_name, opt_value in value_options:
        setattr(ParticularSelectPageElement, opt_name, InputPageElement(lambda: locator().find_element_by_xpath("//option[@value = '%s']" % opt_value)))
        
    for opt_name, opt_text in text_options:
        setattr(ParticularSelectPageElement, opt_name, InputPageElement(lambda: locator().find_element_by_xpath("//option[text() = '%s']" % opt_text)))

    yield ParticularSelectPageElement()

    del(ParticularSelectPageElement)
