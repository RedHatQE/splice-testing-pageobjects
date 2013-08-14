import webuitestcase
import tests as TESTS
from selenium_wrapper import SE
from pageobjects import pages
from pageobjects.sampageobject import SamPageObject, organisation_ctx
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

class SamDashboardPageTestCase(webuitestcase.WebuiTestCase):
    @classmethod
    def setUpClass(cls):
        SE.reset(url=KATELLO.url)
        SE.maximize_window()
        login(KATELLO.username, KATELLO.password)
        SE.get(KATELLO.url + '/' + pages.dashboard.url)
        cls.page = SamPageObject()

    @classmethod
    def tearDownClass(cls):
        SE.get(KATELLO.url)
        logout()

    def test_01_access_organisation_menu(self):
        self.page.organisation_menu

    def test_02_access_current_organisation(self):
        self.page.organisation_menu.current_organisation

    def test_03_set_acme_corp_organisation(self):
        self.page.organisation_menu.current_organisation = 'ACME_Corporation'
        self.assertEqual(self.page.organisation_menu.current_organisation, 'ACME_Corporation')

    def test_04_set_acme_corp_organisation_ctx(self):
        with organisation_ctx('ACME_Corporation'):
            self.assertEqual(self.page.organisation_menu.current_organisation, 'ACME_Corporation')

