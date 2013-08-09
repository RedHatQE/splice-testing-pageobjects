#!/usr/bin/env python
import sys, unittest, re, time, os.path, logging, nose, selenium, webuitestcase
import tests as TESTS
import pageobjects.filters as filters
from pageobjects.login import login, logout
from selenium_wrapper import SE
from selenium.common.exceptions import NoSuchElementException, TimeoutException

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
        SE.get(KATELLO.url)
        cls.filters = filters.Filters()

    def setUp(self):
        self.verificationErrors = []

    def tearDown(self):
        self.assertEqual([], self.verificationErrors)

    @classmethod
    def tearDownClass(cls):
        SE.get(KATELLO.url)
        logout()


class DefaultRhelFilterTestCase(BaseFilterTestCase):
    @classmethod
    def setUpClass(cls):
        super(DefaultRhelFilterTestCase, cls).setUpClass()
        cls.report_filter = cls.filters.get_filter(filters.REDHAT_DEFAULT_FILTER_NAME)

    def test_01_select(self):
        self.report_filter

    def test_02_select_and_close(self):
        self.report_filter.close()

        
    def test_03_enable_encrypt_export(self):
        #self.report_filter.encrypt_export
        try:
            self.assertTrue(self.report_filter.encrypt_export.is_selected())
        except AssertionError:
            self.report_filter.encrypt_export.click()
            self.assertTrue(self.report_filter.encrypt_export.is_selected())

    def test_04_enable_skipping_json_export(self):
        try:
            self.assertTrue(self.report_filter.skip_json_export.is_selected())
        except AssertionError:
            self.report_filter.skip_json_export.click()
            self.assertTrue(self.report_filter.skip_json_export.is_selected())

    def test_05_run(self):
        self.report_filter.run_report()


class DefaultRhelFilterTestCaseSanity(BaseFilterTestCase):
    @classmethod
    def setUpClass(cls):
        super(DefaultRhelFilterTestCaseSanity, cls).setUpClass()
        cls.report_filter = cls.filters.default_filter_menu
        
    def test_01_filter_name(self):
        self.assertEqual(self.report_filter.filter_name.text, "Red Hat Default Report")
        
    def test_02_description_name(self):
        self.assertEqual(self.report_filter.filter_description.text, "A default report that can be sent back to Red Hat representatives")
        
    def test_03_status_field(self):
        self.assertEqual(self.report_filter.status_field.text, "Current, Invalid, Insufficient")
        
    def test_04_satellite_field(self):
        self.assertEqual(self.report_filter.satellite_field.text, "Any")
        
    def test_05_organizations_field(self):
        self.assertEqual(self.report_filter.organizations_field.text, "ACME_Corporation")
        
    def test_06_lifecycle_field(self):
        self.assertEqual(self.report_filter.lifecycle_field.text, "Active, Inactive")
        
    def test_07_hours_field(self):
        self.assertEqual(self.report_filter.hours_field.text, "24")
        
    def test_08_start_date(self):
        self.assertEqual(self.report_filter.start_date.text, "None")
        
    def test_09_end_date(self):
        self.assertEqual(self.report_filter.end_date.text, "None")

