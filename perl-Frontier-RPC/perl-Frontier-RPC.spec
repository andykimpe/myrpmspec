Summary:        A Perl interface for making and serving XML-RPC calls
Name:           perl-Frontier-RPC
Version:        0.07b4p1
Release:        10%{?dist}
License:        GPL+ or Artistic
Group:          Development/Libraries
URL:            http://search.cpan.org/dist/Frontier-RPC/
Source0:        http://search.cpan.org/CPAN/authors/id/R/RT/RTFIREFLY/Frontier-RPC-%{version}.tar.gz
Patch0:         perl-frontier-raw-call.patch
Patch1:         perl-frontier-raw-serve.patch
Patch2:         perl-frontier-undef-scalar.patch
Patch3:         security-xml-external-entity.patch
Patch4:         apache2.patch
# Respect proxy setting for HTTPS, bug #832390, CPAN RT#117812
Patch5:         Frontier-RPC-0.07b4p1-Respect-proxy-setting-for-HTTPS.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  perl(LWP::UserAgent), perl(XML::Parser), perl(ExtUtils::MakeMaker)
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
Requires:       perl-Frontier-RPC-doc

%package Client
Summary:        Frontier-RPC-Client Perl module
Group:          Development/Libraries
License:        GPL+ or Artistic
Requires:       perl-Frontier-RPC-doc

# fix conflicts between those two packages
%package doc
Summary:        Frontier-RPC-Client Perl module documentation
Group:          Development/Libraries
License:        GPL+ or Artistic

%description
Frontier::RPC implements UserLand Software's XML RPC (Remote
Procedure Calls using Extensible Markup Language).  Frontier::RPC
includes both a client module for making requests to a server and
several server modules for implementing servers using CGI, Apache,
and standalone with HTTP::Daemon.

%description Client
Frontier::RPC::Client implements UserLand Software's XML RPC (Remote
Procedure Calls using Extensible Markup Language).  Frontier::RPC::Client
includes just client module for making requests to a server.

%description doc
Documentation and examples to Frontier::RPC and Frontier::RPC::Client.

%prep
%setup -q -n Frontier-RPC-%{version}
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT

make pure_install DESTDIR=$RPM_BUILD_ROOT

find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} \;
find $RPM_BUILD_ROOT -depth -type d -exec rmdir {} 2>/dev/null \;

%{_fixperms} $RPM_BUILD_ROOT/*

%check
make test

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%{perl_vendorlib}/*

%files Client
%defattr(-,root,root,-)
%{perl_vendorlib}/Frontier/Client.pm
%{perl_vendorlib}/Frontier/RPC2.pm

%files doc
%defattr(-,root,root,-)
%doc ChangeLog Changes COPYING README examples/
%{_mandir}/man3/*

%changelog
* Tue Sep 13 2016 Petr Pisar <ppisar@redhat.com> - 0.07b4p1-10
- Respect proxy setting for HTTPS (bug #832390)

* Mon May  3 2010 Marcela Mašláňová <mmaslano@redhat.com> - 0.07b4p1-9
- create doc sub-package to solve conflicts
- Related: rhbz#543948

* Fri Dec  4 2009 Stepan Kasal <skasal@redhat.com> - 0.07b4p1-8
- rebuild against perl 5.10.1

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.07b4p1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.07b4p1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Aug 28 2008 Tom "spot" Callaway <tcallawa@redhat.com> 0.07b4p1-5
- fix license tag

* Wed Jul 30 2008 Miroslav Suchý <msuchy@redhat.com> 0.07b4p1-4
- applied security patches.
- created light package with only Client part.

* Thu Mar 06 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.07b4-4
Rebuild for new perl

* Fri Oct 26 2007 Robin Norwood <rnorwood@redhat.com> - 0.07b4-3
- Various fixes from package review:
- Remove BR: perl
- Use dist tag in release
- Resolves: bz#226258

* Wed Aug 29 2007 Robin Norwood <rnorwood@redhat.com> - 0.07b4-2
- Update license tag
- add some files to %%doc section
- Update BuildRequires

* Mon Jun 05 2006 Jason Vas Dias <jvdias@redhat.com> - 0.07b4-1
- Upgrade to upstream version 0.07b4

* Fri Feb 03 2006 Jason Vas Dias <jvdias@redhat.com> - 0.06-39.2
- rebuild for new perl-5.8.8

* Fri Dec 16 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt for new gcc

* Fri Dec 16 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt for new gcj

* Sat Apr 30 2005 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.06-39
- Source URL: using the Comprehensive Perl Arcana Society Tapestry address
  (Frontier::RPC version 0.06 no longer available in CPAN mirrors).
- spec cleanup (#156480)

* Wed Sep 22 2004 Chip Turner <cturner@redhat.com> 0.06-38
- rebuild

* Tue Aug  6 2002 Chip Turner <cturner@redhat.com>
- automated release bump and build

* Fri Apr  5 2002 Chip Turner <cturner@redhat.com>
- add patch from RHN to allow raw non-conformat calls.
- doesn't affect main code path, but adds functionality
- similar to python xmlrpc module

* Wed Jan 09 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Mon Apr 30 2001 Chip Turner <cturner@redhat.com>
- Spec file was autogenerated.

