Name:		splice-testing-pageobjects
Version:	0.4
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



