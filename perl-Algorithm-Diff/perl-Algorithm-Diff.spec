Name:           perl-Algorithm-Diff
Version:        1.1902
Release:        9%{?dist}
Summary:        Algorithm::Diff Perl module
License:        GPL+ or Artistic
Group:          Development/Libraries
URL:            http://search.cpan.org/dist/Algorithm-Diff/
Source0:        http://www.cpan.org/authors/id/T/TY/TYEMQ/Algorithm-Diff-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  perl(ExtUtils::MakeMaker)
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%description
This is a module for computing the difference between two files, two
strings, or any other two lists of things.  It uses an intelligent
algorithm similar to (or identical to) the one used by the Unix "diff"
program.  It is guaranteed to find the *smallest possible* set of
differences.

%prep
%setup -q -n Algorithm-Diff-%{version}
chmod 644 *.pl

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT

make pure_install PERL_INSTALL_ROOT=$RPM_BUILD_ROOT

find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} \;
find $RPM_BUILD_ROOT -depth -type d -exec rmdir {} 2>/dev/null \;

%{_fixperms} $RPM_BUILD_ROOT/*

rm -f $RPM_BUILD_ROOT%{perl_vendorlib}/Algorithm/*.pl

%check
make test

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc Changes README *.pl
%{perl_vendorlib}/*
%{_mandir}/man3/*

%changelog
* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 1.1902-9
- rebuild against perl 5.10.1

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1902-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1902-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Feb 27 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.1902-6
- Rebuild for perl 5.10 (again)

* Sun Jan 20 2008 Tom "spot" Callaway <tcallawa@redhat.com> 1.1902-5
- rebuild for new perl

* Thu Jan 10 2008 Tom "spot" Callaway <tcallawa@redhat.com> 1.1902-4
- fix license tag, rebuild for perl

* Wed Apr 18 2007 Steven Pritchard <steve@kspei.com> 1.1902-3
- Use fixperms macro instead of our own chmod incantation.
- BR ExtUtils::MakeMaker.

* Sun Sep 17 2006 Steven Pritchard <steve@kspei.com> 1.1902-2
- Rebuild.

* Sat Aug 05 2006 Steven Pritchard <steve@kspei.com> 1.1902-1
- Update to 1.1902.
- Minor spec cleanup to match current template/cpanspec output.

* Mon Sep 05 2005 Steven Pritchard <steve@kspei.com> 1.1901-1
- Updated to 1.1901.

* Sat Sep 03 2005 Steven Pritchard <steve@kspei.com> 1.15-2
- Move example files to %%doc.

* Sat Aug 27 2005 Steven Pritchard <steve@kspei.com> 1.15-1
- Specfile autogenerated.
