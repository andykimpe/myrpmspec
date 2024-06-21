%global tarball libXxf86dga
#global gitdate 20130524
%global gitversion a8dc6be32

Summary: X.Org X11 libXxf86dga runtime library
Name: libXxf86dga
Version: 1.1.4
Release: 2.1%{?gitdate:.%{gitdate}git%{gitversion}}%{?dist}
License: MIT
Group: System Environment/Libraries
URL: http://www.x.org

%if 0%{?gitdate}
Source0:    %{tarball}-%{gitdate}.tar.bz2
Source1:    make-git-snapshot.sh
Source2:    commitid
%else
Source0: ftp://ftp.x.org/pub/individual/lib/%{name}-%{version}.tar.bz2
%endif

Requires: libX11 >= 1.5.99.902

BuildRequires: xorg-x11-util-macros
BuildRequires: autoconf automake libtool
BuildRequires: pkgconfig
BuildRequires: xorg-x11-proto-devel >= 7.4-32
BuildRequires: libX11-devel >= 1.5.99.902
BuildRequires: libXext-devel

%description
X.Org X11 libXxf86dga runtime library

%package devel
Summary: X.Org X11 libXxf86dga development package
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}

%description devel
X.Org X11 libXxf86dga development package

%prep
%setup -q -n %{tarball}-%{?gitdate:%{gitdate}}%{!?gitdate:%{version}}

%build
autoreconf -v --install --force
%configure --disable-static
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p"

# We intentionally don't ship *.la files
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc COPYING README
%{_libdir}/libXxf86dga.so.1
%{_libdir}/libXxf86dga.so.1.0.0

%files devel
%defattr(-,root,root,-)
%{_libdir}/libXxf86dga.so
%{_libdir}/pkgconfig/xxf86dga.pc
%{_mandir}/man3/*.3*
%{_includedir}/X11/extensions/xf86dga1.h
%{_includedir}/X11/extensions/Xxf86dga.h

%changelog
* Wed Feb 12 2014 Adam Jackson <ajax@redhat.com> 1.1.4-2.1
- Mass rebuild

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 1.1.4-2
- Mass rebuild 2013-12-27

* Tue Jun 04 2013 Peter Hutterer <peter.hutterer@redhat.com> 1.1.4-1
- libXxf86dga 1.1.4

* Mon May 27 2013 Peter Hutterer <peter.hutterer@redhat.com> - 1.1.3-6.20130524gita8dc6be32
- Require libX11 1.6RC2 for _XEatDataWords

* Fri May 24 2013 Dave Airlie <airlied@redhat.com> 1.1.3-5.20130524gita8dc6be32
- update to latest git for security fixes (CVE-2013-1991)

* Thu Mar 07 2013 Peter Hutterer <peter.hutterer@redhat.com> - 1.1.3-4
- autoreconf for aarch64

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Mar 08 2012 Adam Jackson <ajax@redhat.com> 1.1.3-1
- libXxf86dga 1.1.3

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Nov 08 2010 Adam Jackson <ajax@redhat.com> 1.1.2-1
- libXxf86dga 1.1.2

* Mon Jul 19 2010 Peter Hutterer <peter.hutterer@redhat.com> 1.1.1-2
- Spec file fixes (#226094)

* Tue Oct 06 2009 Peter Hutterer <peter.hutterer@redhat.com> 1.1.1-1
- libXxf86dga 1.1.1
  Requires xorg-x11-proto-devel for new xf86dgaproto.

* Fri Aug 28 2009 Peter Hutterer <peter.hutterer@redhat.com> 1.0.99.1-1
- libXxf86dga 1.0.99.1

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Jul 23 2009 Adam Jackson <ajax@redhat.com> 1.0.2-5
- Un-require xorg-x11-filesystem

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Jul 15 2008 Adam Jackson <ajax@redhat.com> 1.0.2-3
- Fix license tag.

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.0.2-2
- Autorebuild for GCC 4.3

* Mon Dec 03 2007 Adam Jackson <ajax@redhat.com> 1.0.2-1
- libXxf86dga 1.0.2

* Tue Aug 21 2007 Adam Jackson <ajax@redhat.com> - 1.0.1-4
- Rebuild for build id

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - sh: line 0: fg: no job control
- rebuild

* Fri Jun 09 2006 Mike A. Harris <mharris@redhat.com> 1.0.1-3
- Added "Requires: xorg-x11-proto-devel" to devel package for xxf86dga.pc

* Mon Jun 05 2006 Mike A. Harris <mharris@redhat.com> 1.0.1-2
- Added "BuildRequires: pkgconfig" for (#193507)
- Replace "makeinstall" with "make install DESTDIR=..." for (#192728)

* Thu Apr 27 2006 Adam Jackson <ajackson@redhat.com> 1.0.1-1
- Update to 1.0.1

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 1.0.0-2.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 1.0.0-2.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Mon Jan 23 2006 Mike A. Harris <mharris@redhat.com> 1.0.0-2
- Bumped and rebuilt

* Fri Dec 16 2005 Mike A. Harris <mharris@redhat.com> 1.0.0-1
- Updated libXxf86dga to version 1.0.0 from X11R7 RC4

* Tue Dec 13 2005 Mike A. Harris <mharris@redhat.com> 0.99.3-1
- Updated libXxf86dga to version 0.99.3 from X11R7 RC3
- Added "Requires(pre): xorg-x11-filesystem >= 0.99.2-3", to ensure
  that /usr/lib/X11 and /usr/include/X11 pre-exist.
- Removed 'x' suffix from manpage directories to match RC3 upstream.

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Fri Nov 11 2005 Mike A. Harris <mharris@redhat.com> 0.99.2-1
- Updated libXxf86dga to version 0.99.2 from X11R7 RC2
- Changed 'Conflicts: XFree86-devel, xorg-x11-devel' to 'Obsoletes'
- Changed 'Conflicts: XFree86-libs, xorg-x11-libs' to 'Obsoletes'


* Mon Oct 24 2005 Mike A. Harris <mharris@redhat.com> 0.99.1-1
- Updated libXxf86dga to version 0.99.1 from X11R7 RC1
- Updated file manifest to find manpages in "man3x"

* Thu Sep 29 2005 Mike A. Harris <mharris@redhat.com> 0.99.0-3
- Renamed package to remove xorg-x11 from the name due to unanimous decision
  between developers.
- Use Fedora Extras style BuildRoot tag.
- Disable static library creation by default.
- Add missing defattr to devel subpackage
- Add missing documentation files to doc macro

* Tue Aug 23 2005 Mike A. Harris <mharris@redhat.com> 0.99.0-2
- Renamed package to prepend "xorg-x11" to the name for consistency with
  the rest of the X11R7 packages.
- Added "Requires: %%{name} = %%{version}-%%{release}" dependency to devel
  subpackage to ensure the devel package matches the installed shared libs.
- Added virtual "Provides: lib<name>" and "Provides: lib<name>-devel" to
  allow applications to use implementation agnostic dependencies.
- Added post/postun scripts which call ldconfig.
- Added Conflicts with XFree86-libs and xorg-x11-libs to runtime package,
  and Conflicts with XFree86-devel and xorg-x11-devel to devel package.

* Mon Aug 22 2005 Mike A. Harris <mharris@redhat.com> 0.99.0-1
- Initial build.