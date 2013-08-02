class ContainerPageElement(object):
    _locator = staticmethod(lambda: None)

    @property
    def element(self):
        return self._locator()

    def __set__(self, obj, value):
        self.element.send_keys(value)

    def __delete__(self):
        pass
