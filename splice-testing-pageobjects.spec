Name:		splice-testing-pageobjects
Version:	0.7
Release:	1%{?dist}
Summary:	Splice WebUI page objects for test case automation

Group:		Development/Tools
License:	GPLv3+
URL:		https://github.com/RedHatQE/splice-testing-pageobjects
Source0:	%{name}-%{version}.tar.gz
BuildArch:  	noarch

BuildRequires:	python-devel
Requires:	python-selenium-wrapper

%description
%{summary}

%prep
%setup -q

%build

%install
%{__python} setup.py install --single-version-externally-managed -O1 --root=$RPM_BUILD_ROOT --record=INSTALLED_FILES 

%clean
rm -rf $RPM_BUILD_ROOT

%files -f INSTALLED_FILES
%defattr(-,root,root,-)
%doc LICENSE README.md


%changelog
* Fri Sep 06 2013 dparalen <vetrisko@gmail.com> 0.7-1
= Snapshot #4
- snapshot #5 handles org selection only when there are orgs to choose from
  (vetrisko@gmail.com)
- fix: default driver attribute (vetrisko@gmail.com)
- introducing the version attribute (vetrisko@gmail.com)
- introducing invalid date fields test case "stub" (vetrisko@gmail.com)
- fix: proper time handling instead of days addition (vetrisko@gmail.com)
- fix: slight gitch with first test case; SE.refresh() fixed
  (vetrisko@gmail.com)
- introducing signo-login--logout independence (vetrisko@gmail.com)
- introducing non-signo login and logout details (vetrisko@gmail.com)
- introducing org selection link (vetrisko@gmail.com)
- introducing a redirect page (vetrisko@gmail.com)

* Thu Aug 29 2013 dparalen <vetrisko@gmail.com> 0.6-1
- SAM 1.3 < Snap #4
- test modified to check properties of the context managers: preserved
  current_url, exceptions propagated (vetrisko@gmail.com)
- fix: test the context managers in more detail (vetrisko@gmail.com)
- now propagating driver config (vetrisko@gmail.com)
- fix: introducing try--finally block in contextmanagers (vetrisko@gmail.com)
- driver handling added (vetrisko@gmail.com)
- fix: double insufficient instead of invalid (vetrisko@gmail.com)
- fix to match run_report() API (p.bartikova@gmail.com)
- fix: avoid selecting when setting underscored attributess
  (vetrisko@gmail.com)
- fix: syntax' (vetrisko@gmail.com)
- fix: navigate no longer needed (vetrisko@gmail.com)
- adapting to match the basepageobject changes (vetrisko@gmail.com)
- fix: don't navigate when setting underscored attributes; fix: syntax
  (vetrisko@gmail.com)
- fix: using contexts for all steps now (vetrisko@gmail.com)
- adopting updated basepageobject features (vetrisko@gmail.com)
- adopting updated basepageobject features; context wrappers now preserve
  current_url (vetrisko@gmail.com)
- adopting updated basepageobject features (vetrisko@gmail.com)
- adopting updated basepageobject features; context wrappers now preserve
  current_url (vetrisko@gmail.com)
- introducing sam and reports url stuff (vetrisko@gmail.com)
- fix: org selecting stuff (vetrisko@gmail.com)
- re-design: page is a self-navigating object (vetrisko@gmail.com)
- introducing new InfoReportTestCase tests (p.bartikova@gmail.com)
- Merge branch 'master' of github.com:RedHatQE/splice-testing-pageobjects
  (vetrisko@gmail.com)
- fix: user_experimental_ui_ctx now preserves URL (vetrisko@gmail.com)
- Merge branch 'master' of github.com:RedHatQE/splice-testing-pageobjects
  (p.bartikova@gmail.com)
- introducing new test in NewFilterTestCaseVerification (p.bartikova@gmail.com)
- fix: organisation_ctx now preserves current URL (vetrisko@gmail.com)
- adjust the test case to match the login_ctx manager changes
  (vetrisko@gmail.com)
- fix: restoring URLs should now work as expected within the login_ctx manager
  (vetrisko@gmail.com)
- "fix": avoid restoring "Select An Organization" upon leave
  (vetrisko@gmail.com)
- fix: restore original url having logged in (vetrisko@gmail.com)
- fix: better refresh after test case (vetrisko@gmail.com)
- introducing create/delete filter functions ' (vetrisko@gmail.com)
- introducing further filter context managers (vetrisko@gmail.com)
- introducing elements comparison (vetrisko@gmail.com)
- implemented copy that returns a namespace (vetrisko@gmail.com)
- introducing date_range filter context manager (vetrisko@gmail.com)
- introducet filter details context test (vetrisko@gmail.com)
- introduced filter details context (vetrisko@gmail.com)
- a selenium.select attribute introduced (vetrisko@gmail.com)
- fix: run report has to be the last test case (vetrisko@gmail.com)
- fix: test case restores original experimental ui setting (vetrisko@gmail.com)
- fix: user item does not appear instantly (vetrisko@gmail.com)

* Thu Aug 15 2013 dparalen <vetrisko@gmail.com> 0.5-1
- SAM snapshot #1
- WebUiTestCase now does log in and enable experimental UI by default
  (vetrisko@gmail.com)
- introducing experimental ui enabler and disabler (vetrisko@gmail.com)
- introducing user_experimental_ui_ctx (vetrisko@gmail.com)
- introducing users page with the experimental_ui switch (vetrisko@gmail.com)
- fix: restore original page only when the current_organisation attribute is
  set (vetrisko@gmail.com)
- introducing sam page sanity tests (vetrisko@gmail.com)
- introducing dashboard url (vetrisko@gmail.com)
- fix: accessing the current organisation happens with the menu already
  selected (vetrisko@gmail.com)
