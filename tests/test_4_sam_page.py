import webuitestcase
import tests as TESTS
from selenium_wrapper import SE
from pageobjects import pages
from pageobjects.sampageobject import SamPageObject, organisation_ctx
from pageobjects.login import login, logout


KATELLO = TESTS.ROLES.KATELLO

class SamDashboardPageTestCase(webuitestcase.WebuiTestCase):
    @classmethod
    def setUpClass(cls):
        super(SamDashboardPageTestCase, cls).setUpClass()
        SE.get(KATELLO.url + '/' + pages.dashboard.url)
        cls.page = SamPageObject()

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

