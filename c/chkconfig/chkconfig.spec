Summary: A system tool for maintaining the /etc/rc*.d hierarchy
Name: chkconfig
Version: 1.3.49.5
Release: 1%{?dist}
License: GPLv2
Group: System Environment/Base
Source: http://fedorahosted.org/releases/c/h/chkconfig/%{name}-%{version}.tar.bz2
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: newt-devel gettext popt-devel libselinux-devel
Conflicts: initscripts <= 5.30-1

%description
Chkconfig is a basic system utility.  It updates and queries runlevel
information for system services.  Chkconfig manipulates the numerous
symbolic links in /etc/rc.d, to relieve system administrators of some 
of the drudgery of manually editing the symbolic links.

%package -n ntsysv
Summary: A tool to set the stop/start of system services in a runlevel
Group: System Environment/Base
Requires: chkconfig = %{version}-%{release}

%description -n ntsysv
Ntsysv provides a simple interface for setting which system services
are started or stopped in various runlevels (instead of directly
manipulating the numerous symbolic links in /etc/rc.d). Unless you
specify a runlevel or runlevels on the command line (see the man
page), ntsysv configures the current runlevel (5 if you're using X).

%prep
%setup -q

%build

make RPM_OPT_FLAGS="$RPM_OPT_FLAGS" %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT MANDIR=%{_mandir} SBINDIR=%{_sbindir} install

mkdir -p $RPM_BUILD_ROOT/etc/rc.d/init.d
ln -s rc.d/init.d $RPM_BUILD_ROOT/etc/init.d
for n in 0 1 2 3 4 5 6; do
    mkdir -p $RPM_BUILD_ROOT/etc/rc.d/rc${n}.d
    ln -s rc.d/rc${n}.d $RPM_BUILD_ROOT/etc/rc${n}.d
done
mkdir -p $RPM_BUILD_ROOT/etc/chkconfig.d

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}.lang
%defattr(-,root,root)
%doc COPYING
%dir /etc/alternatives
/sbin/chkconfig
%{_sbindir}/update-alternatives
%{_sbindir}/alternatives
/etc/chkconfig.d
/etc/init.d
/etc/rc.d/init.d
/etc/rc[0-6].d
/etc/rc.d/rc[0-6].d
%dir /var/lib/alternatives
%{_mandir}/*/chkconfig*
%{_mandir}/*/update-alternatives*
%{_mandir}/*/alternatives*

%files -n ntsysv
%defattr(-,root,root)
%{_sbindir}/ntsysv
%{_mandir}/*/ntsysv.8*

%changelog
* Thu Jan 07 2016 Lukáš Nykrýn <lnykryn@redhat.com> - 1.3.49.5-1
- leveldb: suppress error messages when selinux is turned off

* Fri Dec 11 2015 Lukáš Nykrýn <lnykryn@redhat.com> - 1.3.49.4-1
- chkconfig: don't create symlinks if they already exist
- chkconfig: resetpriorities should work on all runlevels
- leveldb: fix segfault when selinux policy is not present
- alternatives: always recreate symlinks when the alternative is updated

* Tue Feb 17 2015 Lukáš Nykrýn <lnykryn@redhat.com> - 1.3.49.3-5
- relabel xinetd.d files after change

* Mon Jan 12 2015 Lukáš Nykrýn <lnykryn@redhat.com> - 1.3.49.3-4
- fix permission issues with xinetd services

