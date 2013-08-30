# Base Page Object
import nose
from selenium_wrapper import SE

class BasePageObject(object):
    '''asserting appropriate page is always navigated to'''

    _sub_url=''

    def _assertUrl(self):
        '''assert self._sub_url in SE.current_url'''
        nose.tools.assert_in(self._sub_url, SE.current_url)

    def _navigate(self):
        try:
            # already on the page?
            self._assertUrl()
        except AssertionError as e:
            SE.get(SE.current_url + self._sub_url)
            self._assertUrl()

    def __getattribute__(self, attrname):
        '''to access attributes, the page should be navigated to'''
        if attrname.startswith('_'):
            # prevent recursion by avoiding _<attrname> attributes
            return super(BasePageObject, self).__getattribute__(attrname)

        # navigate & access
        super(BasePageObject, self).__getattribute__('_navigate')()
        return super(BasePageObject, self).__getattribute__(attrname)

    def __setattr__(self, attrname, value):
        '''before setting an attribute, page should be navigated to'''
        if not attrname.startswith('_'):
            # don't navigate if accessing '_<attrname>' attributes
            self._navigate()
        try:
            # is the attr a descriptor?
            self.__class__.__dict__[attrname].__set__(self.__class__, value)
        except (KeyError, AttributeError) as e:
            self.__dict__[attrname] = value

    def __init__(self):
        self._navigate()


class RedirectingPageObject(BasePageObject):
    _sub_url = ''
    _check_url = ''

    def _assertUrl(self):
        '''assert self._check_url in SE.current_url'''
        nose.tools.assert_in(self._check_url, SE.current_url)
