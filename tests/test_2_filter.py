#!/usr/bin/env python
import sys, unittest, re, time, os.path, logging, nose, selenium, webuitestcase
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

class BaseFilterTestCase(webuitestcase.WebuiTestCase):
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

    def test_01_select(self):
        # navigate to new filter menu works
        # FIXME: assert something here
        self.filters.new_filter_menu.filter_name

    def test_02_close(self):
        self.filters.new_filter_menu.close()

    def test_03_insert_name(self):
        # check name can be inserted
        self.filters.new_filter_menu.filter_name = self.__class__.__name__ + "_filter"
        self.assertElementValue(self.filters.new_filter_menu.filter_name, self.__class__.__name__ + "_filter")

    def test_04_insert_description(self):
        # check description can be inserted
        self.filters.new_filter_menu.filter_description = self.__class__.__name__ + "_description"
        self.assertElementValue(self.filters.new_filter_menu.filter_description, self.__class__.__name__ + "_description")

    def test_05_select_hours_menu(self):
        self.filters.new_filter_menu.hours_menu
        self.assertTrue(self.filters.new_filter_menu.hours_menu.element.is_selected())

    def test_06_select_hours_field(self):
        self.filters.new_filter_menu.hours_menu.hours_field.element = '24'
        self.assertElementValue(self.filters.new_filter_menu.hours_menu.hours_field.element, '24')

    def test_07_select_hours_field_option(self):
        self.filters.new_filter_menu.hours_menu.hours_field.option_8.click()
        self.assertElementValue(self.filters.new_filter_menu.hours_menu.hours_field.element, '8')

    def test_08_select_current_status_option(self):
        self.filters.new_filter_menu.status_field.option_current.click()
        self.assertTrue(self.filters.new_filter_menu.status_field.option_current.is_selected())

    def test_09_select_invalid_status_option(self):
        self.filters.new_filter_menu.status_field.option_invalid.click()
        self.assertTrue(self.filters.new_filter_menu.status_field.option_invalid.is_selected())

    def test_10_select_insufficient_status_option(self):
        self.filters.new_filter_menu.status_field.option_insufficient.click()
        self.assertTrue(self.filters.new_filter_menu.status_field.option_insufficient.is_selected())

    def test_11_select_default_organization_option(self):
        self.filters.new_filter_menu.organizations_field = "ACME_Corporation"
        option_element = self.filters.new_filter_menu.organizations_field.get_option_element_by_text("ACME_Corporation")
        self.assertTrue(option_element.is_selected())

    def test_12_select_ctx_default_organization_option(self):
        from pageobjects.selectpageelement import select_ctx
        with select_ctx(self.filters.new_filter_menu.organizations_field._locator, text_options=[('acme_corp', 'ACME_Corporation')]) as select_page_element:
            select_page_element.acme_corp.click()
            self.assertTrue(select_page_element.acme_corp.is_selected())

    def test_13_selenium_select_default_organization_option(self):
        from selenium.webdriver.support.select import Select
        select_organization = Select(self.filters.new_filter_menu.organizations_field.element)
        select_organization.deselect_all()
        select_organization.select_by_visible_text("ACME_Corporation")
        selected_option_value = select_organization.first_selected_option.get_attribute('value')
        self.assertElementValue(self.filters.new_filter_menu.organizations_field.element, selected_option_value)
        self.assertEqual("ACME_Corporation", self.filters.new_filter_menu.organizations_field.element.text)

    def test_14_select_active_lifecycle_option(self):
        self.filters.new_filter_menu.lifecycle_field.option_active.click()
        self.assertTrue(self.filters.new_filter_menu.lifecycle_field.option_active.is_selected())

    def test_15_select_inactive_lifecycle_option(self):
        self.filters.new_filter_menu.lifecycle_field.option_inactive.click()
        self.assertTrue(self.filters.new_filter_menu.lifecycle_field.option_inactive.is_selected())

    def test_16_select_deleted_lifecycle_option(self):
        self.filters.new_filter_menu.lifecycle_field.option_deleted.click()
        self.assertTrue(self.filters.new_filter_menu.lifecycle_field.option_deleted.is_selected())

    def test_17_has_save_filter_button(self):
        self.filters.new_filter_menu.save_filter

    def test_18_select_date_range_menu(self):
        self.filters.new_filter_menu.date_range_menu
        self.assertTrue(self.filters.new_filter_menu.date_range_menu.element.is_selected())

    def test_19_set_start_date(self):
        import datetime
        # FIXME the WebUI might have a bug here: it doesn't accept iso formated date
        today = datetime.date.today()
        today_str = "%02d/%02d/%d" % (today.month, today.day, today.year)
        self.filters.new_filter_menu.date_range_menu.start_date = today_str
        self.assertElementValue(self.filters.new_filter_menu.date_range_menu.start_date, today_str)

    def test_20_set_end_date(self):
        import datetime
        # FIXME the WebUI might have a bug here: it doesn't accept iso formated date
        today = datetime.date.today()
        today_str = "%02d/%02d/%d" % (today.month, today.day, today.year)
        self.filters.new_filter_menu.date_range_menu.end_date = today_str
        self.assertElementValue(self.filters.new_filter_menu.date_range_menu.end_date, today_str)

if __name__ == '__main__':
    nose.main()