- ACME_corporation organisation is selected by default (vetrisko@gmail.com)
- assert ACME_Corporation organisation (vetrisko@gmail.com)
- fix: selecting organisation resets page to dashboard (vetrisko@gmail.com)
- fix: remove debug prints (vetrisko@gmail.com)
- fix: missing singlequotes around name (vetrisko@gmail.com)
- fix: typo (vetrisko@gmail.com)
- fixes (vetrisko@gmail.com)
- introducing organisation context (vetrisko@gmail.com)
- fix: tests asserts not to count on the ACME_Corp bein the only org registered
  (vetrisko@gmail.com)
- introducing common SamPageObject (vetrisko@gmail.com)
- correction (p.bartikova@gmail.com)
- introducing new NewFilterTestCaseVerification test (p.bartikova@gmail.com)
- introducing report page object (vetrisko@gmail.com)
- introducing remove_default_filter test (p.bartikova@gmail.com)
- introducing DefaultRhelFilterTestCaseSanity tests (p.bartikova@gmail.com)
- introducing new NewFilterTestCaseVerification tests and select_all_options
  tests (p.bartikova@gmail.com)
- introducing NewFilterTestCaseVerification test (p.bartikova@gmail.com)
- introducing validation errors container (vetrisko@gmail.com)
- fix: added events.appears in FilterMenu (p.bartikova@gmail.com)
- structural update (vetrisko@gmail.com)
- fix: element change at filter name for selected_locator in filter menu
  (vetrisko@gmail.com)
- introducing new E2E tests (p.bartikova@gmail.com)
- introducing the filter_name field in a filter menu (vetrisko@gmail.com)
- fix: converted run_report method to static method (vetrisko@gmail.com)
- fix: the logout notice shouldn't be there anymore (vetrisko@gmail.com)
- fix: the logout notice shouldn't be there anymore (vetrisko@gmail.com)
- introducing an e2e new filter scenario (vetrisko@gmail.com)
- introducing a namespaced setattr thing (vetrisko@gmail.com)
- fix: test order (vetrisko@gmail.com)
- update: rc 1.3 changes inactive checkbox for lifecyle select
  (vetrisko@gmail.com)
- introducing date range field (vetrisko@gmail.com)
- introducing save filter button (vetrisko@gmail.com)
- introducing inactive checkbox (vetrisko@gmail.com)
- introducing selenium select use case (vetrisko@gmail.com)
- introducing SelectPageElements where select is used (vetrisko@gmail.com)
- introducing selec page element and organizations select (vetrisko@gmail.com)
- introducing status field (vetrisko@gmail.com)
- introducing particular hour selection options (vetrisko@gmail.com)
- introducing WebuiTestCase (vetrisko@gmail.com)
- introducing container attr element setter (vetrisko@gmail.com)
- introducing hours_field (vetrisko@gmail.com)
- introducing a container page element (vetrisko@gmail.com)
- fix: namespace import (vetrisko@gmail.com)
- added NewFilterTestCase.insert_description (p.bartikova@gmail.com)
- fixed asserting the value (p.bartikova@gmail.com)
- fixed __setattr__ (p.bartikova@gmail.com)
- introduced hours menu for new filter (vetrisko@gmail.com)
- implemented element attribute (vetrisko@gmail.com)

* Wed Jul 31 2013 dparalen <vetrisko@gmail.com> 0.4-1
- ignore vim .swo files, too (vetrisko@gmail.com)
- fix: leave files spec up to setup.py --record (vetrisko@gmail.com)
- fix: data specified explicitly (vetrisko@gmail.com)
- made the locators data of the library (vetrisko@gmail.com)
- move namespace module to pageobjects (vetrisko@gmail.com)

* Tue Jul 30 2013 dparalen <vetrisko@gmail.com> 0.3-1
- implemented a leaf processor (vetrisko@gmail.com)
- refactoring the basepageelement to accept locator as an __init__ parameter
  (vetrisko@gmail.com)
- refactoring and new filter menu introduced (vetrisko@gmail.com)
- refactoring and new filter menu introduced (vetrisko@gmail.com)
- refactoring and new filter menu introduced (vetrisko@gmail.com)
- fix: shouldn't be a descriptor; fix: setting attribute should invoke _select;
  fix: use appears in _select to determine selected status (vetrisko@gmail.com)
- fix: implement a two-fold is_displayed check to avoid second call to locator
  (vetrisko@gmail.com)
- fix: move MenuPageElement into a separate module (vetrisko@gmail.com)
- fix: MenuPageElement shouldn't be a descendant of BasePageElement
  (vetrisko@gmail.com)
- fix: selector requires a parameter; added docstring for _selector
  (vetrisko@gmail.com)
- fix: super call and override the default __get__ method (vetrisko@gmail.com)
- update: menu element requires a selector method (vetrisko@gmail.com)
- fix: allow custom selector method (vetrisko@gmail.com)
- Merge branch 'master' of github.com:RedHatQE/splice-testing-pageobjects
  (vetrisko@gmail.com)
- fix: decorate the filter locator with appears (vetrisko@gmail.com)
- fix: check whether an element appears by issuing its .is_displayed() method,
  too (vetrisko@gmail.com)
- Fix: example sam URL (vetrisko@gmail.com)
- requirements added (vetrisko@gmail.com)
- Update README.md (vetrisko@gmail.com)
- nosetests running mentioned (vetrisko@gmail.com)
- fix: exclude tests from the egg (vetrisko@gmail.com)

* Wed Jul 24 2013 dparalen <vetrisko@gmail.com> 0.2-1
- new package built with tito



