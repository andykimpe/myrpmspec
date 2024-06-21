Summary:        Library providing low-level IEEE-1394 access
Name:           libraw1394
Version:        2.0.4
Release:        1%{?dist}
License:        LGPLv2+
Group:          System Environment/Libraries
Source:         http://www.kernel.org/pub/linux/libs/ieee1394/%{name}-%{version}.tar.bz2
URL:            http://www.dennedy.org/libraw1394/
ExcludeArch:    s390 s390x
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  autoconf automake libtool kernel-headers

%description
The libraw1394 library provides direct access to the IEEE-1394 bus through
the Linux 1394 subsystem's raw1394 user space interface. Support for both
the classic ieee1394 and new firewire linux driver stacks is included, with
run-time detection of the active stack. Fedora comes with the firewire stack
by default.

%package devel
Summary:       Development libs for libraw1394
Group:         Development/Libraries
Requires:      %{name} = %{version}-%{release}, pkgconfig

%description devel
Development libraries needed to build applications against libraw1394.

%prep
%setup -q

%build
%configure --disable-static
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT%{_libdir}/libraw1394.la

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,0755)
%doc COPYING.LIB README NEWS
%{_bindir}/dumpiso
%{_bindir}/sendiso
%{_bindir}/testlibraw
%{_libdir}/libraw1394.so.*
%{_mandir}/man1/dumpiso.1.gz
%{_mandir}/man1/sendiso.1.gz
%{_mandir}/man1/testlibraw.1.gz
%{_mandir}/man5/isodump.5.gz

%files devel
%defattr(-,root,root,0755)
%doc doc/libraw1394.sgml
%{_includedir}/libraw1394/
%{_libdir}/libraw1394.so
%{_libdir}/pkgconfig/libraw1394.pc


%changelog
* Thu Sep 17 2009 Jarod Wilson <jarod@redhat.com> - 2.0.4-1
- Update to libraw1394 v2.0.4 release
- Point to new download location and project page

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Jan 15 2009 Jarod Wilson <jarod@redhat.com> - 2.0.1-1
- Update to libraw1394 v2.0.1 release

