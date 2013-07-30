# Base Page Element

class BasePageElement(object):
    def __init__(self, locator=lambda: None):
        self.locator = locator

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

