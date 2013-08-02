class ContainerPageElement(object):
    _locator = staticmethod(lambda: None)

    @property
    def element(self):
        return self._locator()

    @element.setter
    def element(self, value):
        self.element.send_keys(value)

    def __set__(self, obj, value):
        self.element.send_keys(value)

    def __delete__(self):
        pass
