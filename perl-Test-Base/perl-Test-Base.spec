Name:           perl-Test-Base
Version:        0.58
Release:        3%{?dist}
Summary:        Data Driven Testing Framework
License:        GPL+ or Artistic
Group:          Development/Libraries
URL:            http://search.cpan.org/dist/Test-Base/
Source0:        http://www.cpan.org/authors/id/I/IN/INGY/Test-Base-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(Spiffy) >= 0.30
BuildRequires:  perl(Test::Deep)
BuildRequires:  perl(Test::More) >= 0.62
BuildRequires:  perl(Test::Tester)
BuildRequires:  perl(Text::Diff) >= 0.35
BuildRequires:  perl(YAML)
Requires:       perl(Text::Diff) >= 0.35
Requires:       perl(LWP::Simple)
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%description
Testing is usually the ugly part of Perl module authoring. Perl gives you a
standard way to run tests with Test::Harness, and basic testing primitives
with Test::More. After that you are pretty much on your own to develop a
testing framework and philosophy. Test::More encourages you to make your
own framework by subclassing Test::Builder, but that is not trivial.

%prep
%setup -q -n Test-Base-%{version}

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT

make pure_install PERL_INSTALL_ROOT=$RPM_BUILD_ROOT

find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} \;
find $RPM_BUILD_ROOT -depth -type d -exec rmdir {} 2>/dev/null \;

%{_fixperms} $RPM_BUILD_ROOT/*

%check
make test

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc Changes README
%{perl_vendorlib}/*
%{_mandir}/man3/*

%changelog
* Fri Dec  4 2009 Stepan Kasal <skasal@redhat.com> - 0.58-3
- rebuild against perl 5.10.1

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.58-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sun May 17 2009 Steven Pritchard <steve@kspei.com> 0.58-1
- Update to 0.58.
- BR Test::Deep and Test::Tester.

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.55-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Dec 10 2008 Steven Pritchard <steve@kspei.com> 0.55-1
- Update to 0.55.
- Explicitly BR Test::More >= 0.62.
- BR YAML.

* Thu Mar 06 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.54-3
- Rebuild for new perl

* Sat Jul 07 2007 Steven Pritchard <steve@kspei.com> 0.54-2
- BR Test::More.

* Mon Jul 02 2007 Steven Pritchard <steve@kspei.com> 0.54-1
- Update to 0.54.

* Wed Apr 18 2007 Steven Pritchard <steve@kspei.com> 0.53-2
- BR ExtUtils::MakeMaker.

* Sat Dec 09 2006 Steven Pritchard <steve@kspei.com> 0.53-1
- Update to 0.53.
- Use fixperms macro instead of our own chmod incantation.

* Sat Sep 16 2006 Steven Pritchard <steve@kspei.com> 0.52-2
- Fix find option order.

* Sat Jul 01 2006 Steven Pritchard <steve@kspei.com> 0.52-1
- Update to 0.52.

* Mon May 08 2006 Steven Pritchard <steve@kspei.com> 0.50-2
- Add explicit dependencies for Text::Diff and LWP::Simple.

* Thu May 04 2006 Steven Pritchard <steve@kspei.com> 0.50-1
- Specfile autogenerated by cpanspec 1.65.
- Remove explicit BR: perl and Requires: perl(Spiffy).