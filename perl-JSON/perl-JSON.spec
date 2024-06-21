Name:           perl-JSON
Version:        2.15
Release:        5%{?dist}
Summary:        Parse and convert to JSON (JavaScript Object Notation)
License:        GPL+ or Artistic
Group:          Development/Libraries
URL:            http://search.cpan.org/dist/JSON/
Source0:        http://search.cpan.org/CPAN/authors/id/M/MA/MAKAMAKA/JSON-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

# core
BuildRequires:  perl(ExtUtils::MakeMaker)
# cpan
BuildRequires:  perl(HTTP::Request)
BuildRequires:  perl(HTTP::Response)
# tests, etc
BuildRequires:  perl(CGI)
BuildRequires:  perl(LWP::UserAgent)
BuildRequires:  perl(HTTP::Daemon)
BuildRequires:  perl(Test::More)
BuildRequires:  perl(Scalar::Util)

# not picked up due to eval { requires ... } constructs
Requires:       perl(Scalar::Util)
Requires:       perl(LWP::UserAgent)
Requires:       perl(HTTP::Daemon)

# use the whole kit-n-kaboodle, as perl_default_filter isn't in F-11
%{?filter_setup: %{expand: 
%filter_from_provides /^perl(JSON::PP)$/d
%filter_provides_in %{perl_vendorarch}/.*\\.so$ 
%filter_provides_in -P %{perl_archlib}/(?!CORE/libperl).*\\.so$ 
%filter_provides_in %{_docdir} 
%filter_requires_in %{_docdir} 
%filter_setup 
}}

%description
This module converts between JSON (JavaScript Object Notation) and Perl
data structure into each other. For JSON, see http://www.crockford.com/JSON/.

%prep
%setup -q -n JSON-%{version}

# make rpmlint happy...
find .  -type f -exec chmod -c -x {} +
find t/ -type f -exec perl -pi -e 's|^#! perl|#!%{__perl}|' {} +
sed -i 's/\r//' README t/*

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
rm -rf %{buildroot}

make pure_install PERL_INSTALL_ROOT=%{buildroot}

find %{buildroot} -type f -name .packlist -exec rm -f {} +
find %{buildroot} -depth -type d -exec rmdir {} 2>/dev/null \;

%{_fixperms} %{buildroot}/*

%check
make test

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc Changes README t/
%{perl_vendorlib}/*
%{_mandir}/man3/*

%changelog
* Wed Sep 02 2009 Chris Weyl <cweyl@alumni.drew.edu> 2.15-5
- adjust filtering so we don't drop the versioned perl(JSON:PP) prov

* Tue Sep 01 2009 Chris Weyl <cweyl@alumni.drew.edu> 2.15-4
- bump

* Mon Aug 31 2009 Chris Weyl <cweyl@alumni.drew.edu> 2.15-3
- update filtering 

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.15-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Jun 22 2009 Chris Weyl <cweyl@alumni.drew.edu> 2.15-1
- auto-update to 2.15 (by cpan-spec-update 0.01)

* Sun Mar 01 2009 Chris Weyl <cweyl@alumni.drew.edu> 2.14-1
- update to 2.14

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.12-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.12-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sun Oct 12 2008 Chris Weyl <cweyl@alumni.drew.edu> 2.12-1
- update to 2.12

* Wed Jun 25 2008 Chris Weyl <cweyl@alumni.drew.edu> 2.11-1
- update to 2.11

* Wed May 28 2008 Chris Weyl <cweyl@alumni.drew.edu> 2.09-1
- update to 2.09

* Sun Mar 09 2008 Chris Weyl <cweyl@alumni.drew.edu> 2.07-1
- update to 2.x series before F9

* Wed Mar  5 2008 Tom "spot" Callaway <tcallawa@redhat.com> 1.15-2
- rebuild for new perl

* Mon Nov 26 2007 Chris Weyl <cweyl@alumni.drew.edu> 1.15-1
- update to 1.15

* Sun May 13 2007 Chris Weyl <cweyl@alumni.drew.edu> 1.14-1
- update to 1.14

* Wed May 09 2007 Chris Weyl <cweyl@alumni.drew.edu> 1.13-1
- update to 1.13

* Fri May 04 2007 Chris Weyl <cweyl@alumni.drew.edu> 1.12-1
- update to 1.12
- add t/ to %%doc

* Wed Apr 25 2007 Chris Weyl <cweyl@alumni.drew.edu> 1.11-2
- bump

* Tue Apr 24 2007 Chris Weyl <cweyl@alumni.drew.edu> 1.11-1
- update to 1.11

* Wed Apr 18 2007 Chris Weyl <cweyl@alumni.drew.edu> 1.10-1
- Specfile autogenerated by cpanspec 1.69.1.