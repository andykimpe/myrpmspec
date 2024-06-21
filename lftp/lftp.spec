Summary:	A sophisticated file transfer program
Name:		lftp
Version:	4.0.9
Release:	15%{?dist}
License:	GPLv3+
Group:		Applications/Internet
Source0:	ftp://ftp.yar.ru/lftp/lftp-%{version}.tar.lzma
URL:		http://lftp.yar.ru/
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:	ncurses-devel, gnutls-devel, pkgconfig, readline-devel, gettext

Patch1:		lftp-4.0.9-buf-overflow.patch
Patch2:		lftp-4.0.9-conn-err.patch
Patch3:		lftp-4.0.9-ascii_hang.patch
Patch4:		lftp-4.0.9-overwrite.patch
Patch5:		lftp-4.0.9-auto-rename-option-man.patch
Patch6:		lftp-4.0.9-mirror302.patch
Patch7:		lftp-4.0.9-help-exitcode.patch
Patch8:		lftp-4.0.9-mirror302-2.patch
# Commits: https://github.com/lavv17/lftp/commit/0cbe1516e48aa13ad2a684ad72fc9ac4fb3055a0
#          https://github.com/lavv17/lftp/commit/f8ee088ee909c9d93b3a75a5ddd0ab954edd9619
#          https://github.com/lavv17/lftp/commit/132017e4c49b66cc8bf05178ad9c405a670d1b9b
#          https://github.com/lavv17/lftp/commit/d4a865fae0dbc3e4b1ea77820969d1675890e8cc
# BZ: https://bugzilla.redhat.com/show_bug.cgi?id=1305235
# Fixed in: lftp 4.4.6
Patch9:		lftp-4.0.9-follow-symlink.patch
# Commits: https://github.com/lavv17/lftp/commit/32f73ba41246c94e29573f057dfcc767d6d87dab
#          https://github.com/lavv17/lftp/commit/8c8ac2fd5030db8455cc451356e802da0c5ec183
# BZ: https://bugzilla.redhat.com/show_bug.cgi?id=1305235
Patch10:	lftp-4.0.9-follow-symlink-attrs.patch
# Commits: https://github.com/lavv17/lftp/commit/f42e2d62a3dddc7df0daf6adf05ab4c5e4c1f33b?diff=unified
# BZ: https://bugzilla.redhat.com/show_bug.cgi?id=1228484
# Fixed in: 4.7.3
Patch11:	lftp-4.0.9-mirror_hang.patch
#BZ: https://bugzilla.redhat.com/show_bug.cgi?id=1364524
Patch12:	lftp-4.0.9-size-loop.patch
# Commit:	https://github.com/lavv17/lftp/commit/b406805d2b3d4c9a88e24363980e5717e61d0948
# BZ: 		https://bugzilla.redhat.com/show_bug.cgi?id=1363629
# Fixed in:	4.6
Patch13:	lftp-4.0.9-ssl-tls-restrict.patch
# Commits: 	https://github.com/lavv17/lftp/commit/1150a445552973a52ff640cfda9062bcc38f4934
# BZ: 		https://bugzilla.redhat.com/show_bug.cgi?id=1208219
# Fixed in: 	4.7.3
Patch14:	lftp-4.0.9-fail-exit-doc.patch
# BZ:		https://bugzilla.redhat.com/show_bug.cgi?id=1320721
# Fixed in:	4.7.3
Patch15:	lftp-4.0.9-mirror-segfault.patch
# Commit: https://github.com/lavv17/lftp/commit/f2f2bb91e4ad9a4e8a6eb74b557bac04f505b872
# Fixed in: 4.4.10
Patch16:        lftp-4.0.9-mirror-array-info-hang.patch
# Commit: https://github.com/lavv17/lftp/commit/f7f78542f96700761ef498b9dc9787c6a6ad479a
# Fixed in: 4.4.6
Patch17:	lftp-4.0.9-mirror-crash.patch


%description
LFTP is a sophisticated ftp/http file transfer program. Like bash, it has job
control and uses the readline library for input. It has bookmarks, built-in
mirroring, and can transfer several files in parallel. It is designed with
reliability in mind.

%package scripts
Summary:	Scripts for lftp
Group:		Applications/Internet
Requires:	lftp >= %{version}-%{release}
BuildArch:	noarch

