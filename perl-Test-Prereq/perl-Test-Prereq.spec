Name:           perl-Test-Prereq
Version:        1.037
Release:        2%{?dist}
Summary:        Check if Makefile.PL has the right pre-requisites
License:        GPL+ or Artistic
Group:          Development/Libraries
URL:            http://search.cpan.org/dist/Test-Prereq/
Source0:        http://www.cpan.org/authors/id/B/BD/BDFOY/Test-Prereq-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  perl(Module::Build)
BuildRequires:  perl(Module::CoreList)
BuildRequires:  perl(Module::Info)
BuildRequires:  perl(CPAN)
BuildRequires:  perl(Test::Builder)
BuildRequires:  perl(Test::Builder::Tester)
BuildRequires:  perl(Test::More)
BuildRequires:  perl(Test::Pod)
BuildRequires:  perl(Test::Pod::Coverage)
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%description
The prereq_ok() function examines the modules it finds in blib/lib/,
blib/script, and the test files it finds in t/ (and test.pl). It figures
out which modules they use, skips the modules that are in the Perl core,
and compares the remaining list of modules to those in the PREREQ_PM
section of Makefile.PL.

%prep
%setup -q -n Test-Prereq-%{version}

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT

make pure_install PERL_INSTALL_ROOT=$RPM_BUILD_ROOT

find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} \;
find $RPM_BUILD_ROOT -depth -type d -empty -exec rmdir {} \;

%{_fixperms} $RPM_BUILD_ROOT/*

%check
# switch off tests completely, because they are detected at the start
# and can't be easily switched off by _with_network_tests
#make test

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc Changes LICENSE README
%{perl_vendorlib}/*
%{_mandir}/man3/*

%changelog
* Wed Jan  6 2010 Marcela Mašláňová <mmaslano@redhat.com> - 1.037-2
- switch off failing tests, which need network
- Resolves: rhbz#552804 

* Fri Oct 30 2009 Stepan Kasal <skasal@redhat.com> - 1.037-1
- new upstream version

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.036-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.036-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Jan 22 2009 Steven Pritchard <steve@kspei.com> 1.036-1
- Update to 1.036.
- Add some dependencies when building with --with-check.

* Wed Dec 10 2008 Steven Pritchard <steve@kspei.com> 1.034-1
- Update to 1.034.

* Tue Feb  5 2008 Tom "spot" Callaway <tcallawa@redhat.com> 1.033-2
- rebuild for new perl

* Fri Mar 23 2007 Steven Pritchard <steve@kspei.com> 1.033-1
- Update to 1.033.

* Wed Jan 17 2007 Steven Pritchard <steve@kspei.com> 1.032-1
- Update to 1.032.
- Use fixperms macro instead of our own chmod incantation.
- Add LICENSE to docs.

* Sat Sep 16 2006 Steven Pritchard <steve@kspei.com> 1.031-2
- Fix find option order.

* Wed May 24 2006 Steven Pritchard <steve@kspei.com> 1.031-1
- Update to 1.031.

* Fri Mar 24 2006 Steven Pritchard <steve@kspei.com> 1.030-1
- Specfile autogenerated by cpanspec 1.64.
- Fix License.
- Drop explicit Requires.
- Disable tests by default (uses network).