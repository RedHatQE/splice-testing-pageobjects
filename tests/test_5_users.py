import webuitestcase
import tests as TESTS
from selenium_wrapper import SE
from pageobjects.users import UsersPage, DEFAULT_USER_NAME, user_experimental_ui_ctx
from pageobjects.login import login, logout

KATELLO = TESTS.ROLES.KATELLO

def setUpModule():
    '''Sanity test KATELLO role'''
    try: 
        KATELLO.url, KATELLO.username, KATELLO.password
    except AttributeError as e:
        raise unittest.SkipTest(e.message)

def tearDownModule():
    pass

class UsersPageTest(webuitestcase.WebuiTestCase):
    @classmethod
    def setUpClass(cls):
        SE.reset(url=KATELLO.url)
        SE.maximize_window()
        login(KATELLO.username, KATELLO.password)
        SE.get(KATELLO.url)
        cls.page = UsersPage()

    @classmethod
    def tearDownClass(cls):
        SE.get(KATELLO.url)
        logout()

    def test_01_access_default_user(self):
        self.page.get_user(DEFAULT_USER_NAME)

    def test_02_access_default_user_experimental_ui(self):
        self.page.get_user(DEFAULT_USER_NAME).experimental_ui

    def test_03_enable_default_user_experimental_ui(self):
        user = self.page.get_user(DEFAULT_USER_NAME)
        try:        
            self.assertTrue(user.experimental_ui.is_selected())
        except AssertionError:
            user.experimental_ui.click()
            self.assertTrue(user.experimental_ui.is_selected())

    def test_04_disable_default_user_experimental_ui(self):
        user = self.page.get_user(DEFAULT_USER_NAME)
        try:
            self.assertFalse(user.experimental_ui.is_selected())
        except AssertionError:
            user.experimental_ui.click()
            self.assertFalse(user.experimental_ui.is_selected())

    def test_05_default_user_experimental_ctx(self):
        with user_experimental_ui_ctx(DEFAULT_USER_NAME):
            self.assertTrue(self.page.get_user(DEFAULT_USER_NAME).experimental_ui.is_selected())