%description scripts
Utility scripts for use with lftp.

%prep
%setup -q
%patch1 -p1 -b .buf-overflow
%patch2 -p1 -b .conn-err
%patch3 -p1 -b .ascii_hang
%patch4 -p1 -b .overwrite
%patch5 -p1 -b .autorename_man
%patch6 -p1 -b .mirror302
%patch7 -p1 -b .help_exit
%patch8 -p1 -b .mirror302-2
%patch9 -p1 -b .follow_symlink
%patch10 -p1 -b .follow_symlink_attr
%patch11 -p1 -b .mirror_hang
%patch12 -p1 -b .size-loop
%patch13 -p1 -b .ssl-tls-restrict
%patch14 -p1 -b .fail-exit-doc
%patch15 -p1 -b .mirror-segfault
%patch16 -p1 -b .mirror-array-info-hang
%patch17 -p1 -b .mirror-crash


#sed -i.rpath -e '/lftp_cv_openssl/s|-R.*lib||' configure
sed -i.norpath -e \
	'/sys_lib_dlsearch_path_spec/s|/usr/lib |/usr/lib /usr/lib64 /lib64 |' \
	configure

%build
%configure --with-modules --disable-static --with-gnutls --without-openssl --with-debug
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
export tagname=CC
make DESTDIR=$RPM_BUILD_ROOT INSTALL='install -p' install
chmod 0755 $RPM_BUILD_ROOT%{_libdir}/lftp/*
chmod 0755 $RPM_BUILD_ROOT%{_libdir}/lftp/%{version}/*.so
iconv -f ISO88591 -t UTF8 NEWS -o NEWS.tmp
touch -c -r NEWS NEWS.tmp
mv NEWS.tmp NEWS
# Remove files from $RPM_BUILD_ROOT that we aren't shipping.
#rm $RPM_BUILD_ROOT%{_libdir}/lftp/%{version}/*.la
rm $RPM_BUILD_ROOT%{_libdir}/liblftp-jobs.la
rm $RPM_BUILD_ROOT%{_libdir}/liblftp-tasks.la
rm $RPM_BUILD_ROOT%{_libdir}/liblftp-jobs.so
rm $RPM_BUILD_ROOT%{_libdir}/liblftp-tasks.so

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files -f %{name}.lang
%defattr(-,root,root,-)
%doc BUGS COPYING ChangeLog FAQ FEATURES README* NEWS THANKS TODO
%config(noreplace) %{_sysconfdir}/lftp.conf
%{_bindir}/*
%{_mandir}/*/*
%dir %{_libdir}/lftp
%dir %{_libdir}/lftp/%{version}
%{_libdir}/lftp/%{version}/cmd-torrent.so
%{_libdir}/lftp/%{version}/cmd-mirror.so
%{_libdir}/lftp/%{version}/cmd-sleep.so
%{_libdir}/lftp/%{version}/liblftp-network.so
%{_libdir}/lftp/%{version}/liblftp-pty.so
%{_libdir}/lftp/%{version}/proto-file.so
%{_libdir}/lftp/%{version}/proto-fish.so
%{_libdir}/lftp/%{version}/proto-ftp.so
%{_libdir}/lftp/%{version}/proto-http.so
%{_libdir}/lftp/%{version}/proto-sftp.so
%{_libdir}/liblftp-jobs.so.*
%{_libdir}/liblftp-tasks.so.*

%files scripts
%defattr(-,root,root,-)
%{_datadir}/lftp


%changelog
* Tue Jan 02 2018 Michal Ruprich <mruprich@redhat.com> - 4.0.9-15
- Resolves: #1487631 - lftp crash when mirroring a repository

* Tue Dec 13 2016 Michal Ruprich <mruprich@redhat.com> - 4.0.9-14
- Related: #1228484 - lftp hangs after dowloading one file during a mirror
- Related: #1305235 - lftp not following symlinks through sftp

* Tue Oct 18 2016 Michal Ruprich - 4.0.9-13
- Resolves: #1320721 - lftp crash when mirroring over a http proxy

* Tue Oct 04 2016 Michal Ruprich - 4.0.9-12
- Resolves: #1208219 - Misleading documentation for cmd:fail-exit 

