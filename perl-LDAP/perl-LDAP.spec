Name:           perl-LDAP
Version:        0.40
Release:        3%{?dist}
Epoch:          1
Summary:        LDAP Perl module

Group:          Development/Libraries
License:        GPL+ or Artistic
URL:            http://search.cpan.org/dist/perl-ldap/
Source0:        http://www.cpan.org/authors/id/G/GB/GBARR/perl-ldap-%{version}.tar.gz
# Do not set SSL ciphers at all by default, bug #1090966, CPAN RT#95001,
# in upstream 0.63
Patch0:         perl-ldap-0.40-Do-not-set-SSL_ciphers-to-ALL-by-default.patch
# Correct Do-not-set-SSL_ciphers-to-ALL-by-default patch, bug #1090966,
# in upstream 0.64
Patch1:         perl-ldap-0.40-LDAP.pm-set-SSL_cipher_list-to-correct-value.patch
# Pass actual length to syswrite() instead of default 1500 B, bug #1104069,
# CPAN RT#96203, in upstream 0.64
Patch2:         perl-ldap-0.40-RT-96203-LDAP.pm-use-correct-length-for-syswrite.patch
# Correct misspellings in the documentation, bug #1286228, CPAN RT#118254
Patch3:         perl-ldap-0.40-Correct-misspellings.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
BuildRequires:  perl(Convert::ASN1)
BuildRequires:  perl(Test::More)
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
Requires:       perl(IO::Socket::SSL)
# Recommended requires
Requires:       perl(Authen::SASL)
Requires:       perl(MIME::Base64)
Requires:       perl(IO::Socket::SSL)
Requires:       perl(URI::ldap)
Requires:       perl(XML::SAX::Writer)


%description
Net::LDAP is a collection of modules that implements a LDAP services API
for Perl programs. The module may be used to search directories or perform
maintenance functions such as adding, deleting or modifying entries.


%prep
%setup -q -n perl-ldap-%{version}
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
chmod -c 644 bin/* contrib/* lib/Net/LDAP/DSML.pm
%{__perl} -pi -e 's|^#!/usr/local/bin/perl\b|#!%{__perl}|' contrib/*

# Filter unwanted Provides:
cat << \EOF > %{name}-prov
#!/bin/sh
%{__perl_provides} $* |\
  sed -e '/perl(Net::LDAP::Filter)$/d'
EOF

%define __perl_provides %{_builddir}/perl-ldap-%{version}/%{name}-prov
chmod +x %{__perl_provides}

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor < /dev/null
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make pure_install PERL_INSTALL_ROOT=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type d -depth -exec rmdir {} 2>/dev/null ';'
chmod -R u+w $RPM_BUILD_ROOT/*

%check
make test
 
%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc Changes CREDITS
%doc contrib/ bin/
%{perl_vendorlib}/Bundle/
%{perl_vendorlib}/LWP/
%{perl_vendorlib}/Net/
%{_mandir}/man3/*.3pm*


%changelog
* Tue Oct 04 2016 Petr Pisar <ppisar@redhat.com> - 1:0.40-3
- Correct misspellings in the documentation (bug #1286228)

* Thu Nov 19 2015 Petr Pisar <ppisar@redhat.com> - 1:0.40-2
- Do not set SSL ciphers at all by default (bug #1090966)
- Pass actual length to syswrite() instead of default 1500 B (bug #1104069)

* Mon Jun  7 2010 Marcela Mašláňová <mmaslano@redhat.com> - 1:0.40-1
- update to 0.40, add recommended requires
- Resolves: rhbz#594771

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 1:0.34-7
- rebuild against perl 5.10.1

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.34-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.34-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Mar 06 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1:0.34-4
- rebuild for new perl

* Mon Apr 09 2007 Robin Norwood <rnorwood@redhat.com> - 1:0.34-3
- Resolves: bz#226267
- Only filter out the unversioned Provides: perl(Net::LDAP::Filter) to
  avoid breaking dependencies.

* Thu Apr 05 2007 Robin Norwood <rnorwood@redhat.com> - 1:0.34-2
- Resolves: bz#226267
- Filter out provides perl(Net::LDAP::Filter) per package review.

* Tue Feb 13 2007 Robin Norwood <rnorwood@redhat.com> - 1:0.34-1
- New version: 0.34

* Wed Sep 27 2006 Robin Norwood <rnorwood@redhat.com> - 1:0.33-3
- Bugzilla: 207430
- Incorporate fixes from Jose Oliveira's patch
- Add perl(IO::Socket::SSL) as a BuildRequires as well
- Other cleanups from Jose

* Wed Sep 27 2006 Robin Norwood <rnorwood@redhat.com> - 0.33-1.3
- Add a requirement for IO::Socket::SSL, per bug #122066

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - sh: line 0: fg: no job control
- rebuild

* Fri Feb 03 2006 Jason Vas Dias <jvdias@redhat.com> - 0.33-1.2
- rebuild for new perl-5.8.8

* Fri Dec 16 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt for new gcc

* Tue Apr 26 2005 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.33-1
- Update to 0.33.

* Sat Apr 02 2005 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0.3202-1
- Update to 0.3202.
- Specfile cleanup. (#153766)

* Wed Sep 22 2004 Chip Turner <cturner@redhat.com> 0.31-5
- rebuild

* Wed Mar 10 2004 Chip Turner <cturner@redhat.com> - 0.31-1
- Specfile autogenerated.
