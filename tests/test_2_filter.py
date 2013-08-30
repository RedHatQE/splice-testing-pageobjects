#!/usr/bin/env python
import sys, unittest, re, time, os.path, logging, nose, selenium, webuitestcase
import tests as TESTS
import pageobjects.filters as filters
from pageobjects.login import login, logout, login_ctx
from pageobjects.sampageobject import organisation_ctx
from pageobjects.users import user_experimental_ui_ctx
from selenium_wrapper import SE, current_url, restore_url
from selenium.common.exceptions import NoSuchElementException, TimeoutException

KATELLO = TESTS.ROLES.KATELLO
SELENIUM = TESTS.ROLES.SELENIUM

class BaseFilterTestCase(webuitestcase.WebuiTestCase):
    @classmethod
    def setUpClass(cls):
        # reset SE driver 
        super(BaseFilterTestCase, cls).setUpClass()
        cls.filters = filters.Filters()
        cls.filters.organisation_menu.current_organisation = 'ACME_Corporation'

    def setUp(self):
        self.verificationErrors = []

    def tearDown(self):
        self.assertEqual([], self.verificationErrors)


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

    def test_05_remove_filter(self):
        self.report_filter.remove_default_filter

    def test_99_run(self):
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
        self.assertIn("ACME_Corporation", self.report_filter.organizations_field.text)
        
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
        SE.refresh()

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
            
    def test_07_start_date_later_than_end_date(self):
        import datetime
        today = datetime.date.today()
        today2_str = "%02d/%02d/%d" % (today.month, today.day+2, today.year)
        self.filters.new_filter_menu.date_range_menu.start_date = today2_str
        today_str = "%02d/%02d/%d" % (today.month, today.day, today.year)
        self.filters.new_filter_menu.date_range_menu.end_date = today_str
        self.filters.new_filter_menu.submit()
        self.filters.new_filter_menu.validation_error_message.message_date_criteria
        
    def test_08_filter_name_white_space(self):
        self.filters.new_filter_menu.filter_name = "   "
        self.filters.new_filter_menu.submit()
        with self.assertRaises(TimeoutException):
            self.filters.new_filter_menu.validation_error_message.message_filter_name
        self.filters.new_filter_menu.validation_error_message.message_filter_name_white_space

        
        
class FilterDetailsCtxTest(webuitestcase.WebuiTestCase):
    @classmethod
    def setUpClass(cls):
        # override default in order not to do login --- done within the contexts here
        SE.reset(driver=SELENIUM.driver, url=KATELLO.url)
        SE.maximize_window()
        cls.details = filters.DEFAULT_FILTER_DETAILS
   
    @classmethod
    def tearDownClass(cls):
        # override default in order not to do logout --- done within the contexts here
        pass
         
    def assertNonTimeFields(self):
        from selenium_wrapper import SE
        self.assertEqual(self.filter_menu.filter_name.text, self.details.filter_name)
        self.assertEqual(self.filter_menu.filter_description.text, self.details.filter_description)
        self.assertSameElements(self.filter_menu.organizations_field.text, self.details.organizations_field.select)
        self.assertSameElements(self.filter_menu.status_field.text, self.details.status_field.select)
        self.assertSameElements(self.filter_menu.lifecycle_field.text, self.details.lifecycle_field.select)

    def assertDateRangeFields(self):
        self.assertEqual(self.filter_menu.start_date.text, self.details.date_range_menu.start_date)
        self.assertEqual(self.filter_menu.end_date.text, self.details.date_range_menu.end_date)

    def assertHoursField(self):
        self.assertEqual(self.filter_menu.hours_field.text, self.details.hours_menu.hours_field)

    def setUp(self):
        # reset the filter menu
        self.filter_menu = None

    def tearDown(self):
        # remove the filter_menu if present (after test case Failure/Error in the ctx)
        # FIXME: some kind of a bug; removing the filter doesn't work without a refresh here
        #from selenium_wrapper import SE
        #SE.refresh()
        if self.filter_menu is not None:
            self.filter_menu.remove()

    def test_01_preserve_status(self):
        '''assert context managers preserve exceptions and SE.current_url'''

        class SurpriseError(RuntimeError):
            '''a surprise error type'''

        with self.assertRaises(SurpriseError):
            with current_url(KATELLO.url):
                self.assertEqual(SE.current_url, KATELLO.url + "/")
                with login_ctx(KATELLO.username, KATELLO.password):
                    self.assertEqual(SE.current_url, KATELLO.url + "/")
                    with user_experimental_ui_ctx(KATELLO.username):
                        self.assertEqual(SE.current_url, KATELLO.url + "/")
                        with organisation_ctx("ACME_Corporation"):
                            self.assertEqual(SE.current_url, KATELLO.url + "/")
                            with filters.filter_details_ctx() as (filters_page, filter_menu):
                                # ;) self.assertEqual(SE.current_url, KATELLO.url + "/")
                                report_page = filter_menu.run_report()
                                raise SurpriseError("oOops")
                            self.assertEqual(SE.current_url, KATELLO.url + "/")
                        self.assertEqual(SE.current_url, KATELLO.url + "/")
                    self.assertEqual(SE.current_url, KATELLO.url + "/")
                self.assertEqual(SE.current_url, KATELLO.url + "/")

    def test_02_date_range_ctx(self):
        with current_url(KATELLO.url):
            with login_ctx(KATELLO.username, KATELLO.password):
                with user_experimental_ui_ctx(KATELLO.username):
                    with organisation_ctx("ACME_Corporation"):
                        with filters.filter_date_range_ctx() as (filters_page, filter_menu):
                            filters_page._navigate()
                            self.filter_menu = filter_menu
                            self.assertNonTimeFields()
                            self.assertDateRangeFields()
                            self.filter_menu = None

    def test_03_hours_ctx(self):
        with current_url(KATELLO.url):
            with login_ctx(KATELLO.username, KATELLO.password):
                with user_experimental_ui_ctx(KATELLO.username):
                    with organisation_ctx("ACME_Corporation"):
                        with filters.filter_hours_ctx() as (filters_page, filter_menu):
                            filters_page._navigate()
                            self.filter_menu = filter_menu
                            self.assertNonTimeFields()
                            self.assertHoursField()
                            self.filter_menu = None

if __name__ == '__main__':
    nose.main()
