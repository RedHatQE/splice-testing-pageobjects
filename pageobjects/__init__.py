# Page Objects
from selenium_wrapper import SE

locators = {
    "login.username": lambda : SE.find_element_by_name("username"),
    "login.password": lambda : SE.find_element_by_name("password"),
    "login.submit": lambda : SE.find_element_by_name("commit"),
    "login.logout": lambda : SE.find_element_by_link_text("logout"),
    "login.logout_notice": lambda: SE.find_element_by_xpath("//li[text()='You have been logged out']"),

    "filters.page_title": lambda: SE.find_element_by_xpath("//header/h2[@original-title='Report Filters']"),
    "filters.filter": lambda filter_name: SE.find_element_by_xpath("//div/div/span[normalize-space(text()) = '%s']/../.." % filter_name),
    "filters.filter.close_link": lambda : SE.find_element_by_xpath("//a[@class='close' and @href='#' and @data-close='panel' and text() = 'Close']"),
    "filters.filter.selected": lambda filter_name: SE.find_element_by_xpath("//div[@id='filter_name' and @title='%s']" % filter_name),
    "filters.filter.run_button": lambda : SE.find_element_by_xpath("//a[contains(@href, 'reports')]/div[@id='submit_button' and normalize-space(text())='Run Report']/.."),
    "filters.filter.encrypt_export": lambda : SE.find_element_by_xpath("//input[@id='splice_reports_export_encrypt_cbox' and @type='checkbox']"),
    "filters.filter.skip_json_export": lambda : SE.find_element_by_xpath("//input[@id='splice_reports_include_json_cbox' and @type='checkbox']") 

}

pages = {
    "login.url": u"/signo",
    "login.title": "Signo",
    "logout": u"/signo",
    "logout.title": "Signo", 
    "filters.url": u"sam/splice_reports/filters"
}
