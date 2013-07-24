#!/usr/bin/env python
import splice_webui_tests as SWT
import sys, unittest, re, time, os.path, logging, nose, selenium, namespace
from pageobjects.login import login, logout
import pageobjects.filters as filters
from selenium_wrapper import SE

KATELLO = SWT.ROLES.KATELLO

def setUpModule():
    '''Sanity test KATELLO role'''
    try: 
        KATELLO.url, KATELLO.username, KATELLO.password
    except AttributeError as e:
        raise unittest.SkipTest(e.message)


def tearDownModule():
    pass

class DefaultRhelFilterTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # reset SE driver 
        SE.reset(url=KATELLO.url)
        SE.maximize_window()
        login(KATELLO.username, KATELLO.password)

    def setUp(self):
        SE.get(KATELLO.url)
        self.filters = filters.Filters()
        self.report_filter = self.filters.get_filter(filters.REDHAT_DEFAULT_FILTER_NAME)
        self.verificationErrors = []

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
            
            

    def tearDown(self):
        self.assertEqual([], self.verificationErrors)

    @classmethod
    def tearDownClass(cls):
        SE.get(KATELLO.url)
        logout()

if __name__ == '__main__':
    nose.main()
