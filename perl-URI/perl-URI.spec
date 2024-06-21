Name:           perl-URI
Version:        1.40
Release:        2%{?dist}
Summary:        A Perl module implementing URI parsing and manipulation

Group:          Development/Libraries
License:        GPL+ or Artistic
URL:            http://search.cpan.org/dist/URI/
Source0:        http://www.cpan.org/authors/id/G/GA/GAAS/URI-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
BuildRequires:  perl(MIME::Base64)
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(Test::More)
BuildRequires:  perl(Business::ISBN)
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))


%description
This module implements the URI class. Objects of this class represent
"Uniform Resource Identifier references" as specified in RFC 2396 (and
updated by RFC 2732).


%prep
%setup -q -n URI-%{version}
chmod 644 uri-test

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make pure_install PERL_INSTALL_ROOT=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type d -depth -exec rmdir {} 2>/dev/null ';'
chmod -R u+w $RPM_BUILD_ROOT/*

for file in Changes; do
  iconv -f iso-8859-1 -t utf-8 < "$file" > "${file}_"
  mv -f "${file}_" "$file"
done


%check
make test


%clean 
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc Changes README rfc2396.txt uri-test
%{perl_vendorlib}/URI*
%{_mandir}/man3/*.3*


%changelog
* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 1.40-2
- rebuild against perl 5.10.1

* Tue Oct  6 2009 Marcela Mašláňová <mmaslano@redhat.com> - 1.40-1
- update to new upstream release

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.37-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.37-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Feb 20 2009 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.37-1
- Upstream update.
- Add BR: perl(Test::More), perl(Business::ISBN).
- Remove requires-filter.

* Wed Feb 27 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.35-8
- Rebuild for perl 5.10 (again)

* Wed Feb 13 2008 Robin Norwood <rnorwood@redhat.com> - 1.35-7
- rebuild again for new perl

* Wed Feb 13 2008 Robin Norwood <rnorwood@redhat.com> - 1.35-6
- Last update for package review

* Thu Jan 24 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.35-5
- rebuild for new perl

* Thu Oct 25 2007 Robin Norwood <rnorwood@redhat.com> - 1.35-4
- Fix various package review issues:
- Remove redundant BR: perl
- remove "|| :" from %%check
- move requires filter into spec file
- remove tabs and fix spacing

* Wed Oct 17 2007 Tom "spot" Callaway <tcallawa@redhat.com> - 1.35-3.1
- correct license tag
- add BR: perl(ExtUtils::MakeMaker)

* Mon Jun 05 2006 Jason Vas Dias <jvdias@redhat.com> - 1.35-3
- fix License: tag

* Fri Feb 03 2006 Jason Vas Dias <jvdias@redhat.com> - 1.35-2.2
- rebuild for new perl-5.8.8

* Fri Dec 16 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt for new gcc

* Fri Dec 16 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt for new gcj

* Sat Apr 02 2005 Jose Pedro Oliveira <jpo at di.uminho.pt> - 1.35-2
- Update to 1.35.
- Spec cleanup (#153205)

* Thu Sep 23 2004 Chip Turner <cturner@redhat.com> 1.30-3
- rebuild

* Wed Sep 22 2004 Chip Turner <cturner@redhat.com> 1.30-2
- rebuild

* Fri Feb 13 2004 Chip Turner <cturner@redhat.com> 1.30-1
- update to 1.30

* Tue Aug  6 2002 Chip Turner <cturner@redhat.com>
- automated release bump and build

* Tue Aug  6 2002 Chip Turner <cturner@localhost.localdomain>
- update to 1.21

* Tue Jun  4 2002 Chip Turner <cturner@redhat.com>
- properly claim directories owned by package so they are removed when package is removed

* Wed Jan 09 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Fri Dec 7 2001 root <root@redhat.com>
- Spec file was autogenerated. 