* Tue Jan 13 2009 Jarod Wilson <jarod@redhat.com> - 2.0.0-6
- Set errno = ENOSYS for all unimplemented functions
- Make dvgrab and friends work w/o requiring r/w on the local fw node (#441073)

* Mon Dec 08 2008 Jarod Wilson <jarod@redhat.com> - 2.0.0-5
- Fix up iso stop command so starting/stopping/starting iso reception works
- Plug firewire handle leak

* Fri Dec 05 2008 Jarod Wilson <jarod@redhat.com> - 2.0.0-4
- Fix channel modify code, should make iso reception work reliably now

* Thu Nov 20 2008 Jarod Wilson <jarod@redhat.com> - 2.0.0-3
- Address some compiler warnings
- Reduce nesting depth in new_handle dispatches
- Fix segfault in handle_arm_request

* Wed Oct 01 2008 Jarod Wilson <jarod@redhat.com> - 2.0.0-2
- Misc fixes from Erik Hovland, based on coverity prevent analysis

* Fri Jul 18 2008 Jarod Wilson <jwilson@redhat.com> - 2.0.0-1
- Update to libraw1394 v2.0.0 release

* Mon Jun 23 2008 Jarod Wilson <jwilson@redhat.com> - 2.0.0-0.2.20080430_git
- Restore ieee1394 raw1394_read_cycle_timer, add firewire variant

* Tue Jun 17 2008 Jarod Wilson <jwilson@redhat.com> - 2.0.0-0.1.20080430_git
- Update to pre-2.0.0 git tree, which features merged "juju" firewire
  stack support, enabled simultaneously with classic ieee1394 support

* Tue Jun 17 2008 Jarod Wilson <jwilson@redhat.com> - 1.3.0-7
- Fully initialize data structures and plug dir leak. Resolves
  crashes when used with kino (Philippe Troin, #451727)

* Mon Apr 28 2008 Jarod Wilson <jwilson@redhat.com> - 1.3.0-6
- Unmap the correct memory range on iso receive teardown, fixes
  segfault on exit from dvgrab (Mladen Kuntner, #444354)

* Tue Feb 26 2008 Jarod Wilson <jwilson@redhat.com> - 1.3.0-5
- Update license and kill an errant tab (#226039)

* Wed Jan 30 2008 Jarod Wilson <jwilson@redhat.com> - 1.3.0-4
- Use firewire-cdev.h provided by kernel-headers

* Wed Oct 24 2007 Jarod Wilson <jwilson@redhat.com> - 1.3.0-3
- Update firewire-cdev.h to match kernel and eliminate
  bitfield usage, fixes capture on big-endian systems (#345221)

* Fri Oct 19 2007 Jarod Wilson <jwilson@redhat.com> - 1.3.0-2
- Fix the 'double free' crash on shutdown (#328011)

* Thu Oct 18 2007 Jarod Wilson <jwilson@redhat.com> - 1.3.0-1
- libraw1394 v1.3.0

* Wed Aug 29 2007 Fedora Release Engineering <rel-eng at fedoraproject dot org> - 1.2.1-10
- Rebuild for selinux ppc32 issue.

* Fri Jun 15 2007 Jarod Wilson <jwilson@redhat.com> - 1.2.1-9
- Drop Conficts, causes interesting issues if people have an
  older kernel installed and/or kernel-xen installed (#244474)

* Thu Jun 14 2007 Jarod Wilson <jwilson@redhat.com> - 1.2.1-8
- Switch kernel Requires to a Conflicts so we don't end up pulling
  kernels into build chroot, and bump to GA kernel ver (#244128)

* Wed Apr 18 2007 Kristian Høgsberg <krh@redhat.com> - 1.2.1-7
- Update firewire-cdev.h again to get the iso context create ioctl changes.
- Bump kernel requires accordingly.

* Tue Apr 17 2007 Kristian Høgsberg <krh@redhat.com> - 1.2.1-6
- Update to latest ioctl changes.

* Thu Apr 12 2007 Kristian Høgsberg <krh@redhat.com> - 1.2.1-5
- Make rawiso support actually work.
- Update fw-device-cdev.h to sync with latest kernel patch.
- Add Requires to pull in a recent enough kernel.

* Tue Apr  3 2007 Kristian Høgsberg <krh@redhat.com> - 1.2.1-4
- Update juju patch with rawiso support.

* Mon Mar 19 2007 Kristian Høgsberg <krh@redhat.com> 1.2.1-3
- Add support for new stack (juju).

* Sun Feb 04 2007 Jarod Wilson <jwilson@redhat.com> - 1.2.1-2
- Minor spec cleanups for Core/Extras merger (#226039)

* Wed Jul 12 2006 Jarod Wilson <jwilson@redhat.com> - 1.2.1-1
- update to 1.2.1
- use %%dist tag

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 1.2.0-3.fc5.2.1
- rebuild

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 1.2.0-3.fc5.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 1.2.0-3.fc5.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Tue Dec 13 2005 Warren Togami <wtogami@redhat.com> - 1.2.0-3
- disable static and remove .la (#172642)

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Fri Nov 11 2005 Warren Togami <wtogami@redhat.com> - 1.2.0-2
- spec fixes from Matthias (#172105)

* Fri Jul 22 2005 Warren Togami <wtogami@redhat.com> - 1.2.0-1
- 1.2.0

* Wed Mar 16 2005 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Mon Feb 28 2005 Warren Togami <wtogami@redhat.com. 1.1.0-2
- gcc4 rebuild

* Sun Feb 06 2005 Warren Togami <wtogami@redhat.com> 1.1.0-1
- 1.1.0

* Thu Jul 15 2004 Tim Waugh <twaugh@redhat.com> 0.10.1-3
- Fixed warnings in shipped m4 file.

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Mon Apr 05 2004 Warren Togami <wtogami@redhat.com> 0.10.1-1
- 0.10.1, license LGPL

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Sat Feb 21 2004 Florian La Roche <Florian.LaRoche@redhat.de>
- add symlinks to shared libs already at install time

* Thu Feb 12 2004 Warren Togami <wtogami@redhat.com> 0.10.0-1
- upgrade to 0.10.0
- Spec cleanups
- Remove INSTALL, add NEWS
- Add new binaries
- libtool, auto* not needed

* Mon Aug 25 2003 Bill Nottingham <notting@redhat.com> 0.9.0-12
- have -devel require main pacakge

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Thu May 22 2003 Jeremy Katz <katzj@redhat.com> 0.9.0-10
- fix build with gcc 3.3

* Mon Feb 17 2003 Elliot Lee <sopwith@redhat.com>
- ppc64 fix

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Wed Nov 20 2002 Florian La Roche <Florian.LaRoche@redhat.de>
- exclude mainframe
- allow lib64

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Wed Jun 19 2002 Michael Fulbright <msf@redhat.com>
- fixed up %%files list for devel subpackage and included api docs

* Sun Jun 09 2002 Michael Fulbright <msf@redhat.com>
- First RPM build

