#!/usr/bin/env python
import sys, unittest, re, time, os.path, logging, nose, selenium
import tests as TESTS
import pageobjects.filters as filters
from pageobjects.login import login, logout
from selenium_wrapper import SE

KATELLO = TESTS.ROLES.KATELLO

def setUpModule():
    '''Sanity test KATELLO role'''
    try: 
        KATELLO.url, KATELLO.username, KATELLO.password
    except AttributeError as e:
        raise unittest.SkipTest(e.message)


def tearDownModule():
    pass

class BaseFilterTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # reset SE driver 
        SE.reset(url=KATELLO.url)
        SE.maximize_window()
        login(KATELLO.username, KATELLO.password)

    def setUp(self):
        SE.get(KATELLO.url)
        self.filters = filters.Filters()
        self.verificationErrors = []

    def tearDown(self):
        self.assertEqual([], self.verificationErrors)

    @classmethod
    def tearDownClass(cls):
        SE.get(KATELLO.url)
        logout()


class DefaultRhelFilterTestCase(BaseFilterTestCase):
    def setUp(self):
        # navigate to the default filter
        super(DefaultRhelFilterTestCase, self).setUp()
        self.report_filter = self.filters.get_filter(filters.REDHAT_DEFAULT_FILTER_NAME)

    def test_1_open_reports_page(self):
        # TODO: assert something here ;)
        pass

    def test_2_select(self):
        self.report_filter

    def test_3_select_and_close(self):
        self.report_filter.close()

    def test_4_run(self):
        self.report_filter.run_report()
        
    def test_5_enable_encrypt_export(self):
        try:
            self.assertTrue(self.report_filter.encrypt_export.is_selected())
        except AssertionError:
            self.report_filter.encrypt_export.click()
            self.assertTrue(self.report_filter.encrypt_export.is_selected())

    def test_6_enable_skipping_json_export(self):
        try:
            self.assertTrue(self.report_filter.skip_json_export.is_selected())
        except AssertionError:
            self.report_filter.skip_json_export.click()
            self.assertTrue(self.report_filter.skip_json_export.is_selected())


class NewFilterTestCase(BaseFilterTestCase):

    def test_1_select(self):
        # navigate to new filter menu works
        # FIXME: assert something here
        self.filters.new_filter_menu.filter_name

    def test_2_close(self):
        self.filters.new_filter_menu.close()

    def test_3_insert_name(self):
        # check name can be inserted
        self.filters.new_filter_menu.filter_name = self.__class__.__name__ + "_filter"
        self.assertEqual(self.filters.new_filter_menu.filter_name.get_attribute("value"), self.__class__.__name__ + "_filter")

    def test_4_insert_description(self):
        # check description can be inserted
        self.filters.new_filter_menu.filter_description = self.__class__.__name__ + "_description"
        self.assertEqual(self.filters.new_filter_menu.filter_description.get_attribute("value"), self.__class__.__name__ + "_description")

    def test_5_select_hours_menu(self):
        self.filters.new_filter_menu.hours_menu
        self.assertTrue(self.filters.new_filter_menu.hours_menu.element.is_selected())

    def test_6_select_hours_field(self):
        self.filters.new_filter_menu.hours_menu.hours_field.element = '24'
        self.assertEqual(self.filters.new_filter_menu.hours_menu.hours_field.element.get_attribute('value'), '24')
    
if __name__ == '__main__':
    nose.main()
