Name:		splice-testing-pageobjects
Version:	0.1
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
%{__python} setup.py install -O1 --root $RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc LICENSE README.md
%{python_sitelib}/*.egg-info
%{python_sitelib}/pageobjects/*.py*

%changelog


