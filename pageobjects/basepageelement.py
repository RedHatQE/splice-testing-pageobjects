# Base Page Element
from selenium.common.exceptions import NoSuchElementException

class BasePageElement(object):
    locator = staticmethod(lambda : None)

    def __get__(self, obj, cls=None):
        return self.locator()

    def __delete__(self, obj):
        pass

class InputPageElement(BasePageElement):
    def __set__(self, obj, value):
        element = self.__get__(obj)
        element.clear()
        element.send_keys(value)

class ButtonPageElement(BasePageElement):
    pass
    #def click(self):
    #    self.locator().click()

class LinkPageElement(BasePageElement):
    def click(self):
        self.localtor().click()

class MenuPageElement(BasePageElement):
    '''element that requires selecting each time its attributes are accessed
    _locator: to find the menu instance on a page
    _selected_locator: to determine whether the menu instance has already been selected
    Note: all attributes not prefixed with '_' sign are preceeded with a self._select() call
    '''
    _locator = staticmethod(lambda : None)
    _selected_locator = staticmethod(lambda : None)
    _selector = staticmethod(lambda: None)

    def _select(self):
        '''if not selected, select'''
        try:
            # already selected?
            self._selected_locator()
        except NoSuchElementException as e:
            # nope --- click the menu and try again
            self._selector(self._locator())
            self._selected_locator()

    def __getattribute__(self, attrname):
        '''to access attributes, menu instance has to be selected
           all attributes that do not start with the '_' sign are preceeded with a _select() call
        '''
        if attrname.startswith('_'):
            return super(BasePageElement, self).__getattribute__(attrname)
        object.__getattribute__(self, '_select')()
        return object.__getattribute__(self, attrname)