* Tue Oct 04 2016 mruprich <mruprich@redhat.com> - 4.0.9-11
- Resolves: #1363629 - Unable to do TLSv1.2 negotiation with LFTP and GNUTLS 

* Tue Oct 04 2016 mruprich <mruprich@redhat.com> - 4.0.9-10
- Resolves: #1364524 -  lftp command SIZE on non-existing file is executed in a loop instead of return

* Tue Aug 30 2016 mruprich <mruprich@redhat.com> - 4.0.9-9
- Resolves: #1228484 - lftp hangs after dowloading one file during a mirror

* Wed Jun 29 2016 Luboš Uhliarik <luhliari@redhat.com> - 4.0.9-8
- Related: #1305235 - lftp not following symlinks through sftp

* Mon Jun 06 2016 Luboš Uhliarik <luhliari@redhat.com> - 4.0.9-7
- Resolves: #1305235 - lftp not following symlinks through sftp

* Wed Apr 01 2015 Tomas Hozza <thozza@redhat.com> - 4.0.9-6
- Fix lftp to follow 302 redirect if the new Location is full URL (#928307)

* Thu Feb 19 2015 Tomas Hozza <thozza@redhat.com> - 4.0.9-5
- Fix help command exit code (#1193617)

* Tue Jan 13 2015 Tomas Hozza <thozza@redhat.com> - 4.0.9-4
- Fix lftp to follow http redirect (302) in mirror mode (#928307)

* Tue Dec 02 2014 Tomas Hozza <thozza@redhat.com> - 4.0.9-3
- Fix lftp to try also other addresses if connecting to first fails (#732863)
- Fix lftp hang when using ascii mode with sftp (#842322)
- Fix lftp to overwrite filename when auto-rename and clobber are enabled (#619777)
- Add description of xfer:auto-rename into man page (#674875)

* Mon Feb 03 2014 Jiri Skala <jskala@redhat.com> - 4.0.9-2
- Resolves: #915740 - lftp crashes with buffer overflow

* Tue Jun 15 2010 Jiri Skala <jskala@redhat.com> - 4.0.9-1
- Resolves: #602838 - CVE-2010-2251 lftp: multiple HTTP client download filename vulnerability
- re-base to latest upstream version

* Tue Mar 16 2010 Jiri Skala <jskala@redhat.com> - 4.0.4-2
- Resolves: #574041 - lftp doesn't properly implement CCC

* Mon Nov 23 2009 Jiri Skala <jskala@redhat.com> - 4.0.4-1
- updated to latest stable version due to bug fixes

* Mon Sep 14 2009 Jiri Skala <jskala@redhat.com> - 4.0.0-1
- updated to latest stable version

* Wed Sep 02 2009 Jiri Skala <jskala@redhat.com> - 3.7.15-1
- updated to latest upstream release

* Wed Aug 12 2009 Ville Skyttä <ville.skytta@iki.fi> - 3.7.14-6
- Use lzma compressed upstream tarball.

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.7.14-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Jul 20 2009 Adam Jackson <ajax@redhat.com> 3.7.14-4
- Split utility scripts to subpackage to isolate perl dependency. (#510813)

* Wed Jun 10 2009 Jiri Skala <jskala@redhat.com> - 3.7.14-3
- fixed bug in ls via http - corrupted file names containing spaces

* Fri May 22 2009 Jiri Skala <jskala@redhat.com> - 3.7.14-1
- rebase to latest upstream release; among others fixes #474413

* Tue Apr 14 2009 Jiri Skala <jskala@redhat.com> - 3.7.11-3
- release number repaired

* Tue Apr 14 2009 Jiri Skala <jskala@redhat.com> - 3.7.11-1
- rebase to latest upstream release

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.7.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Jan 14 2009 Jiri Skala <jskala@redhat.com> - 3.7.7-1
- rebase to latest upstream version
- resolves license conflict GPLv2 -> GPLv3+ due to gnulib

* Mon Sep 29 2008 Jiri Skala <jskala@redhat.com> - 3.7.4-1
- Resolves: #464420 re-base to 3.7.4
- replaced usage of OpenSSL by GNUTLS due to license conflict

* Wed Apr 23 2008 Martin Nagy <mnagy@redhat.com> - 3.7.1-1
- update to upstream version 3.7.1

* Thu Feb 28 2008 Martin Nagy <mnagy@redhat.com> - 3.6.3-2
- fix rpath

* Mon Feb 25 2008 Martin Nagy <mnagy@redhat.com> - 3.6.3-1
- update to newest version
- remove patches fixed in upstream: progress_overflow, empty_argument

* Tue Feb 12 2008 Martin Nagy <mnagy@redhat.com> - 3.6.1-2
- fix library paths (#432468)

* Mon Feb 11 2008 Martin Nagy <mnagy@redhat.com> - 3.6.1-1
- upgrade to upstream version 3.6.1
- remove rpath and make some spec file changes for review (#225984)
- remove old patches
- fix core dumping when html tag has its argument empty
- use own libtool

* Thu Dec 13 2007 Martin Nagy <mnagy@redhat.com> - 3.5.14-3
- Fixed coredumping when downloading (#414051)

* Tue Dec 04 2007 Martin Nagy <mnagy@redhat.com> - 3.5.14-2.1
- rebuild

* Mon Sep 17 2007 Maros Barabas <mbarabas@redhat.com> - 3.5.14-2
- rebase
- deleted symlinks liblftp-jobs.so & liblftp-tasks.so

* Thu Sep 06 2007 Maros Barabas <mbarabas@redhat.com> - 3.5.10-4
- rebuild

* Wed Apr 11 2007 Maros Barabas <mbarabas@redhat.com> - 3.5.10-3
- Correct mistake removing devel package & calling chkconfig
- Resolves #235436
- Removing automake autoconf
- Resolves #225984

* Wed Apr 04 2007 Maros Barabas <mbarabas@redhat.com> - 3.5.10-2
- Merge review fix
- Resolves #225984

* Wed Apr 04 2007 Maros Barabas <mbarabas@redhat.com> - 3.5.10
- Upgrade to 3.5.10 from upstream

* Thu Jan 18 2007 Maros Barabas <mbarabas@redhat.com> - 3.5.9
- Upgrade to 3.5.9 from upstream 

* Wed Aug 23 2006 Maros Barabas <mbarabas@redhat.com> - 3.5.1-2
- remove .a & .la from libdir

* Mon Jul 17 2006 Jason Vas Dias <jvdias@redhat.com> - 3.5.1-1.fc6
- Upgrade to 3.5.1

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 3.4.7-2.FC6.1
- rebuild

* Mon Jun 12 2006 Jason Vas Dias <jvdias@redhat.com> - 3.4.7-2
- Add BuildRequires for broken Brew

* Wed May 31 2006 Jason Vas Dias <jvdias@redhat.com> - 3.4.7-1
- Upgrade to upstream version 3.4.7

* Fri Apr 28 2006 Jason Vas Dias <jvdias@redhat.com> - 3.4.6-1
- Upgrade to upstream version 3.4.6

* Fri Apr 21 2006 Jason Vas Dias <jvdias@redhat.com> - 3.4.4-1
- Upgrade to upstream version 3.4.4

* Thu Mar 16 2006 Jason Vas Dias <jvdias@redhat.com> - 3.4.3-1
- Upgrade to upstream version 3.4.3

* Fri Mar 10 2006 Bill Nottingham <notting@redhat.com> - 3.4.2-5
- rebuild for ppc TLS issue (#184446)

* Thu Feb 16 2006 Jason Vas Dias<jvdias@redhat.com> - 3.4.2-4
- Apply upstream fix for bug 181694.

* Wed Feb 15 2006 Jason Vas Dias<jvdias@redhat.com> - 3.4.2-2
- fix bug 181694: segfault on redirection to non-existent location

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 3.4.2-1.1
- bump again for double-long bug on ppc(64)

* Wed Feb 08 2006 Jason Vas Dias<jvdias@redhat.com> - 3.4.2-1
- Upgrade to upstream version 3.4.2, that fixes 3.4.1's coredump

* Tue Feb 07 2006 Jason Vas Dias<jvdias@redhat.com> - 3.4.1-1
- Upgrade to upstream version 3.4.1
- fix core dump

* Fri Jan 13 2006 Jason Vas Dias<jvdias@redhat.com> - 3.4.0-1
- Upgrade to upstream version 3.4.0

* Wed Dec 21 2005 Jason Vas Dias<jvdias@redhat.com> - 3.3.5-4
- fix bug 176315: openssl libraries not being picked up - gnutls was instead
- improvements to bug 172376 fix

* Tue Dec 20 2005 Jason Vas Dias<jvdias@redhat.com> - 3.3.5-2
- fix bug 176175: perl-String-CRC32 now in separate RPM 

* Thu Dec 15 2005 Jason Vas Dias<jvdias@redhat.com> - 3.3.5-1
- Upgrade to version 3.3.5
- fix bug bz172376 : host lookups should use any address found after timeout 

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Fri Nov 11 2005 Jason Vas Dias <jvdias@redhat.com> - 3.3.3-1
- Upgrade to upstream 3.3.3 release, fixing bug 171884 .

* Tue Oct 18 2005 Jason Vas Dias <jvdias@redhat.com> - 3.3.2-1
- *** PLEASE COULD ANYONE MODIFYING lftp TEST IT BEFORE SUBMITTING! ***
  (and preferably contact the lftp package maintainer (me) first - thank you!)
  bug 171096 : 'mget files in lftp causes abort' (core dump actually)
  resulted from not doing so .
  See http://lftp.yar.ru :
	Recent events:2005-10-17: 
	lftp-3.3.2 released. Fixed a coredump caused by double-free.

* Sat Oct 15 2005 Florian La Roche <laroche@redhat.com> - 3.3.1-1
- 3.3.1

* Wed Aug 24 2005 Jason Vas Dias <jvdias@redhat.com> - 3.3.0-1
- Upgrade to upstream version 3.3.0

* Mon Aug  8 2005 Tomas Mraz <tmraz@redhat.com> - 3.2.1-2
- rebuild with new gnutls

* Thu Jun 30 2005 Warren Togami <wtogami@redhat.com> 3.2.1-1
- 3.2.1

* Mon Apr 25 2005 Jason Vas Dias <jvdias@redhat.com> 3.1.3-1
- Upgrade to upstream version 3.1.3

* Tue Mar  8 2005 Jason Vas Dias <jvdias@redhat.com> 3.1.0-1
- Upgrade to upstream verson 3.1.0; remove patch for broken libtool

* Tue Mar  8 2005 Joe Orton <jorton@redhat.com> 3.0.13-2
- rebuild

* Fri Jan 21 2005 Jason Vas Dias <jvdias@redhat.com> 3.0.13-1
- Upgrade to upstream version 3.0.13 .

* Wed Jan 12 2005 Tim Waugh <twaugh@redhat.com> 3.0.6-4
- Rebuilt for new readline.

* Mon Oct 18 2004 Jason Vas Dias <jvdias@redhat.com> 3.0.6-3
- rebuilding for current FC3 glibc fixes bug 136109
 
* Mon Aug 16 2004 Nalin Dahyabhai <nalin@redhat.com> 3.0.6-2
- rebuild

* Tue Jun 15 2004 Nalin Dahyabhai <nalin@redhat.com> 3.0.6-1
- update to 3.0.6

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Mar 12 2004 Nalin Dahyabhai <nalin@redhat.com> 2.6.12-1
- update to 2.6.12

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Dec 16 2003 Nalin Dahyabhai <nalin@redhat.com> 2.6.10-3
- add patch to avoid DoS when connecting to HTTP servers (or "HTTP" "servers")
  which don't provide status headers, or provide empty lines instead of status
  headers

* Fri Dec 12 2003 Nalin Dahyabhai <nalin@redhat.com> 2.6.10-2
- rebuild

* Fri Dec 12 2003 Nalin Dahyabhai <nalin@redhat.com> 2.6.10-1
- update to 2.6.10, which folds in the previous patches
- configure with --with-debug so that we get useful debug info

* Tue Dec  9 2003 Nalin Dahyabhai <nalin@redhat.com> 2.6.9-1
- include patch based on patch from Ulf Härnhammar to fix unsafe use of
  sscanf when reading http directory listings (CAN-2003-0963)
- include patch based on patch from Ulf Härnhammar to fix compile warnings
  modified based on input from Solar Designer

* Mon Dec  8 2003 Nalin Dahyabhai <nalin@redhat.com>
- update to 2.6.9

* Wed Aug  6 2003 Elliot Lee <sopwith@redhat.com>
- Fix libtool

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Tue Jan  7 2003 Nalin Dahyabhai <nalin@redhat.com> 2.6.3-2
- rebuild

* Thu Dec 12 2002 Nalin Dahyabhai <nalin@redhat.com>
- use openssl's pkg-config data, if available

* Thu Nov 14 2002 Nalin Dahyabhai <nalin@redhat.com> 2.6.3-1
- update to 2.6.3

* Tue Nov 12 2002 Tim Powers <timp@redhat.com> 2.6.2-2
- remove files we aren't including from the $$RPM_BUILD_ROOT

* Fri Oct  4 2002 Nalin Dahyabhai <nalin@redhat.com> 2.6.2-1
- build with the system's libtool

* Thu Sep 26 2002 Nalin Dahyabhai <nalin@redhat.com>
- update to 2.6.2

* Sat Aug 10 2002 Elliot Lee <sopwith@redhat.com>
- rebuilt with gcc-3.2 (we hope)

* Tue Jul 23 2002 Tim Powers <timp@redhat.com> 2.5.2-4
- build using gcc-3.2-0.1

* Fri Jun 21 2002 Tim Powers <timp@redhat.com> 2.5.2-3
- automated rebuild

* Sun May 26 2002 Tim Powers <timp@redhat.com> 2.5.2-2
- automated rebuild

* Fri May 17 2002 Nalin Dahyabhai <nalin@redhat.com> 2.5.2-1
- update to 2.5.2

* Fri Feb 22 2002 Nalin Dahyabhai <nalin@redhat.com> 2.4.9-1
- update to 2.4.9

* Wed Jan 23 2002 Nalin Dahyabhai <nalin@redhat.com> 2.4.8-1
- update to 2.4.8

* Wed Jan 09 2002 Tim Powers <timp@redhat.com> 2.4.0-3
- automated rebuild

* Thu Aug 16 2001 Nalin Dahyabhai <nalin@redhat.com> 2.4.0-2
- remove the .la files from the final package -- these aren't libraries
  people link with anyway

* Mon Aug  6 2001 Nalin Dahyabhai <nalin@redhat.com> 2.4.0-1
- update to 2.4.0 (fixes some memory leaks and globbing cases)

* Thu Jul  5 2001 Nalin Dahyabhai <nalin@redhat.com>
- langify

* Fri Jun 29 2001 Nalin Dahyabhai <nalin@redhat.com>
- explicitly list the modules which are built when the package compiles, so
  that module build failures (for whatever reason) get caught

* Mon Jun 25 2001 Nalin Dahyabhai <nalin@redhat.com>
- merge in changes from ja .spec file

* Wed May 30 2001 Nalin Dahyabhai <nalin@redhat.com>
- update to 2.3.11

* Fri Apr 27 2001 Nalin Dahyabhai <nalin@redhat.com>
- update to 2.3.9

* Fri Mar  2 2001 Tim Powers <timp@redhat.com>
- rebuilt against openssl-0.9.6-1

* Fri Jan 19 2001 Nalin Dahyabhai <nalin@redhat.com>
- update to 2.3.7

* Thu Jan  4 2001 Nalin Dahyabhai <nalin@redhat.com>
- update to 2.3.6

* Fri Dec  1 2000 Nalin Dahyabhai <nalin@redhat.com>
- update to 2.3.5

* Mon Jul 24 2000 Prospector <prospector@redhat.com>
- rebuilt

* Thu Jul 13 2000 Tim Powers <timp@redhat.com>
- patched to build with gcc-2.96
- use gcc instead of c++ for CXX, otherwise you expose an ICE in gcc when
  using g++ on two files, one being a C++ source, and the other a C source.
  Using gcc does the correct thing.

* Mon Jul 10 2000 Tim Powers <timp@redhat.com>
- rebuilt

* Thu Jun 8 2000 Tim Powers <timp@redhat.com>
- fix man page location
- use %%makeinstall
- use predefined macros wherever possible

* Mon May 15 2000 Tim Powers <timp@redhat.com>
- updated to 2.2.2
- added locales tofiles list
- built for 7.0

* Thu Jan 27 2000 Tim Powers <timp@redhat.com>
- fixed package description etc.

* Fri Jan 21 2000 Tim Powers <timp@redhat.com>
- ughh. didn't include /usr/lib/lftp in files list, fixed

* Thu Jan 13 2000 Tim Powers <timp@redhat.com>
- initial build for Powertools