class NewFilterTestCase(BaseFilterTestCase):

    def tearDown(self):
        # make sure the menu is closed after each test to deselect items selected by the test
        self.filters.new_filter_menu.close()

    def test_01_select(self):
        # navigate to new filter menu works
        # FIXME: assert something here
        self.filters.new_filter_menu.filter_name

    def test_02_insert_name(self):
        # check name can be inserted
        self.filters.new_filter_menu.filter_name = self.__class__.__name__ + "_filter"
        self.assertElementValue(self.filters.new_filter_menu.filter_name, self.__class__.__name__ + "_filter")

    def test_03_insert_description(self):
        # check description can be inserted
        self.filters.new_filter_menu.filter_description = self.__class__.__name__ + "_description"
        self.assertElementValue(self.filters.new_filter_menu.filter_description, self.__class__.__name__ + "_description")

    def test_04_select_hours_menu(self):
        self.filters.new_filter_menu.hours_menu
        self.assertTrue(self.filters.new_filter_menu.hours_menu.element.is_selected())

    def test_05_select_hours_field(self):
        self.filters.new_filter_menu.hours_menu.hours_field.element = '24'
        self.assertElementValue(self.filters.new_filter_menu.hours_menu.hours_field.element, '24')

    def test_06_select_hours_field_option(self):
        self.filters.new_filter_menu.hours_menu.hours_field.option_8.click()
        self.assertElementValue(self.filters.new_filter_menu.hours_menu.hours_field.element, '8')

    def test_07_select_current_status_option(self):
        self.filters.new_filter_menu.status_field.option_current.click()
        self.assertTrue(self.filters.new_filter_menu.status_field.option_current.is_selected())

    def test_08_select_invalid_status_option(self):
        self.filters.new_filter_menu.status_field.option_invalid.click()
        self.assertTrue(self.filters.new_filter_menu.status_field.option_invalid.is_selected())

    def test_09_select_insufficient_status_option(self):
        self.filters.new_filter_menu.status_field.option_insufficient.click()
        self.assertTrue(self.filters.new_filter_menu.status_field.option_insufficient.is_selected())
        
    def test_10_select_all_status_options(self):
        self.filters.new_filter_menu.status_field.option_current.click()
        self.filters.new_filter_menu.status_field.option_invalid.click()
        self.filters.new_filter_menu.status_field.option_insufficient.click()
        self.assertTrue(self.filters.new_filter_menu.status_field.option_current.is_selected())
        self.assertTrue(self.filters.new_filter_menu.status_field.option_invalid.is_selected())
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
        
    def test_17_select_all_lifecycle_options(self):
        self.filters.new_filter_menu.lifecycle_field.option_active.click()
        self.filters.new_filter_menu.lifecycle_field.option_inactive.click()
        self.filters.new_filter_menu.lifecycle_field.option_deleted.click()
        self.assertTrue(self.filters.new_filter_menu.lifecycle_field.option_active.is_selected())
        self.assertTrue(self.filters.new_filter_menu.lifecycle_field.option_inactive.is_selected())
        self.assertTrue(self.filters.new_filter_menu.lifecycle_field.option_deleted.is_selected())

    def test_18_has_save_filter_button(self):
        self.filters.new_filter_menu.save_filter

    def test_19_select_date_range_menu(self):
        self.filters.new_filter_menu.date_range_menu
        self.assertTrue(self.filters.new_filter_menu.date_range_menu.element.is_selected())

    def test_20_set_start_date(self):
        import datetime
        # FIXME the WebUI might have a bug here: it doesn't accept iso formated date
        today = datetime.date.today()
        today_str = "%02d/%02d/%d" % (today.month, today.day, today.year)
        self.filters.new_filter_menu.date_range_menu.start_date = today_str
        self.assertElementValue(self.filters.new_filter_menu.date_range_menu.start_date, today_str)

    def test_21_set_end_date(self):
        import datetime
        # FIXME the WebUI might have a bug here: it doesn't accept iso formated date
        today = datetime.date.today()
        today_str = "%02d/%02d/%d" % (today.month, today.day, today.year)
        self.filters.new_filter_menu.date_range_menu.end_date = today_str
        self.assertElementValue(self.filters.new_filter_menu.date_range_menu.end_date, today_str)