* Thu Sep 12 2013 Lukas Nykryn <lnykryn@redhat.com> - 1.3.49.3-3
- check readServices return value (#905555)

* Wed Feb  1 2012 Bill Nottingham <notting@redhat.com> 1.3.49.3-2
- fix another regression, this one in 'install_initd' (#696305)

* Tue Jan 17 2012 Bill Nottingham <notting@redhat.com> 1.3.49.2-1
- backport fix for regression introduced in last set of fixes (#782152)
 
* Wed Jan  4 2012 Bill Nottingham <notting@redhat.com> 1.3.49.1-1
- backport LSB fixes from head
- fixes: #693202/#771455, #649227/#771452, #750446/#771454, #701573/#771741, #696305 (<jbastian@redhat.com>)

* Tue Nov  9 2010 Bill Nottingham <notting@redhat.com> 1.3.49-1
- fix abort on free of uninitialized data. (#649227)

* Wed Oct 27 2010 Bill Nottingham <notting@redhat.com> 1.3.48-1
- fix install_initd invocation for services that require $local_fs (#632294)

* Tue Aug 10 2010 Bill Nottingham <notting@redhat.com> 1.3.47-1
- Fix regression introduced in 1.3.45 (#622799)

* Wed May 05 2010 Bill Nottingham <notting@redhat.com> 1.3.46-1
- translation updates: hu, kn, ko (#589187)

* Thu Mar 04 2010 Bill Nottingham <notting@redhat.com> 1.3.45-1
- add support for Should-Start, Should-Stop (#98470, <iarnell@gmail.com>)
- ntsysv: don't drop initscripts with '.' in the name (#556751)
- translation updates: el, id

* Tue Sep 29 2009 Bill Nottingham <notting@redhat.com> 1.3.44-1
- alternatives: update symlinks if they exist on installation (#104940)
- alternatives: clarify error messages with more context (#441443)
- alternatives: fix removal of manual links (#525021, <dtardon@redhat.com>)
- translation updates: ml, mr, pl, ta, uk

* Mon Sep 14 2009 Bill Nottingham <notting@redhat.com> 1.3.43-1
- ntsysv man page tweak (#516599)
- another minor LSB tweak (#474223)
- translation updates

* Fri Mar  6 2009 Bill Nottingham <notting@redhat.com> 1.3.42-1
- further LSB fixes (#474223)
- throw errors on various malformed init scripts (#481198)
- man page updates re: LSB (#487979)
- translation updates: mai, gu, pt_BR, ro, ca, pa, sr, fr, hu

* Tue Jan 20 2009 Bill Nottingham <notting@redhat.com> 1.3.41-1
- restore return code & error on unconfigured services (#480805)

* Fri Dec  5 2008 Bill Nottingham <notting@redhat.com> 1.3.40-1
- fix some overflows. (#176944)
- add --type parameter to specify either xinetd or sysv services.
  (#467863, <mschmidt@redhat.com>
- do a permissions check before add/remove/on/off/resetpriorities. (#450254)
- parse Short-Description correctly (#441813, <peter_e@gmx.net>)

* Thu Dec  4 2008 Bill Nottingham <notting@redhat.com> 1.3.39-1
- fail if dependencies fail on add/remove in LSB mode (#474223)

* Wed Oct 29 2008 Bill Nottingham <notting@redhat.com> 1.3.38-1
- Fix runlevel list in man page (#466739)
- translation updates

* Thu Nov  8 2007 Bill Nottingham <notting@redhat.com> 1.3.37-1
- make no options do --list (#290241, #176184)
- sr@Latn -> sr@latin

* Tue Sep 25 2007 Bill Nottingham <notting@redhat.com> 1.3.36-1
- buildreq popt-devel, link it dynamically (#279531)
- translation updates: kn, ko, mr, ro

* Fri Aug  3 2007 Bill Nottingham <notting@redhat.com> 1.3.35-1
- clarify licensing

* Mon Apr 16 2007 Bill Nottingham <notting@redhat.com> 1.3.34-1
- translation updates: as, bg, bn_IN, bs, ca, de, fr, hi, hu, id, ja,
  ka, ml, ms, nb, or, sk, sl
- add resetpriorities to the man page (#197399)
  
* Tue Feb  6 2007 Bill Nottingham <notting@redhat.com> 1.3.33-1
- various changes from review - support alternate %%{_sbindir}, fix
  summaries, add version to requires, assorted other bits

* Fri Feb  2 2007 Bill Nottingham <notting@redhat.com> 1.3.32-1
- support overriding various defaults via /etc/chkconfig.d (<johnsonm@rpath.com>)

* Thu Feb  1 2007 Bill Nottingham <notting@redhat.com> 1.3.31-1
- fix man page (#220558, <esr@thyrus.com>)
- add some more verbiage in alternatives man page (#221089)
- don't print usage message on a nonexstent service (#226804)

* Fri Dec  1 2006 Bill Nottingham <notting@redhat.com> 1.3.30.1-1
- translation updates: as, ka, lv, ml, te (#216617)

* Thu Sep  7 2006 Bill Nottingham <notting@redhat.com> 1.3.30-1
- license cleanup

* Fri Feb 24 2006 Bill Nottingham <notting@redhat.com> 1.3.29-1
- fix accidental enabling of services on --add (#182729)

* Mon Feb 13 2006 Bill Nottingham <notting@redhat.com> 1.3.27-1
- translation updates

* Thu Feb  2 2006 Bill Nottingham <notting@redhat.com> 1.3.26-1
- add support for resetting priorities without on/off status (#178864)

* Wed Nov 30 2005 Bill Nottingham <notting@redhat.com> 1.3.25-1
- return an error if changing services fails (#150235)

* Fri Nov 18 2005 Bill Nottingham <notting@redhat.com> 1.3.24-1
- when removing alternatives links, check to make sure they're
  actually links (#173685)

* Fri Nov 11 2005 Bill Nottingham <notting@redhat.com> 1.3.23-1
- fix ntsysv (#172996)

* Wed Nov  9 2005 Bill Nottingham <notting@redhat.com>
- fix doSetService call in frobOneDependencies

* Tue Nov  8 2005 Bill Nottingham <notting@redhat.com>
- for LSB scripts, use any chkconfig: priorities as a basis,
  instead of 50/50 (#172599)
- fix LSB script dependency setting when no chkconfig: line
  is present (#161870, <jean-francois.larvoire@hp.com>)
- fix LSB script dependency setting when one of Required-Stop
  or Required-Start: is missing (#168457)

* Fri Oct  7 2005 Bill Nottingham <notting@redhat.com>
- fix segfault on directories in /etc/xinetd.d (#166385)
- don't needlessly rewrite xinetd files (#81008)

* Thu May  5 2005 Bill Nottingham <notting@redhat.com> 1.3.20-1
- fix deletion of orphaned slave links (#131496, <mitr@redhat.com>)

* Fri Apr 29 2005 Bill Nottingham <notting@redhat.com> 1.3.19-1
- build with updated translations

* Thu Mar  3 2005 Bill Nottingham <notting@redhat.com> 1.3.18-1
- actually return an error code if changing a service info fails

* Tue Feb 22 2005 Bill Nottingham <notting@redhat.com> 1.3.17-1
- more chkconfig: vs. LSB fixes (#149066)

* Thu Feb 10 2005 Bill Nottingham <notting@redhat.com> 1.3.16-1
- prefer chkconfig: start/stop priorities in LSB mode unless
  Required-Start/Stop are used

* Mon Feb  7 2005 Bill Nottingham <notting@redhat.com> 1.3.15-1
- print usage when various invalid args are passed (#147393)

* Wed Feb  2 2005 Bill Nottingham <notting@redhat.com> 1.3.14-1
- resize reasonably with larger screens (#74156)
- don't error out completely on bad symlink (#74324)
- use ngettext (#106176)
- error out on invalid start/stop values (#109858)
- some man page updates
- fix return code of chkconfig for xinetd services (#63123)
- sort chkconfig --list display (#61576, <shishz@alum.rpi.edu>)

* Tue Jan 11 2005 Bill Nottingham <notting@redhat.com> 1.3.13-1
- fix LSB comment parsing some more (#144739)

* Thu Oct 28 2004 Bill Nottingham <notting@redhat.com> 1.3.11.2-1
- fix manpage reference (#137492)

* Fri Oct  1 2004 Bill Nottingham <notting@redhat.com> 1.3.11.1-1
- rebuild with updated translations

* Fri Jun  4 2004 Bill Nottingham <notting@redhat.com> 1.3.11-1
- fix LSB comment parsing (#85678)

* Wed May 29 2004 Bill Nottingham <notting@redhat.com> 1.3.10-1
- mark alternatives help output for translation (#110526)

* Wed Oct 22 2003 Bill Nottingham <notting@redhat.com> 1.3.9-1
- update translations

* Mon Jul 28 2003 Bill Nottingham <notting@redhat.com> 1.3.8-4
- rebuild

* Tue May 13 2003 Dan Walsh <dwalsh@redhat.com> 1.3.8-3
- Update for RHEL

* Thu May 8 2003 Dan Walsh <dwalsh@redhat.com> 1.3.8-2
- Fix readXinetdServiceInfo to return error on not regular files
- Fix chkconfig to not write messages if readXinetdServiceInfo gets an error

* Fri Jan 31 2003 Bill Nottingham <notting@redhat.com> 1.3.8-1
- fix some wording in alternatives (#76213)
- actually mark alternatives for translation

* Thu Dec 12 2002 Elliot Lee <sopwith@redhat.com> 1.3.7-1
- Link to libpopt in a multilib-safe fashion.

* Thu Aug 29 2002 Trond Eivind Glomsrød <teg@redhat.com> 1.3.6-3
- bump

* Thu Aug 15 2002 Bill Nottingham <notting@redhat.com> 1.3.6-2
- rebuild against new newt

* Mon Aug 12 2002 Bill Nottingham <notting@redhat.com> 1.3.6-1
- make on and off handle runlevel 2 too (#70766)

* Mon Apr 15 2002 Trond Eivind Glomsrød <teg@redhat.com> 1.3.5-3
- Update translations

* Mon Apr 15 2002 Trond Eivind Glomsrød <teg@redhat.com> 1.3.5-2
- Update translations

* Sun Apr  7 2002 Jeremy Katz <katzj@redhat.com> 1.3.5-1
- alternatives: handle default with --config properly (#62009)

* Thu Mar 14 2002 Bill Nottingham <notting@redhat.com> 1.3.4-1
- don't apply the dependency logic to things that already have
  start/stop priorities
- fix silly display bug in --config

* Tue Mar 12 2002 Bill Nottingham <notting@redhat.com> 1.3.2-1
- chkconfig: LSB support

* Fri Mar  8 2002 Bill Nottingham <notting@redhat.com>
- alternatives: handle initscripts too; --initscript command-line option
- chkconfig/ntsysv (and serviceconf, indirectly): services with
   *no* links in /etc/rc*.d are no longer displayed with --list, or
   available for configuration except via chkconfig command-line options
- alternatives: fix trying to enable disable a null service

* Tue Mar  5 2002 Bill Nottingham <notting@redhat.com>
- alternatives: handle things with different numbers of slave links

* Mon Mar  4 2002 Bill Nottingham <notting@redhat.com>
- minor alternatives tweaks: don't install the same thing multiple times

* Wed Jan 30 2002 Bill Nottingham <notting@redhat.com>
- actually, put the alternatives stuff back in /usr/sbin
- ship /etc/alternatives dir
- random alternatives fixes

* Sun Jan 27 2002 Erik Troan <ewt@redhat.com>
- reimplemented update-alternatives as just alternatives

* Thu Jan 25 2002 Bill Nottingham <notting@redhat.com>
- add in update-alternatives stuff (perl ATM)

* Mon Aug 27 2001 Trond Eivind Glomsrød <teg@redhat.com>
- Update translations

* Tue Jun 12 2001 Bill Nottingham <notting@redhat.com>
- don't segfault on files that are exactly the length of a page size
  (#44199, <kmori@redhat.com>)

* Sun Mar  4 2001 Bill Nottingham <notting@redhat.com>
- don't show xinetd services in ntsysv if xinetd doesn't appear to be
  installed (#30565)

* Wed Feb 14 2001 Preston Brown <pbrown@redhat.com>
- final translation update.

* Tue Feb 13 2001 Preston Brown <pbrown@redhat.com>
- warn in ntsysv if not running as root.

* Fri Feb  2 2001 Preston Brown <pbrown@redhat.com>
- use lang finder script

* Fri Feb  2 2001 Bill Nottingham <notting@redhat.com>
- finally fix the bug Nalin keeps complaining about :)

* Wed Jan 24 2001 Preston Brown <pbrown@redhat.com>
- final i18n update before Beta.

* Wed Oct 18 2000 Bill Nottingham <notting@redhat.com>
- ignore .rpmnew files (#18915)
- fix typo in error message (#17575)

* Wed Aug 30 2000 Nalin Dahyabhai <nalin@redhat.com>
- make xinetd config files mode 0644, not 644

* Thu Aug 24 2000 Erik Troan <ewt@redhat.com>
- updated it and es translations

* Sun Aug 20 2000 Bill Nottingham <notting@redhat.com>
- get man pages in proper packages

* Sun Aug 20 2000 Matt Wilson <msw@redhat.com>
- new translations

* Tue Aug 16 2000 Nalin Dahyabhai <nalin@redhat.com>
- don't worry about extra whitespace on chkconfig: lines (#16150)

* Wed Aug 10 2000 Trond Eivind Glomsrød <teg@redhat.com>
- i18n merge

* Wed Jul 26 2000 Matt Wilson <msw@redhat.com>
- new translations for de fr it es

* Tue Jul 25 2000 Bill Nottingham <notting@redhat.com>
- change prereqs

* Sun Jul 23 2000 Bill Nottingham <notting@redhat.com>
- fix ntsysv's handling of xinetd/init files with the same name

* Fri Jul 21 2000 Bill Nottingham <notting@redhat.com>
- fix segv when reading malformed files

* Wed Jul 19 2000 Bill Nottingham <notting@redhat.com>
- put links, rc[0-6].d dirs back, those are necessary

* Tue Jul 18 2000 Bill Nottingham <notting@redhat.com>
- add quick hack support for reading descriptions from xinetd files

* Mon Jul 17 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- don't own the /etc/rc[0-6].d symlinks; they're owned by initscripts

* Sat Jul 15 2000 Matt Wilson <msw@redhat.com>
- move back to old file layout

* Thu Jul 13 2000 Preston Brown <pbrown@redhat.com>
- bump copyright date

* Tue Jul 11 2000 Bill Nottingham <notting@redhat.com>
- no %%pre today. Maybe tomorrow.

* Thu Jul  6 2000 Bill Nottingham <notting@redhat.com>
- put initscripts %%pre here too

* Mon Jul  3 2000 Bill Nottingham <notting@redhat.com>
- oops, if we don't prereq initscripts, we *need* to own /etc/rc[0-6].d

* Sun Jul  2 2000 Bill Nottingham <notting@redhat.com>
- add xinetd support

* Tue Jun 27 2000 Matt Wilson <msw@redhat.com>
- changed Prereq: initscripts >= 5.18 to Conflicts: initscripts < 5.18
- fixed sumary and description where a global string replace nuked them

* Mon Jun 26 2000 Matt Wilson <msw@redhat.com>
- what Bill said, but actually build this version

* Thu Jun 15 2000 Bill Nottingham <notting@redhat.com>
- don't own /etc/rc.*

* Fri Feb 11 2000 Bill Nottingham <notting@redhat.com>
- typo in man page

* Wed Feb 02 2000 Cristian Gafton <gafton@redhat.com>
- fix description

* Wed Jan 12 2000 Bill Nottingham <notting@redhat.com>
- link chkconfig statically against popt

* Mon Oct 18 1999 Bill Nottingham <notting@redhat.com>
- fix querying alternate levels

* Mon Aug 23 1999 Jeff Johnson <jbj@redhat.com>
- don't use strchr to skip unwanted files, look at extension instead (#4166).

* Thu Aug  5 1999 Bill Nottingham <notting@redhat.com>
- fix --help, --verson

* Mon Aug  2 1999 Matt Wilson <msw@redhat.com>
- rebuilt ntsysv against newt 0.50

* Mon Aug  2 1999 Jeff Johnson <jbj@redhat.com>
- fix i18n problem in usage message (#4233).
- add --help and --version.

* Mon Apr 19 1999 Cristian Gafton <gafton@redhat.com>
- release for Red Hat 6.0

* Thu Apr  8 1999 Matt Wilson <msw@redhat.com>
- added support for a "hide: true" tag in initscripts that will make
  services not appear in ntsysv when run with the "--hide" flag

* Thu Apr  1 1999 Matt Wilson <msw@redhat.com>
- added --hide flag for ntsysv that allows you to hide a service from the
  user.

* Mon Mar 22 1999 Bill Nottingham <notting@redhat.com>
- fix glob, once and for all. Really. We mean it.

* Thu Mar 18 1999 Bill Nottingham <notting@redhat.com>
- revert fix for services@levels, it's broken
- change default to only edit the current runlevel

* Mon Mar 15 1999 Bill Nottingham <notting@redhat.com>
- don't remove scripts that don't support chkconfig

* Tue Mar 09 1999 Erik Troan <ewt@redhat.com>
- made glob a bit more specific so xinetd and inetd don't cause improper matches

* Thu Feb 18 1999 Matt Wilson <msw@redhat.com>
- removed debugging output when starting ntsysv

* Thu Feb 18 1999 Preston Brown <pbrown@redhat.com>
- fixed globbing error
- fixed ntsysv running services not at their specified levels.

* Tue Feb 16 1999 Matt Wilson <msw@redhat.com>
- print the value of errno on glob failures.

* Sun Jan 10 1999 Matt Wilson <msw@redhat.com>
- rebuilt for newt 0.40 (ntsysv)

* Tue Dec 15 1998 Jeff Johnson <jbj@redhat.com>
- add ru.po.

* Thu Oct 22 1998 Bill Nottingham <notting@redhat.com>
- build for Raw Hide (slang-1.2.2)

* Wed Oct 14 1998 Cristian Gafton <gafton@redhat.com>
- translation updates

* Thu Oct 08 1998 Cristian Gafton <gafton@redhat.com>
- updated czech translation (and use cs instead of cz)

* Tue Sep 22 1998 Arnaldo Carvalho de Melo <acme@conectiva.com.br>
- added pt_BR translations
- added more translatable strings
- support for i18n init.d scripts description

* Sun Aug 02 1998 Erik Troan <ewt@redhat.com>
- built against newt 0.30
- split ntsysv into a separate package

* Thu May 07 1998 Erik Troan <ewt@redhat.com>
- added numerous translations

* Mon Mar 23 1998 Erik Troan <ewt@redhat.com>
- added i18n support

* Sun Mar 22 1998 Erik Troan <ewt@redhat.com>
- added --back