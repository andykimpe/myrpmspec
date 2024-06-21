Summary: A library that performs asynchronous DNS operations
Name: c-ares
Version: 1.10.0
Release: 3%{?dist}
License: MIT
Group: System Environment/Libraries
URL: http://c-ares.haxx.se/
Source0: http://c-ares.haxx.se/c-ares-%{version}.tar.gz
Source1: LICENSE
Patch0: 0001-Use-RPM-compiler-options.patch
Patch1: c-ares-1.10.0-multilib.patch
Patch2: 0003-host_callback-Fall-back-to-AF_INET-on-searching-with.patch
Patch3: 0004-Don-t-override-explicitly-specified-search-domains.patch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires: autoconf
BuildRequires: automake
BuildRequires: libtool

%description
c-ares is a C library that performs DNS requests and name resolves 
asynchronously. c-ares is a fork of the library named 'ares', written 
by Greg Hudson at MIT.

%package devel
Summary: Development files for c-ares
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: pkgconfig

%description devel
This package contains the header files and static libraries needed to
compile applications or shared objects that use c-ares.

%prep
%setup -q
%patch0 -p1 -b .optflags
%patch1 -p1 -b .multilib
%patch2 -p1 -b .fallback
%patch3 -p1 -b .searchdom

cp %{SOURCE1} .
f=CHANGES ; iconv -f iso-8859-1 -t utf-8 $f -o $f.utf8 ; mv $f.utf8 $f

%build
autoreconf -if
%configure --enable-shared --disable-static \
           --disable-dependency-tracking
%{__make} %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install
rm -f $RPM_BUILD_ROOT/%{_libdir}/libcares.la

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-, root, root)
%doc README README.cares CHANGES NEWS LICENSE
%{_libdir}/*.so.*

%files devel
%defattr(-, root, root, 0755)
%{_includedir}/ares.h
%{_includedir}/ares_build.h
%{_includedir}/ares_dns.h
%{_includedir}/ares_rules.h
%{_includedir}/ares_version.h
%{_libdir}/*.so
%{_libdir}/pkgconfig/libcares.pc
%{_mandir}/man3/ares_*

%changelog
* Thu Jul 24 2014 Jakub Hrozek <jhrozek@redhat.com> - 1.10.0-3
- Fall back to AF_INET when ares_gethostbyname() is called with AF_UNSPEC
- Only set search domains from /etc/resolv.conf if there isn't a value
  already present in the channel (David Drisdale)
- Related: rhbz#1077544 - Rebase c-ares to version 1.10

* Tue May 20 2014 Jakub Hrozek <jhrozek@redhat.com> - 1.10.0-2
- Run autoreconf during build
- Related: rhbz#1077544 - Rebase c-ares to version 1.10

* Thu Apr  3 2014 Jakub Hrozek <jhrozek@redhat.com> - 1.10.0-1
- Rebase c-ares to 1.10
- Resolves: rhbz#1077544 - Rebase c-ares to version 1.10

* Sat Mar  3 2012 Jakub Hrozek <jhrozek@redhat.com> - 1.7.0-6
- Only fall back to AF_INET searches when looking for AF_UNSPEC
  addresses (#730695)
- Do not leak memory in ares_parse_a_reply when parsing an invalid
  record (#730693)
- Add a missing break (#713133) - reported and patched by Michal Luscon
- Fix a SIGBUS when resolving SRV queries on architectures that do
  not support unaligned memory access (#695426)
- Amend the ares_gethostbyname manpage so that it lists ARES_ENODATA as
  an allowed return code (#640944)

* Mon Jun  7 2010 Jakub Hrozek <jhrozek@redhat.com> - 1.7.0-5
- Actually apply patch for rhbz#597287

* Mon Jun  7 2010 Jakub Hrozek <jhrozek@redhat.com> - 1.7.0-4
- Fix multilib conflict
- Resolves: rhbz#604131

* Mon Jun  7 2010 Jakub Hrozek <jhrozek@redhat.com> - 1.7.0-3
- Use last instance of search/domain, not the first one
- Resolves: rhbz#597287

* Wed Mar  3 2010 Jakub Hrozek <jhrozek@redhat.com> - 1.7.0-2
- Add a patch to allow usage of IPv6 nameservers
  (upstream revisions 1199,1201,1202)
- Resolves: rhbz#560116

* Tue Dec  1 2009 Tom "spot" Callaway <tcallawa@redhat.com> - 1.7.0-1
- update to 1.7.0

* Sat Jul 25 2009 Ville Skyttä <ville.skytta at iki.fi> - 1.6.0-3
- Patch to make upstream build system honor our CFLAGS and friends.
- Don't bother building throwaway static libs.
- Disable autotools dependency tracking for cleaner build logs and possible
  slight build speedup.
- Convert docs to UTF-8.
- Update URLs.

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Jul 22 2009 Tom "spot" Callaway <tcallawa@redhat.com> - 1.6.0-1
- update to 1.6.0

* Mon Feb 23 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Sep 12 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.5.3-1
- update to 1.5.3

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.5.1-2
- Autorebuild for GCC 4.3

* Tue Feb 19 2008 Tom "spot" Callaway <tcallawa@redhat.com> 1.5.1-1
- update to 1.5.1

* Thu Aug 23 2007 Tom "spot" Callaway <tcallawa@redhat.com> 1.4.0-2
- rebuild for ppc32

* Wed Jun 27 2007 Tom "spot" Callaway <tcallawa@redhat.com> 1.4.0-1
- bump to 1.4.0 (resolves bugzilla 243591)
- get rid of static library (.a)

* Wed Jan 17 2007 Tom "spot" Callaway <tcallawa@redhat.com> 1.3.2-1
- bump to 1.3.2

* Mon Sep 11 2006 Tom "spot" Callaway <tcallawa@redhat.com> 1.3.1-2
- FC-6 bump

* Mon Jul 10 2006 Tom "spot" Callaway <tcallawa@redhat.com> 1.3.1-1
- bump to 1.3.1

* Tue Feb 28 2006 Tom "spot" Callaway <tcallawa@redhat.com> 1.3.0-2
- bump for FC-5 rebuild

* Sun Sep  4 2005 Tom "spot" Callaway <tcallawa@redhat.com> 1.3.0-1
- include LICENSE text
- bump to 1.3.0

* Tue May 31 2005 Tom "spot" Callaway <tcallawa@redhat.com> 1.2.1-4
- use dist tag to prevent EVR overlap

* Fri Apr 22 2005 Tom "spot" Callaway <tcallawa@redhat.com> 1.2.1-2
- fix license (MIT, not LGPL)
- get rid of libcares.la

* Fri Apr 22 2005 Tom "spot" Callaway <tcallawa@redhat.com> 1.2.1-1
- initial package creation