class NewFilterTestE2ECase(BaseFilterTestCase):
    @classmethod
    def setUpClass(cls):
        super(NewFilterTestE2ECase, cls).setUpClass()
        import pageobjects.namespace
        # details to be filled in the new filter menu
        cls.filter_details = pageobjects.namespace.load_ns({
            'filter_name': cls.__name__ + "_test",
            'filter_description': cls.__name__ + "_description",
            'hours_menu': {
                'hours_field': "24"
            },
            'status_field': "Current",
            'organizations_field': "ACME_Corporation",
            'lifecycle_field': "Active"
        })

        # apply the filter details to the new_filter_menu
        pageobjects.namespace.setattr_ns(cls.filters.new_filter_menu, cls.filter_details)
        # submit the new filter
        cls.filters.new_filter_menu.submit()
        cls.the_filter = cls.filters.get_filter(cls.filter_details.filter_name)
        # kinda "refresh" here
        cls.filters.navigate()

    @classmethod
    def tearDownClass(cls):
        # have to remove the filter through the cls.filters attribute instead of cls.the_filter
        # to access the filters/reports page before accessing the_filter
        SE.get(KATELLO.url)
        cls.filters.get_filter(cls.filter_details.filter_name).remove()
        super(NewFilterTestE2ECase, cls).tearDownClass()
        
    def test_01_filter_name(self):
        self.assertEqual(self.the_filter.filter_name.text, self.filter_details.filter_name)
        
    def test_02_description_name(self):
        self.assertEqual(self.the_filter.filter_description.text, self.filter_details.filter_description)
        
    def test_03_hours_field(self):
        self.assertEqual(self.the_filter.hours_field.text, self.filter_details.hours_menu.hours_field)
        
    def test_04_status_field(self):
        self.assertEqual(self.the_filter.status_field.text, self.filter_details.status_field)
        
    def test_05_organizations_field(self):
        self.assertEqual(self.the_filter.organizations_field.text, self.filter_details.organizations_field)
        
    def test_06_lifecycle_field(self):
        self.assertEqual(self.the_filter.lifecycle_field.text, self.filter_details.lifecycle_field)
        
    def test_07_start_date(self):
        self.assertEqual(self.the_filter.start_date.text, "None")
        
    def test_08_end_date(self):
        self.assertEqual(self.the_filter.end_date.text, "None")


class NewFilterTestCaseVerification(BaseFilterTestCase):

    def tearDown(self):
        # make sure the menu is closed after each test to deselect items selected by the test
        self.filters.new_filter_menu.validation_error_message.close()
        self.filters.new_filter_menu.close()

    def test_01_empty_mandatory_fields(self):
        self.filters.new_filter_menu.submit()
        self.filters.new_filter_menu.validation_error_message.message_filter_name
        self.filters.new_filter_menu.validation_error_message.message_status_field
        self.filters.new_filter_menu.validation_error_message.message_lifecycle_field
        self.filters.new_filter_menu.validation_error_message.message_hour_date_criteria
        
    def test_02_no_empty_filter_name_field(self):
        self.filters.new_filter_menu.filter_name = self.__class__.__name__ + "_filter"
        self.filters.new_filter_menu.submit()
        with self.assertRaises(TimeoutException):
            self.filters.new_filter_menu.validation_error_message.message_filter_name
        
    def test_03_no_empty_status_field(self):
        self.filters.new_filter_menu.status_field.option_current.click()
        self.filters.new_filter_menu.submit()
        with self.assertRaises(TimeoutException):
            self.filters.new_filter_menu.validation_error_message.message_status_field

    def test_04_mo_empty_lifecycle_field(self):
        self.filters.new_filter_menu.lifecycle_field.option_active.click()
        self.filters.new_filter_menu.submit()
        with self.assertRaises(TimeoutException):
            self.filters.new_filter_menu.validation_error_message.message_lifecycle_field
        
    def test_05_no_empty_hours_field(self):
        self.filters.new_filter_menu.hours_menu.hours_field.element = '24'
        self.filters.new_filter_menu.submit()
        with self.assertRaises(TimeoutException):
            self.filters.new_filter_menu.validation_error_message.message_hour_date_criteria
            
    def test_06_empty_only_status_and_lifecycle_field(self):
        self.filters.new_filter_menu.filter_name = self.__class__.__name__ + "_filter"
        self.filters.new_filter_menu.hours_menu.hours_field.option_8.click()
        self.filters.new_filter_menu.submit()
        self.filters.new_filter_menu.validation_error_message.message_status_field
        self.filters.new_filter_menu.validation_error_message.message_lifecycle_field
        with self.assertRaises(TimeoutException):
            self.filters.new_filter_menu.validation_error_message.message_filter_name
        with self.assertRaises(TimeoutException):
            self.filters.new_filter_menu.validation_error_message.message_hour_date_criteria

if __name__ == '__main__':
    nose.main()
