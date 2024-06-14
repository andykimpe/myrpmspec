
%global pkgname   dirsrv
# for a pre-release, define the prerel field e.g. .a1 .rc2 - comment out for official release
# also remove the space between % and global - this space is needed because
# fedpkg verrel stupidly ignores comment lines
# % global prerel .a1
# also need the relprefix field for a pre-release e.g. .0 - also comment out for official release
# % global relprefix 0.

%global use_openldap 1
%global use_db4 1
# If perl-Socket-2.000 or newer is available, set 0 to use_Socket6.
%global use_Socket6 1

# if system doesn't support tmpfiles.d, comment this out
#%{!?with_tmpfiles_d: %global with_tmpfiles_d %{_sysconfdir}/tmpfiles.d}

# systemd support
%global groupname %{pkgname}.target

Summary:          389 Directory Server (base)
Name:             389-ds-base
Version:          1.2.11.32
Release:          %{?relprefix}1%{?prerel}%{?dist}
License:          GPLv2 with exceptions
URL:              http://port389.org/
Group:            System Environment/Daemons
BuildRoot:        %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires:         %{name}-libs = %{version}-%{release}
Provides:         ldif2ldbm 

BuildRequires:    nspr-devel
BuildRequires:    nss-devel
BuildRequires:    svrcore-devel
%if %{use_openldap}
BuildRequires:    openldap-devel
%else
BuildRequires:    mozldap-devel
%endif
%if %{use_db4}
BuildRequires:    db4-devel
%else
BuildRequires:    libdb-devel
%endif
BuildRequires:    cyrus-sasl-devel
BuildRequires:    icu
BuildRequires:    libicu-devel
BuildRequires:    pcre-devel
BuildRequires:    gcc-c++
# The following are needed to build the snmp ldap-agent
BuildRequires:    net-snmp-devel
%ifnarch sparc sparc64 ppc ppc64 s390 s390x
BuildRequires:    lm_sensors-devel
%endif
BuildRequires:    bzip2-devel
BuildRequires:    zlib-devel
BuildRequires:    openssl-devel
BuildRequires:    tcp_wrappers
# the following is for the pam passthru auth plug-in
BuildRequires:    pam-devel

# this is needed for using semanage from our setup scripts
Requires:         policycoreutils-python

# the following are needed for some of our scripts
%if %{use_openldap}
Requires:         openldap-clients
%else
Requires:         mozldap-tools
%endif
# use_openldap assumes perl-Mozilla-LDAP is built with openldap support
Requires:         perl-Mozilla-LDAP

# this is needed to setup SSL if you are not using the
# administration server package
Requires:         nss-tools

# these are not found by the auto-dependency method
# they are required to support the mandatory LDAP SASL mechs
Requires:         cyrus-sasl-gssapi
Requires:         cyrus-sasl-md5

# this is needed for verify-db.pl
%if %{use_db4}
Requires:         db4-utils
%else
Requires:         libdb-utils
%endif

# for setup-ds.pl to support ipv6 
%if %{use_Socket6}
Requires:         perl-Socket6
%else
Requires:         perl-Socket
%endif
Requires:         perl-NetAddr-IP

# This picks up libperl.so as a Requires, so we add this versioned one
Requires:         perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

# for the init script
Requires(post): /sbin/chkconfig
Requires(preun): /sbin/chkconfig
Requires(preun): /sbin/service

Source0:          https://fedorapeople.org/groups/389ds/binaries/%{name}-%{version}%{?prerel}.tar.bz2
# 389-ds-git.sh should be used to generate the source tarball from git
Source1:          https://github.com/andykimpe/myrpmspec/raw/el6/389-ds-base/%{name}-git.sh
Source2:          https://github.com/andykimpe/myrpmspec/raw/el6/389-ds-base/%{name}-devel.README

%description
389 Directory Server is an LDAPv3 compliant server.  The base package includes
the LDAP server and command line utilities for server administration.

%package          libs
Summary:          Core libraries for 389 Directory Server
Group:            System Environment/Daemons
BuildRequires:    nspr-devel
BuildRequires:    nss-devel
BuildRequires:    svrcore-devel
%if %{use_openldap}
BuildRequires:    openldap-devel
%else
BuildRequires:    mozldap-devel
%endif
%if %{use_db4}
BuildRequires:    db4-devel
%else
BuildRequires:    libdb-devel
%endif
BuildRequires:    cyrus-sasl-devel
BuildRequires:    libicu-devel
BuildRequires:    pcre-devel

%description      libs
Core libraries for the 389 Directory Server base package.  These libraries
are used by the main package and the -devel package.  This allows the -devel
package to be installed with just the -libs package and without the main package.

%package          devel
Summary:          Development libraries for 389 Directory Server
Group:            Development/Libraries
Requires:         %{name}-libs = %{version}-%{release}
Requires:         pkgconfig
Requires:         nspr-devel
Requires:         nss-devel
Requires:         svrcore-devel
%if %{use_openldap}
Requires:         openldap-devel
%else
Requires:         mozldap-devel
%endif

%description      devel
Development Libraries and headers for the 389 Directory Server base package.

%prep
%setup -q -n %{name}-%{version}%{?prerel}
cp %{SOURCE2} README.devel

%build
%if %{use_openldap}
OPENLDAP_FLAG="--with-openldap"
%endif
%{?with_tmpfiles_d: TMPFILES_FLAG="--with-tmpfiles-d=%{with_tmpfiles_d}"}
%configure --enable-autobind --with-selinux $OPENLDAP_FLAG $TMPFILES_FLAG

# Generate symbolic info for debuggers
export XCFLAGS=$RPM_OPT_FLAGS

%ifarch x86_64 ppc64 ia64 s390x sparc64
export USE_64=1
%endif

make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT 

make DESTDIR="$RPM_BUILD_ROOT" install

mkdir -p $RPM_BUILD_ROOT/var/log/%{pkgname}
mkdir -p $RPM_BUILD_ROOT/var/lib/%{pkgname}
mkdir -p $RPM_BUILD_ROOT/var/lock/%{pkgname}

#remove libtool and static libs
rm -f $RPM_BUILD_ROOT%{_libdir}/%{pkgname}/*.a
rm -f $RPM_BUILD_ROOT%{_libdir}/%{pkgname}/*.la
rm -f $RPM_BUILD_ROOT%{_libdir}/%{pkgname}/plugins/*.a
rm -f $RPM_BUILD_ROOT%{_libdir}/%{pkgname}/plugins/*.la

# make sure perl scripts have a proper shebang 
sed -i -e 's|#{{PERL-EXEC}}|#!/usr/bin/perl|' $RPM_BUILD_ROOT%{_datadir}/%{pkgname}/script-templates/template-*.pl

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add %{pkgname}
/sbin/ldconfig
/sbin/chkconfig --add %{pkgname}-snmp
# restart the snmp subagent if needed
/sbin/service %{pkgname}-snmp condrestart > /dev/null 2>&1
instbase="%{_sysconfdir}/%{pkgname}"
# echo posttrans - upgrading - looking for instances in $instbase
# find all instances
instances="" # instances that require a restart after upgrade
ninst=0 # number of instances found in total
for dir in $instbase/slapd-* ; do
# echo dir = $dir
    if [ ! -d "$dir" ] ; then continue ; fi
    case "$dir" in *.removed) continue ;; esac
    basename=`basename $dir`
    inst=`echo $basename | sed -e 's/slapd-//g'`
#   echo found instance $inst - getting status
    if /sbin/service %{pkgname} status $inst >/dev/null 2>&1 ; then
#      echo instance $inst is running
       instances="$instances $inst"
    else
#      echo instance $inst is not running
       :
    fi
    ninst=`expr $ninst + 1`
done
if [ $ninst -eq 0 ] ; then
    exit 0 # have no instances to upgrade - just skip the rest
fi
# shutdown all instances
# echo shutting down all instances . . .
/sbin/service %{pkgname} stop > /dev/null 2>&1
# do the upgrade
# echo upgrading instances . . .
%{_sbindir}/setup-ds.pl -l /dev/null -u -s General.UpdateMode=offline > /dev/null 2>&1
# restart instances that require it
for inst in $instances ; do
#   echo restarting instance $inst
    /sbin/service %{pkgname} start $inst >/dev/null 2>&1
done
exit 0

%preun
if [ $1 = 0 ]; then # Final removal
        /sbin/service %{pkgname} stop >/dev/null 2>&1 || :
        /sbin/chkconfig --del %{pkgname}
        /sbin/service %{pkgname}-snmp stop >/dev/null 2>&1 || :
        /sbin/chkconfig --del %{pkgname}-snmp
fi

%postun
/sbin/ldconfig
if [ $1 = 0 ]; then # Final removal
    rm -rf /var/run/%{pkgname}
fi

%files
%defattr(-,root,root,-)
%doc LICENSE EXCEPTION LICENSE.GPLv2
%dir %{_sysconfdir}/%{pkgname}
%dir %{_sysconfdir}/%{pkgname}/schema
%config(noreplace)%{_sysconfdir}/%{pkgname}/schema/*.ldif
%dir %{_sysconfdir}/%{pkgname}/config
%config(noreplace)%{_sysconfdir}/%{pkgname}/config/slapd-collations.conf
%config(noreplace)%{_sysconfdir}/%{pkgname}/config/certmap.conf
%config(noreplace)%{_sysconfdir}/%{pkgname}/config/ldap-agent.conf
%config(noreplace)%{_sysconfdir}/%{pkgname}/config/template-initconfig
%config(noreplace)%{_sysconfdir}/sysconfig/%{pkgname}
%{_datadir}/%{pkgname}
%{_sysconfdir}/rc.d/init.d/%{pkgname}
%{_sysconfdir}/rc.d/init.d/%{pkgname}-snmp
%{_bindir}/*
%{_sbindir}/*
%{_libdir}/%{pkgname}/libns-dshttpd.so*
%{_libdir}/%{pkgname}/perl
%dir %{_libdir}/%{pkgname}/plugins
%{_libdir}/%{pkgname}/plugins/*.so
%dir %{_localstatedir}/lib/%{pkgname}
%dir %{_localstatedir}/log/%{pkgname}
%ghost %dir %{_localstatedir}/lock/%{pkgname}
%{_mandir}/man1/*
%{_mandir}/man8/*

%files devel
%defattr(-,root,root,-)
%doc LICENSE EXCEPTION LICENSE.GPLv2 README.devel
%{_includedir}/%{pkgname}
%{_libdir}/%{pkgname}/libslapd.so
%{_libdir}/pkgconfig/*

%files libs
%defattr(-,root,root,-)
%doc LICENSE EXCEPTION LICENSE.GPLv2 README.devel
%dir %{_libdir}/%{pkgname}
%{_libdir}/%{pkgname}/libslapd.so.*

%changelog
* Thu Sep  4 2014 Noriko Hosoi <nhosoi@redhat.com> - 1.2.11.32-1
- bump version to 1.2.11.32
- Ticket 47875 - dirsrv not running with old openldap
- Ticket 47457 - default nsslapd-sasl-max-buffer-size should be 2MB

* Tue Sep  2 2014 Noriko Hosoi <nhosoi@redhat.com> - 1.2.11.31-1
- bump version to 1.2.11.31
- Bug 1129660  - Adding users to user group throws Internal server error.
- Ticket 47875 - dirsrv not running with old openldap
- Ticket 47446 - logconv.pl memory continually grows
- Ticket 443   - Deleting attribute present in nsslapd-allowed-to-delete-attrs returns Operations error
- Ticket 415   - winsync doesn't sync DN valued attributes if DS DN value doesn't exist
- Ticket 47874 - Performance degradation with scope ONE after some load
- Ticket 47872 - Filter AND with only one clause should be optimized

* Thu Aug  7 2014 Noriko Hosoi <nhosoi@redhat.com> - 1.2.11.30-1
- bump version to 1.2.11.30
- Resolves: #1123477
            Ticket 47869 - unauthenticated information disclosure (Bug 1123477)
- Ticket 616   - High contention on computed attribute lock
- Ticket 47862 - repl-monitor fails to convert "*" to default values
- Ticket 47824 - paged results control is not working in some cases when we have a subsuffix.
- Ticket 47862 - Repl-monitor.pl ignores the provided connection parameters
- Ticket 346   - Fixing memory leaks
- Ticket 443   - Deleting attribute present in nsslapd-allowed-to-delete-attrs returns Operations error
- Ticket 47863 - New defects found in 389-ds-base-1.2.11
- Ticket 47861 - Certain schema files are not replaced during upgrade
- Ticket 47858 - Internal searches using OP_FLAG_REVERSE_CANDIDATE_ORDER can crash the server
- Ticket 47692 - single valued attribute replicated ADD does not work
- Ticket 47781 - Server deadlock if online import started while  server is under load
- Ticket 47821 - deref plugin cannot handle complex acis
- Ticket 47831 - server restart wipes out index config if there is a default index
- Ticket 47820 - 1.2.11 branch: coverity errors
- Ticket 47817 - The error result text message should be obtained just prior to sending result
- Ticket 47331 - Self entry access ACI not working properly
- Ticket 47426 - Coverity issue with last commit(move compute_idletimeout out of handle_pr_read_ready)
- Ticket 47426 - move compute_idletimeout out of handle_pr_read_ready
- Ticket 47809 - find a way to remove replication plugin errors messages "changelog iteration code returned a dummy entry with csn %s, skipping ..."
- Ticket 47813 - remove "goto bail" from previous commit
- Ticket 47813 - managed entry plugin fails to update member  pointer on modrdn operation
- Ticket 47770 - #481 breaks possibility to reassemble memberuid list
- Ticket 47446 - logconv.pl memory continually grows
- Ticket 47713 - Logconv.pl with an empty access log gives lots of errors
- Ticket 47670 - Aci warnings in error log
- Ticket 47804 - db2bak.pl error with changelogdb
- Ticket 47780 - Some VLV search request causes memory leaks
- Ticket 47787 - A replicated MOD fails (Unwilling to perform) if it targets a tombstone
- Ticket 47764 - Problem with deletion while replicated
- Ticket 47750 - Creating a glue fails if one above level is a conflict or missing
- Ticket 47649 - Server hangs in cos_cache when adding a user entry
- Ticket 47772 - fix coverity issue
- Ticket 47793 - Server crashes if uniqueMember is invalid syntax and memberOf                plugin is enabled.
- Ticket 47707 - 389 DS Server crashes and dies while handles paged searches from clients
- Ticket 47771 - Move parentsdn initialization to avoid crash
- Ticket 47771 - Cherry pick issue parentsdn freed twice
- Ticket 47771 - Performing deletes during tombstone purging results in operation errors
- Ticket 346   - Slow ldapmodify operation time for large quantities of multi-valued attribute values
- Ticket 47782 - Parent numbordinate count can be incorrectly updated if an error occurs
- Ticket 47772 - empty modify returns LDAP_INVALID_DN_SYNTAX
- Ticket 47736 - Import incorrectly updates numsubordinates for tombstone entries
- Ticket 47774 - mem leak in do_search - rawbase not freed upon certain errors
- Ticket 47773 - mem leak in do_bind when there is an error
- Ticket 47767 - Nested tombstones become orphaned after purge

* Fri Apr  4 2014 Noriko Hosoi <nhosoi@redhat.com> - 1.2.11.29-1
- bump version to 1.2.11.29
- Ticket 47766 - Tombstone purging can crash the server if the backend is stopped/disabled
- Ticket 47492 - PassSync removes User must change password flag on the Windows side
- Ticket 47448 - Segfault in 389-ds-base-1.3.1.4-1.fc19 when setting up FreeIPA replication
- Ticket 47740 - Fix coverity issues(part 7)
- Ticket 47748 - Simultaneous adding a user and binding as the user could fail in the password policy check
- Ticket 47743 - Memory leak with proxy auth control
- Ticket 47740 - Crash caused by changes to certmap.c
- Ticket 47740 - Fix coverity issues: null deferences - Part 6
- Ticket 47735 - e_uniqueid fails to set if an entry is a conflict entry
- Ticket 47740 - Coverity issue in 1.3.3
- Ticket 47740 - Fix coverity issues - Part 5
- Ticket 47740 - Fix coverity erorrs - Part 4
- Ticket 47640 - Fix coverity issues - part 3
- Ticket 47538 - RFE: repl-monitor.pl plain text output, cmdline config options
- Ticket 47740 - Coverity Fixes (Mark - part 1)
- Ticket 47734 - Change made in resolving ticket #346 fails on Debian SPARC64
- Ticket 47722 - Fixed filter not correctly identified
- Ticket 47722 - rsearch filter error on any search filter
- Ticket 47704 - invalid sizelimits in aci group evaluation
- Ticket 47737 - Under heavy stress, failure of turning a tombstone into glue makes the server hung
- Ticket 47735 - e_uniqueid fails to set if an entry is a conflict entry
- Ticket 47731 - A tombstone entry is deleted by ldapdelete
- Ticket 47729 - Directory Server crashes if shutdown during a replication initialization
- Ticket 47637 - rsa_null_sha should not be enabled by default
- Ticket 417, 458, 47522 - Password Administrator Backport
- Ticket 47455 - valgrind - value mem leaks, uninit mem usage
- fix coverity 11915 - dead code - introduced with fix for ticket 346
- Ticket 47369 - version2 - provide default syntax plugin
- Ticket 346   - version 4 Slow ldapmodify operation time for large quantities of multi-valued attribute values
- Ticket 415   - winsync doesn't sync DN valued attributes if DS DN value doesn't exist
- Ticket 47642 - Windows Sync group issues
- Ticket 47692 - single valued attribute replicated ADD does not work
- Ticket 47677 - Size returned by slapi_entry_size is not accurate
- Ticket 47693 - Environment variables are not passed when DS is started via service
- Ticket 47693 - Environment variables are not passed when DS is started via service
- Ticket 471   - logconv.pl tool removes the access logs contents if "-M" is not correctly used
- Ticket 47463 - IDL-style can become mismatched during partial restoration
- Ticket 47638 - Overflow in nsslapd-disk-monitoring-threshold on 32bit platform
- Ticket 47641 - 7-bit check plugin not checking MODRDN operation
- Ticket 47678 - modify-delete userpassword
- Ticket 47516 - replication stops with excessive clock skew
- Ticket 47627 - Fix replication logging
- Ticket 47627 - changelog iteration should ignore cleaned rids when getting the minCSN
- Ticket 47623 - fix memleak caused by 47347
- Ticket 47587 - hard coded limit of 64 masters in agreement and changelog code
- Ticket 47591 - entries with empty objectclass attribute value can be hidden
- Ticket 47596 - attrcrypt fails to find unlocked key

* Fri Mar 14 2014 Noriko Hosoi <nhosoi@redhat.com> - 1.2.11.28-1
- bump version to 1.2.11.28 (This release is based upon 1.2.11.25 + following tickets.)
- Ticket 47739 - directory server is insecurely misinterpreting authzid on a SASL/GSSAPI bind
- Ticket 47731 - A tombstone entry is deleted by ldapdelete
- Ticket 47729 - Directory Server crashes if shutdown during a replication initialization
- Ticket 47637 - rsa_null_sha should not be enabled by default
- Ticket 417, 458, 47522 - Password Administrator Backport
- Ticket 47455 - valgrind - value mem leaks, uninit mem usage
- fix coverity 11915 - dead code - introduced with fix for ticket 346
- Ticket 47369  version2 - provide default syntax plugin
- Ticket 346 - version 4 Slow ldapmodify operation time for large quantities of multi-valued attribute values
- Ticket 415 - winsync doesn't sync DN valued attributes if DS DN value doesn't exist
- Ticket 47642 - Windows Sync group issues
- Ticket 47692 - single valued attribute replicated ADD does not work
- Ticket 47677 - Size returned by slapi_entry_size is not accurate
- Ticket 47693 - Environment variables are not passed when DS is started via service
- Ticket 47693 - Environment variables are not passed when DS is started via service
- Ticket 471 - logconv.pl tool removes the access logs contents if "-M" is not correctly used
- Ticket 47463 - IDL-style can become mismatched during partial restoration
- Ticket 47638 - Overflow in nsslapd-disk-monitoring-threshold on 32bit platform
- Ticket 47641 - 7-bit check plugin not checking MODRDN operation
- Ticket 47678 - modify-delete userpassword
- Ticket 47516 - replication stops with excessive clock skew
- Ticket 47627 - Fix replication logging
- Ticket 47627 - changelog iteration should ignore cleaned rids when getting the minCSN
- Ticket 47623 - fix memleak caused by 47347
- Ticket 47587 - hard coded limit of 64 masters in agreement and changelog code
- Ticket 47591 - entries with empty objectclass attribute value can be hidden
- Ticket 47596 - attrcrypt fails to find unlocked key

* Tue Mar 11 2014 Rich Megginson <rmeggins@redhat.com> - 1.2.11.26-2
- remove the wip patch

* Mon Mar 10 2014 Noriko Hosoi <nhosoi@redhat.com> - 1.2.11.26-1
- bump version to 1.2.11.26
- Ticket 47739 - directory server is insecurely misinterpreting authzid on a SASL/GSSAPI bind
- Ticket 47704 - invalid sizelimits in aci group evaluation
- Ticket 47737 - Under heavy stress, failure of turning a tombstone into glue makes the server hung
- Ticket 47735 - e_uniqueid fails to set if an entry is a conflict entry
- Ticket 47731 - A tombstone entry is deleted by ldapdelete
- Ticket 47729 - Directory Server crashes if shutdown during a replication initialization
- Ticket 47637 - rsa_null_sha should not be enabled by default
- Ticket 417, 458, 47522 - Password Administrator Backport
- Ticket 47455 - valgrind - value mem leaks, uninit mem usage
- fix coverity 11915 - dead code - introduced with fix for ticket 346
- Ticket 47369  version2 - provide default syntax plugin
- Ticket 346 - version 4 Slow ldapmodify operation time for large quantities of multi-valued attribute values
- Ticket 415 - winsync doesn't sync DN valued attributes if DS DN value doesn't exist
- Ticket 47642 - Windows Sync group issues
- Ticket 47692 - single valued attribute replicated ADD does not work
- Ticket 47677 - Size returned by slapi_entry_size is not accurate
- Ticket 47693 - Environment variables are not passed when DS is started via service
- Ticket 47693 - Environment variables are not passed when DS is started via service
- Ticket 471 - logconv.pl tool removes the access logs contents if "-M" is not correctly used
- Ticket 47463 - IDL-style can become mismatched during partial restoration
- Ticket 47638 - Overflow in nsslapd-disk-monitoring-threshold on 32bit platform
- Ticket 47641 - 7-bit check plugin not checking MODRDN operation
- Ticket 47678 - modify-delete userpassword
- Ticket 47516 - replication stops with excessive clock skew
- Ticket 47627 - Fix replication logging
- Ticket 47627 - changelog iteration should ignore cleaned rids when getting the minCSN
- Ticket 47623 - fix memleak caused by 47347
- Ticket 47587 - hard coded limit of 64 masters in agreement and changelog code
- Ticket 47591 - entries with empty objectclass attribute value can be hidden
- Ticket 47596 - attrcrypt fails to find unlocked key

* Thu Nov 21 2013 Rich Megginson <rmeggins@redhat.com> - 1.2.11.25-1
- Ticket #47605 CVE-2013-4485: DoS due to improper handling of ger attr searches
- Ticket #47596 attrcrypt fails to find unlocked key
- Revert "Ticket #47559 hung server - related to sasl and initialize"
- Ticket #47585 Replication Failures related to skipped entries due to cleaned rids
- Ticket #47581 - Winsync plugin segfault during incremental backoff (phase 2)
- Ticket #47581 - Winsync plugin segfault during incremental backoff
- Ticket 47577 - crash when removing entries from cache
- Ticket #47559 hung server - related to sasl and initialize
- fe52f44 ticket #47550 wip
- Ticket #47550 logconv: failed logins: Use of uninitialized value in numeric comparison at logconv.pl line 949
- Ticket #47551 logconv: -V does not produce unindexed search report
- Ticket 47517 - fix memory leak in ldbm_delete.c
- Ticket #47488 - Users from AD sub OU does not sync to IPA
- minor fixes for bdb 4.2/4.3 and mozldap
- Tickets: 47510 & 47543 - 389 fails to build when using Mozldap

* Tue Oct 15 2013 Rich Megginson <rmeggins@redhat.com> - 1.2.11.23-3.1
- add mutex around ldap ssl functions/bind/unbind

* Wed Oct  2 2013 Rich Megginson <rmeggins@redhat.com> - 1.2.11.23-3
- bump version to rebuild again

* Wed Oct  2 2013 Rich Megginson <rmeggins@redhat.com> - 1.2.11.23-2
- forgot to bump the source version

* Wed Oct  2 2013 Rich Megginson <rmeggins@redhat.com> - 1.2.11.23-1
- Ticket #422 - 389-ds-base - Can't call method "getText"
- Ticket 47509 - CLEANALLRUV doesnt run across all replicas
- Ticket 47533 logconv: some stats do not work across server restarts
- Ticket #47501 logconv.pl uses /var/tmp for BDB temp files
- Ticket 47520 - Fix various issues with logconv.pl
- Ticket #47387 - improve logconv.pl performance with large access logs
- Ticket 47354 - Indexed search are logged with 'notes=U' in the access logs
- Ticket 47461 - logconv.pl - Use of comma-less variable list is deprecated
- Ticket 47447 - logconv.pl man page missing -m,-M,-B,-D
- Ticket #47348 - add etimes to per second/minute stats
- Ticket #47341 - logconv.pl -m time calculation is wrong
- Ticket #47336 - logconv.pl -m not working for all stats
- Ticket 611 - logconv.pl missing stats for StartTLS, LDAPI, and AUTOBIND
- TIcket 419 - logconv.pl - improve memory management
- Ticket 471 - logconv.pl tool removes the access logs contents if "-M" is not correctly used
- Ticket 539 - logconv.pl should handle microsecond timing
- Ticket #356 - RFE - Track bind info
- Ticket #47534 - RUV tombstone search with scope "one" doesn`t work
- Ticket 47489 - Under specific values of nsDS5ReplicaName, replication may get broken or updates missing
- Ticket #47523 - Set up replcation/agreement before initializing the sub suffix, the sub suffix is not found by ldapsearch
- Ticket #47504 idlistscanlimit per index/type/value
- Ticket #47492 - PassSync removes User must change password flag on the Windows side
- Ticket #47516 replication stops with excessive clock skew
- Bug 999634 - ns-slapd crash due to bogus DN

* Fri Aug  2 2013 Rich Megginson <rmeggins@redhat.com> - 1.2.11.22-3
- use socket6 instead of socket

* Thu Aug  1 2013 Rich Megginson <rmeggins@redhat.com> - 1.2.11.22-2
- remove the dependency and conflict with selinux versions

* Wed Jul 31 2013 Rich Megginson <rmeggins@redhat.com> - 1.2.11.22-1
- 89a98eb fix coverity 11895 - null deref - caused by fix to ticket 47392
- 9750ea7 fix compiler warning in posix winsync code for posix_group_del_memberuid_callback
- 12d47a2 Fix compiler warnings for Ticket 47395 and 47397
- d9a1c7b fix compiler warning
- 855d289 Ticket #543 - Sorting with attributes in ldapsearch gives incorrect result
- CVE-2013-2219 ACLs inoperative in some search scenarios
- Ticket #47378 - fix recent compiler warnings
- Ticket 47427 - Overflow in nsslapd-disk-monitoring-threshold
- Ticket 47449 - deadlock after adding and deleting entries
- Ticket 47421 - memory leaks in set_krb5_creds
- Ticket 47441 - Disk Monitoring not checking filesystem with logs
- Ticket 47427 - Overflow in nsslapd-disk-monitoring-threshold
- Ticket #47435 - Very large entryusn values after enabling the USN plugin and the lastusn value is negative.
- Ticket #47424 - Replication problem with add-delete requests on single-valued attributes
- Ticket #47428 - Memory leak in 389-ds-base 1.2.11.15
- Ticket #47392 - ldbm errors when adding/modifying/deleting entries
- Ticket 47385 - Disk Monitoring is not triggered as expected.
- Ticket #47410 - changelog db deadlocks with DNA and replication
- Ticket #47409 - allow setting db deadlock rejection policy
- Ticket #47412 - Modify RUV should be serialized in ldbm_back_modify/add
- Ticket #47409 - allow setting db deadlock rejection policy
- Ticket 47393 - Attribute are not encrypted on a consumer after a full initialization
- Ticket 47396 - crash on modrdn of tombstone
- Ticket 47395 47397 v2 correct behaviour of account policy if only stateattr is configured or no alternate attr is configured
- Ticket #47402 - Attribute names are incorrect in search results
- Ticket #47391 - deleting and adding userpassword fails to update the password
- e3b8e2f Coverity Fixes (Part 7)
- Ticket 47376 - DESC should not be empty as per RFC 2252 (ldapv3)
- Ticket #47375 - flush_ber error sending back start_tls response will deadlock
- Ticket #47377 - make listen backlog size configurable
- Ticket #47367 - (phase 1) ldapdelete returns non-leaf entry error while trying to remove a leaf entry
- Ticket 47383 - connections attribute in cn=snmp,cn=monitor is counted twice
- Ticket 47385 - DS not shutting down when disk monitoring threshold is reached
- Ticket #47378 - fix recent compiler warnings
- 9ac276a Coverity Fixes (Part 5)
- 3ab5aba Coverity Fixes (Part 4)
- 36f2572 Coverity Fixes (Part 3)
- 41a8827 Coverity Fixes (Part 2)
- f771f95 Coverity Fixes (part 1)
- Ticket 580 - Wrong error code return when using EXTERNAL SASL and no client certificate
- Ticket #47349 - DS instance crashes under a high load
- Ticket #47359 - new ldap connections can block ldaps and ldapi connections
- Ticket #47327 - error syncing group if group member user is not synced
- Ticket #47362 - ipa upgrade selinuxusermap data not replicating
- Ticket 47361 - Empty control list causes LDAP protocol error is thrown
- Trac Ticket #531 - loading an entry from the database should use str2entry_fast
- Ticket #47347 - Simple paged results should support async search
- Ticket 623 - cleanAllRUV task fails to cleanup config upon completion
- 6abec15 Coverity fix 13139 - Dereference after NULL check in slapi_attr_value_normalize_ext()
 
* Tue Apr 9 2013 Mark Reynolds <mreynolds@redhat.com> - 1.2.11.21-1
9a7ba7d bump verison to 1.2.11.21
Ticket 47318 - server fails to start after upgrade(schema error)

* Thu Mar 28 2013 Noriko Hosoi <nhosoi@redhat.com> - 1.2.11.20-1
46bfabb bump version to 1.2.11.20
Ticket 623 - cleanAllRUV task fails to cleanup config upon completion
Ticket #47308 - unintended information exposure when anonymous access is set to rootdse
Ticket 628 - crash in aci evaluation
Ticket #627 - ns-slapd crashes sporadically with segmentation fault in libslapd.so
Ticket #634 - Deadlock in DNA plug-in
f6a6514 Coverity issue 13091
Ticket 632 - 389-ds-base cannot handle Kerberos tickets with PAC
Ticket 623 - cleanAllRUV task fails to cleanup config upon completion

* Mon Mar 11 2013 Mark Reynolds <mreynolds@redhat.com> - 1.2.11.19-1
c535f7d bump version to 1.2.11.19
Bug 912964 - CVE-2013-0312 389-ds: unauthenticated denial of service vulnerability in handling of LDAPv3 control data
Ticket 590 - ns-slapd segfaults while trying to delete a tombstone entry
Ticket 518 - dse.ldif is 0 length after server kill or machine kill
Ticket #579 - Error messages encountered when using POSIX winsync
Ticket #576 - DNA: use event queue for config update only at the start up
Ticket 367 - Invalid chaining config triggers a disk full error and shutdown
Ticket 570 - DS returns error 20 when replacing values of a multi-valued attribute  (only when replication is enabled)
Bug 906005 - Valgrind reports memleak in modify_update_last_modified_attr
Ticket #572 - PamConfig schema not updated during upgrade

* Thu Jan 24 2013 Mark Reynolds <mreynolds@redhat.com> - 1.2.11.18-1
12420d9 bump version to 1.2.11.18
Ticket 556 - Don't overwrite certmap.conf during upgrade
Ticket 495 - 1.2.11 - plugin dn is missing from pblock
Ticket 549 - DNA plugin no longer reports additional info when range is depleted
Ticket 541 - need to set plugin as off in ldif template
Ticket 541 - RootDN Access Control plugin is missing after upgrade
Ticket 527 - ns-slapd segfaults if it cannot rename the logs
39b0938 Coverity Issues for 1.2.11
Ticket 216 - disable replication agreements
Ticket 20 - Allow automember to work on entries that have already been added
7d22bc2 Coverity Fixes
Ticket 337 - improve CLEANRUV functionality
Ticket 495 - internalModifiersname not updated by DNA plugin
Ticket 517 - crash in DNA if no dnaMagicRegen is specified
Trac Ticket #520 - RedHat Directory Server crashes (segfaults) when moving ldap entry
Trac Ticket #519 - Search with a complex filter including range search is slow
Trac Ticket #500 - Newly created users with organizationalPerson objectClass fails to sync from AD to DS with missing attribute error
Ticket #503 - Improve AD version in winsync log message
Trac Ticket #498 - Cannot abaondon simple paged result search
55997a6 Coverity defects
Trac Ticket #494 - slapd entered to infinite loop during new index addition
56ebbb2 Fixing compiler warnings in the posix-winsync plugin
a57d913 Coverity defects
Ticket 468 - if pam_passthru is enabled, need to AC_CHECK_HEADERS([security/pam_appl.h])
Ticket 486 - nsslapd-enablePlugin should not be multivalued
Ticket 488 - Doc: DS error log messages with typo
Ticket #491 - multimaster_extop_cleanruv returns wrong error codes

* Mon Dec 10 2012 Mark Reynolds <mreynolds@redhat.com> - 1.2.11.17-1
- 94d5ea3 bump verison to 1.2.11.17
- Ticket 527 - ns-slapd segfaults if it cannot rename the logs
- 39b0938 Coverity Issues for 1.2.11
- Ticket 216 - disable replication agreements
- Ticket 20 - Allow automember to work on entries that have already been added
- 7d22bc2 Coverity Fixes
- Ticket 337 - improve CLEANRUV functionality
- Ticket 495 - internalModifiersname not updated by DNA plugin
- Ticket 517 - crash in DNA if no dnaMagicRegen is specified
- Trac Ticket #520 - RedHat Directory Server crashes (segfaults) when moving ldap entry
- Trac Ticket #519 - Search with a complex filter including range search is slow
- Trac Ticket #500 - Newly created users with organizationalPerson objectClass fails to sync from AD to DS with missing attribute error
- Ticket #503 - Improve AD version in winsync log message
- Trac Ticket #498 - Cannot abaondon simple paged result search
- 55997a6 Coverity defects
- Trac Ticket #494 - slapd entered to infinite loop during new index addition
- 56ebbb2 Fixing compiler warnings in the posix-winsync plugin
- a57d913 Coverity defects
- Ticket 468 - if pam_passthru is enabled, need to AC_CHECK_HEADERS([security/pam_appl.h])
- Ticket 486 - nsslapd-enablePlugin should not be multivalued
- Ticket 488 - Doc: DS error log messages with typo
- Ticket #491 - multimaster_extop_cleanruv returns wrong error codes

* Wed Oct 10 2012 Noriko Hosoi <nhosoi@redhat.com> - 1.2.11.16-1
- Ticket 340 - Change on SLAPI_MODRDN_NEWSUPERIOR is not evaluated in acl
- Ticket 446 - anonymous limits are being applied to directory manager
- Ticket 478 - passwordTrackUpdateTime stops working with subtree password policies
- Ticket 481 - expand nested posix groups
- Ticket 485 - Dirsrv deadlock locking up IPA

* Tue Sep 25 2012 Rich Megginson <rmeggins@redhat.com> - 1.2.11.15-1
- Ticket 470 - 389 prevents from adding a posixaccount with userpassword after schema reload
- Ticket 477 - CLEANALLRUV if there are only winsync agmts task will hang
- Ticket 457 - dirsrv init script returns 0 even when few or all instances fail to start
- Ticket 473 - change VERSION.sh to have console version be major.minor
- Ticket 475 - Root DN Access Control - improve value checking for config
- Trac Ticket #466 - entry_apply_mod - ADD: Failed to set unhashed#user#password to extension
- Ticket 474 - Root DN Access Control - days allowed not working correctly
- Ticket 467 - CLEANALLRUV abort task should be able to ignore down replicas
- 0b79915 fix compiler warnings in ticket 374 code
- Ticket 452 - automember rebuild task adds users to groups that do not match the configuration scope

* Fri Sep  7 2012 Rich Megginson <rmeggins@redhat.com> - 1.2.11.14-1
- Ticket 450 - CLEANALLRUV task gets stuck on winsync replication agreement
- Ticket 386 - large memory growth with ldapmodify(heap fragmentation)
-  this patch doesn't fix the bug - it allows us to experiment with
-  different values of mxfast
- Ticket #374 - consumer can go into total update mode for no reason

* Tue Sep  4 2012 Rich Megginson <rmeggins@redhat.com> - 1.2.11.13-1
- Ticket #426 - support posix schema for user and group sync
-   1) plugin config ldif must contain pluginid, etc. during upgrade or it
-      will fail due to schema errors
-   2) posix winsync should have a lower precedence (25) than the default (50)
-      so that it will be run first
-   3) posix winsync should support the Winsync API v3 - the v2 functions are
-      just stubs for now - but the precedence cb is active

* Thu Aug 30 2012 Rich Megginson <rmeggins@redhat.com> - 1.2.11.12-1
- 8e5087a Coverity defects - 13089: Dereference after null check ldbm_back_delete
- Trac Ticket #437 - variable dn should not be used in ldbm_back_delete
- ba1f5b2 fix coverity resource leak in windows_plugin_add
- e3e81db Simplify program flow: change while loops to for
- a0d5dc0 Fix logic errors: del_mod should be latched (might not be last mod), and avoid skipping add-mods (int value 0)
- 0808f7e Simplify program flow: make adduids/moduids/deluids action blocks all similar
- 77eb760 Simplify program flow: eliminate unnecessary continue
- c9e9db7 Memory leaks: unmatched slapi_attr_get_valueset and slapi_value_new
- a4ca0cc Change "return"s in modGroupMembership to "break"s to avoid leaking
- d49035c Factorize into new isPosixGroup function
- 3b61c03 coverity - posix winsync mem leaks, null check, deadcode, null ref, use after free
- 33ce2a9 fix mem leaks with parent dn log message, setting winsync windows domain
- Ticket #440 - periodic dirsync timed event causes server to loop repeatedly
- Ticket #355 - winsync should not delete entry that appears to be out of scope
- Ticket 436 - nsds5ReplicaEnabled can be set with any invalid values.
- 487932d coverity - mbo dead code - winsync leaks, deadcode, null check, test code
- 2734a71 CLEANALLRUV coverity fixes
- Ticket #426 - support posix schema for user and group sync
- Ticket #430 - server to server ssl client auth broken with latest openldap

* Mon Aug 20 2012 Mark Reynolds <mareynol@redhat.com> - 1.2.11.11-1
6c0778f bumped version to 1.2.11.11
Ticket 429 - added nsslapd-readonly to DS schema
Ticket 403 - fix CLEANALLRUV regression from last commit
Trac Ticket #346 - Slow ldapmodify operation time for large quantities of multi-valued attribute values

* Wed Aug 15 2012 Mark Reynolds <mareynol@redhat.com> - 1.2.11.10-1
db6b354 bumped version to 1.2.11.10
Ticket 403 - CLEANALLRUV revisions

* Tue Aug 7 2012 Mark Reynolds <mareynol@redhat.com> - 1.2.11.9-1
ea05e69 Bumped version to 1.2.11.9
Ticket 407 - dna memory leak - fix crash from prev fix

* Fri Aug 3 2012 Mark Reynolds <mareynol@redhat.com> - 1.2.11.8-1
ddcf669 bump version to 1.2.11.8 for offical release
Ticket #425 - support multiple winsync plugins
Ticket 403 - cleanallruv coverity fixes
Ticket 407 - memory leak in dna plugin
Ticket 403 - CLEANALLRUV feature
Ticket 413 - "Server is unwilling to perform" when running ldapmodify on nsds5ReplicaStripAttrs
3168f04 Coverity defects
5ff0a02 COVERITY FIXES
Ticket #388 - Improve replication agreement status messages
0760116 Update the slapi-plugin documentation on new slapi functions, and added a slapi function for checking on shutdowns
Ticket #369 - restore of replica ldif file on second master after deleting two records shows only 1 deletion
Ticket #409 - Report during startup if nsslapd-cachememsize is too small
Ticket #412 - memberof performance enhancement
12813: Uninitialized pointer read string_values2keys
Ticket #346 - Slow ldapmodify operation time for large quantities of multi-valued attribute values
Ticket #346 - Slow ldapmodify operation time for large quantities of multi-valued attribute values
Ticket #410 - Referential integrity plug-in does not work when update interval is not zero
Ticket #406 - Impossible to rename entry (modrdn) with Attribute Uniqueness plugin enabled
Ticket #405 - referint modrdn not working if case is different
Ticket 399 - slapi_ldap_bind() doesn't check bind results

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.11.7-2.2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jun 28 2012 Petr Pisar <ppisar@redhat.com> - 1.2.11.7-2.1
- Perl 5.16 rebuild

* Wed Jun 27 2012 Rich Megginson <rmeggins@redhat.com> - 1.2.11.7-2
- Ticket 378 - unhashed#user#password visible after changing password
-  fix func declaration from previous patch
- Ticket 366 - Change DS to purge ticket from krb cache in case of authentication error

* Wed Jun 27 2012 Rich Megginson <rmeggins@redhat.com> - 1.2.11.7-1
- Trac Ticket 396 - Account Usability Control Not Working

* Thu Jun 21 2012 Rich Megginson <rmeggins@redhat.com> - 1.2.11.6-1
- Ticket #378 - audit log does not log unhashed password: enabled, by default.
- Ticket #378 - unhashed#user#password visible after changing password
- Ticket #365 - passwords in clear text in the audit log

* Tue Jun 19 2012 Rich Megginson <rmeggins@redhat.com> - 1.2.11.5-2
- workaround for https://bugzilla.redhat.com/show_bug.cgi?id=833529

* Mon Jun 18 2012 Rich Megginson <rmeggins@redhat.com> - 1.2.11.5-1
- Ticket #387 - managed entry sometimes doesn't delete the managed entry
- 5903815 improve txn test index handling
- Ticket #360 - ldapmodify returns Operations error - fix delete caching
- bcfa9e3 Coverity Fix for CLEANALLRUV
- Trac Ticket #335 - transaction retries need to be cache aware
- Ticket #389 - ADD operations not in audit log
- 44cdc84 fix coverity issues with uninit vals, no return checking
- Ticket 368 - Make the cleanAllRUV task one step
- Ticket #110 - RFE limiting root DN by host, IP, time of day, day of week

* Tue May 22 2012 Rich Megginson <rmeggins@redhat.com> - 1.2.11.4-1
- Ticket #360 - ldapmodify returns Operations error
- Ticket #321 - krbExtraData is being null modified and replicated on each ssh login
- Trac Ticket #359 - Database RUV could mismatch the one in changelog under the stress
- Ticket #361: Bad DNs in ACIs can segfault ns-slapd
- Trac Ticket #338 - letters in object's cn get converted to lowercase when renaming object
- Ticket #337 - Improve CLEANRUV task

* Sat May  5 2012 Rich Megginson <rmeggins@redhat.com> - 1.2.11.3-1
- Ticket #358 - managed entry doesn't delete linked entry

* Fri May  4 2012 Rich Megginson <rmeggins@redhat.com> - 1.2.11.2-1
- Ticket #351 - use betxn plugins by default
-   revert - make no plugins betxn by default - too great a risk
-   for deadlocks until we can test this better
- Ticket #348 - crash in ldap_initialize with multiple threads
-   fixes PR_Init problem in ldclt

* Wed May  2 2012 Rich Megginson <rmeggins@redhat.com> - 1.2.11.1-1
- f227f11 Suppress alert on unavailable port with forced setup
- Ticket #353 - coverity 12625-12629 - leaks, dead code, unchecked return
- Ticket #351 - use betxn plugins by default
- Trac Ticket #345 - db deadlock return should not log error
- Ticket #348 - crash in ldap_initialize with multiple threads
- Ticket #214 - Adding Replication agreement should complain if required nsds5ReplicaCredentials not supplied
- Ticket #207 - [RFE] enable attribute that tracks when a password was last set
- Ticket #216 - RFE - Disable replication agreements
- Ticket #337 - RFE - Improve CLEANRUV functionality
- Ticket #326 - MemberOf plugin should work on all backends
- Trac Ticket #19 - Convert entryUSN plugin to transaction aware type
- Ticket #347 - IPA dirsvr seg-fault during system longevity test
- Trac Ticket #310 - Avoid calling escape_string() for logged DNs
- Trac Ticket #338 - letters in object's cn get converted to lowercase when renaming object
- Ticket #183 - passwordMaxFailure should lockout password one sooner
- Trac Ticket #335 - transaction retries need to be cache aware
- Ticket #336 - [abrt] 389-ds-base-1.2.10.4-2.fc16: index_range_read_ext: Process /usr/sbin/ns-slapd was killed by signal 11 (SIGSEGV)
- Ticket #325 - logconv.pl : use of getopts to parse command line options
- Ticket #336 - [abrt] 389-ds-base-1.2.10.4-2.fc16: index_range_read_ext: Process /usr/sbin/ns-slapd was killed by signal 11 (SIGSEGV)
- 554e29d Coverity Fixes
- Trac Ticket #46 - (additional 2) setup-ds-admin.pl does not like ipv6 only hostnames
- Ticket #183 - passwordMaxFailure should lockout password one sooner - and should be configurable to avoid regressions
- Ticket #315 - small fix to libglobs
- Ticket #315 - ns-slapd exits/crashes if /var fills up
- Ticket #20 - Allow automember to work on entries that have already been added
- Trac Ticket #45 - Fine Grained Password policy: if passwordHistory is on, deleting the password fails.

* Fri Mar 30 2012 Rich Megginson <rmeggins@redhat.com> - 1.2.11-0.1.a1
- 453eb97 schema def must have DESC '' - close paren must be preceded by space
- Trac Ticket #46 - (additional) setup-ds-admin.pl does not like ipv6 only hostnames
- Ticket #331 - transaction errors with db 4.3 and db 4.2
- Ticket #261 - Add Solaris i386
- Ticket #316 and Ticket #70 - add post add/mod and AD add callback hooks
- Ticket #324 - Sync with group attribute containing () fails
- Ticket #319 - ldap-agent crashes on start with signal SIGSEGV
- 77cacd9 coverity 12606 Logically dead code
- Trac Ticket #303 - make DNA range requests work with transactions
- Ticket #320 - allow most plugins to be betxn plugins
- Ticket #24 - Add nsTLS1 to the DS schema
- Ticket #271 - Slow shutdown when you have 100+ replication agreements
- TIcket #285 - compilation fixes for '--format-security'
- Ticket 211 - Avoid preop range requests non-DNA operations
- Ticket #271 - replication code cleanup
- Ticket 317 - RHDS fractional replication with excluded password policy attributes leads to wrong error messages.
- Ticket #308 - Automembership plugin fails if data and config area mixed in the plugin configuration
- Ticket #292 - logconv.pl reporting unindexed search with different search base than shown in access logs
- 6f8680a coverity 12563 Read from pointer after free (fix 2)
- e6a9b22 coverity 12563 Read from pointer after free
- 245d494 Config changes fail because of unknown attribute "internalModifiersname"
- Ticket #191  - Implement SO_KEEPALIVE in network calls
- Ticket #289 - allow betxn plugin config changes
- 93adf5f destroy the entry cache and dn cache in the dse post op delete callback
- e2532d8 init txn thread private data for all database modes
- Ticket #291 - cannot use & in a sasl map search filter
- 6bf6e79 Schema Reload crash fix
- 60b2d12 Fixing compiler warnings
- Trac Ticket #260 - 389 DS does not support multiple paging controls on a single connection
- Ticket #302 - use thread local storage for internalModifiersName & internalCreatorsName
- fdcc256 Minor bug fix introcuded by commit 69c9f3bf7dd9fe2cadd5eae0ab72ce218b78820e
- Ticket #306 - void function cannot return value
- ticket 181 - Allow PAM passthru plug-in to have multiple config entries
- ticket 211 - Use of uninitialized variables in ldbm_back_modify()
- Ticket #74 - Add schema for DNA plugin (RFE)
- Ticket #301 - implement transaction support using thread local storage
- Ticket #211 - dnaNextValue gets incremented even if the user addition fails
- 144af59 coverity uninit var and resource leak
- Trac Ticket #34 - remove-ds.pl does not remove everything
- Trac Ticket #169 - allow 389 to use db5
- bc78101 fix compiler warning in acct policy plugin
- Trac Ticket #84 - 389 Directory Server Unnecessary Checkpoints
- Trac Ticket #27 - SASL/PLAIN binds do not work
- Ticket #129 - Should only update modifyTimestamp/modifiersName on MODIFYops
- Ticket #17 - new replication optimizations

* Tue Mar 27 2012 Noriko Hosoi <nhosoi@redhat.com> - 1.2.10.4-4
- Ticket #46 - (revised) setup-ds-admin.pl does not like ipv6 only hostnames
- Ticket #66 - 389-ds-base spec file does not have a BuildRequires on gcc-c++

* Fri Mar 23 2012 Noriko Hosoi <nhosoi@redhat.com> - 1.2.10.4-3
- Ticket #46 - setup-ds-admin.pl does not like ipv6 only hostnames

* Wed Mar 21 2012 Rich Megginson <rmeggins@redhat.com> - 1.2.10.4-2
- get rid of posttrans - move update code to post

* Tue Mar 13 2012 Rich Megginson <rmeggins@redhat.com> - 1.2.10.4-1
- Ticket #305 - Certain CMP operations hang or cause ns-slapd to crash

* Mon Mar  5 2012 Rich Megginson <rmeggins@redhat.com> - 1.2.10.3-1
- b05139b memleak in normalize_mods2bvals
- c0eea24 memleak in mep_parse_config_entry
- 90bc9eb handle null smods
- Ticket #305 - Certain CMP operations hang or cause ns-slapd to crash
- Ticket #306 - void function cannot return value
- ticket 304 - Fix kernel version checking in dsktune

* Thu Feb 23 2012 Rich Megginson <rmeggins@redhat.com> - 1.2.10.2-1
- Trac Ticket #298 - crash when replicating orphaned tombstone entry
- Ticket #281 - TLS not working with latest openldap
- Trac Ticket #290 - server hangs during shutdown if betxn pre/post op fails
- Trac Ticket #26 - Please support setting defaultNamingContext in the rootdse

* Tue Feb 14 2012 Noriko Hosoi <nhosoi@redhat.com> - 1.2.10.1-2
- Ticket #124 - add Provides: ldif2ldbm to rpm

* Tue Feb 14 2012 Rich Megginson <rmeggins@redhat.com> - 1.2.10.1-1
- Ticket #294 - 389 DS Segfaults during replica install in FreeIPA

* Mon Feb 13 2012 Rich Megginson <rmeggins@redhat.com> - 1.2.10.0-1
- Ticket 284 - Remove unnecessary SNMP MIB files
- Ticket 51 - memory leaks in 389-ds-base-1.2.8.2-1.el5?
- Ticket 175 - logconv.pl improvements

* Fri Feb 10 2012 Noriko Hosoi <nhosoi@redhat.com> - 1.2.10-0.10.rc1.2
- Introducing use_db4 macro to support db5 (libdb).

* Fri Feb 10 2012 Petr Pisar <ppisar@redhat.com> - 1.2.10-0.10.rc1.1
- Rebuild against PCRE 8.30

* Thu Feb  2 2012 Rich Megginson <rmeggins@redhat.com> - 1.2.10-0.10.rc1
- ad9dd30 coverity 12488 Resource leak In attr_index_config(): Leak of memory or pointers to system resources
- Ticket #281 - TLS not working with latest openldap
- Ticket #280 - extensible binary filters do not work
- Ticket #279 - filter normalization does not use matching rules
- Trac Ticket #275 - Invalid read reported by valgrind
- Ticket #277 - cannot set repl referrals or state
- Ticket #278 - Schema replication update failed: Invalid syntax
- Ticket #39 - Account Policy Plugin does not work for simple binds when PAM Pass Through Auth plugin is enabled
- Ticket #13 - slapd process exits when put the database on read only mode while updates are coming to the server
- Ticket #87 - Manpages fixes
- c493fb4 fix a couple of minor coverity issues
- Ticket #55 - Limit of 1024 characters for nsMatchingRule
- Trac Ticket #274 - Reindexing entryrdn fails if ancestors are also tombstoned
- Ticket #6 - protocol error from proxied auth operation
- Ticket #38 - nisDomain schema is incorrect
- Ticket #273 - ruv tombstone searches don't work after reindex entryrdn
- Ticket #29 - Samba3-schema is missing sambaTrustedDomainPassword
- Ticket #22 - RFE: Support sendmail LDAP routing schema
- Ticket #161 - Review and address latest Coverity issues
- Ticket #140 - incorrect memset parameters
- Trac Ticket 35 - Log not clear enough on schema errors
- Trac Ticket 139 - eliminate the use of char *dn in favor of Slapi_DN *dn
- Trac Ticket #52 - FQDN set to nsslapd-listenhost makes the server start fail if IPv4-mapped-IPv6 address is given

* Tue Jan 24 2012 Rich Megginson <rmeggins@redhat.com> - 1.2.10-0.9.a8
- Ticket #272 - add tombstonenumsubordinates to schema

* Mon Jan 23 2012 Rich Megginson <rmeggins@redhat.com> - 1.2.10-0.8.a7
- fixes for systemd - remove .pid files after shutting down servers
- Ticket #263 - add systemd include directive
- Ticket #264 - upgrade needs better check for "server is running"

* Fri Jan 20 2012 Rich Megginson <rmeggins@redhat.com> - 1.2.10-0.7.a7
- Ticket #262 - pid file not removed with systemd
- Ticket #50 - server should not call a plugin after the plugin close function is called
- Ticket #18 - Data inconsitency during replication
- Ticket #49 - better handling for server shutdown while long running tasks are active
- Ticket #15 - Get rid of rwlock.h/rwlock.c and just use slapi_rwlock instead
- Ticket #257 - repl-monitor doesn't work if leftmost hostnames are the same
- Ticket #12 - 389 DS DNA Plugin / Replication failing on GSSAPI
- 6aaeb77 add a hack to disable sasl hostname canonicalization
- Ticket 168 - minssf should not apply to rootdse
- Ticket #177 - logconv.pl doesn't detect restarts
- Ticket #159 - Managed Entry Plugin runs against managed entries upon any update without validating
- Ticket 75 - Unconfigure plugin opperations are being called.
- Ticket 26 - Please support setting defaultNamingContext in the rootdse.
- Ticket #71 - unable to delete managed entry config
- Ticket #167 - Mixing transaction and non-transaction plugins can cause deadlock
- Ticket #256 - debug build assertion in ACL_EvalDestroy()
- Ticket #4 - bak2db gets stuck in infinite loop
- Ticket #162 - Infinite loop / spin inside strcmpi_fast, acl_read_access_allowed_on_attr, server DoS
- Ticket #3: acl cache overflown problem
- Ticket 1 - pre-normalize filter and pre-compile substring regex - and other optimizations
- Ticket 2 - If node entries are tombstone'd, subordinate entries fail to get the full DN.

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.10-0.6.a6.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Dec 15 2011 Rich Megginson <rmeggins@redhat.com> - 1.2.10-0.6.a6
- Bug 755725 - 389 programs linked against openldap crash during shutdown
- Bug 755754 - Unable to start dirsrv service using systemd
- Bug 745259 - Incorrect entryUSN index under high load in replicated environment
- d439e3a use slapi_hexchar2int and slapi_str_to_u8 everywhere
- 5910551 csn_init_as_string should not use sscanf
- b53ba00 reduce calls to csn_as_string and slapi_log_error
- c897267 fix member variable name error in slapi_uniqueIDFormat
- 66808e5 uniqueid formatting - use slapi_u8_to_hex instead of sprintf
- 580a875 csn_as_string - use slapi_uN_to_hex instead of sprintf
- Bug 751645 - crash when simple paged fails to send entry to client
- Bug 752155 - Use restorecon after creating init script lock file

* Fri Nov  4 2011 Rich Megginson <rmeggins@redhat.com> - 1.2.10-0.5.a5
- Bug 751495 - 'setup-ds.pl -u' fails with undefined routine 'updateSystemD'
- Bug 750625 750624 750622 744946 Coverity issues
- Bug 748575 - part 2 - rhds81 modrdn operation and 100% cpu use in replication
- Bug 748575 - rhds81 modrn operation and 100% cpu use in replication
- Bug 745259 - Incorrect entryUSN index under high load in replicated environment
- f639711 Reduce the number of DN normalization
- c06a8fa Keep unhashed password psuedo-attribute in the adding entry
- Bug 744945 - nsslapd-counters attribute value cannot be set to "off"
- 8d3b921 Use new PLUGIN_CONFIG_ENTRY feature to allow switching between txn and regular
- d316a67 Change referential integrity to be a betxnpostoperation plugin

* Fri Oct  7 2011 Rich Megginson <rmeggins@redhat.com> - 1.2.10-0.4.a4
- Bug 741744 - part3 - MOD operations with chained delete/add get back error 53
- 1d2f5a0 make memberof transaction aware and able to be a betxnpostoperation plug in
- b6d3ba7 pass the plugin config entry to the plugin init function
- 28f7bfb set the ENTRY_POST_OP for modrdn betxnpostoperation plugins
- Bug 743966 - Compiler warnings in account usability plugin

* Wed Oct  5 2011 Rich Megginson <rmeggins@redhat.com> - 1.2.10.a3-0.3
- 498c42b fix transaction support in ldbm_delete

* Wed Oct  5 2011 Rich Megginson <rmeggins@redhat.com> - 1.2.10.a2-0.2
- Bug 740942 - allow resource limits to be set for paged searches independently of limits for other searches/operations
- Bug 741744 - MOD operations with chained delete/add get back error 53 on backend config
- Bug 742324 - allow nsslapd-idlistscanlimit to be set dynamically and per-user

* Wed Sep 21 2011 Rich Megginson <rmeggins@redhat.com> - 1.2.10.a1-0.1
- Bug 695736 - Providing native systemd file

* Wed Sep  7 2011 Rich Megginson <rmeggins@redhat.com> - 1.2.9.10-2
- corrected source

* Wed Sep  7 2011 Rich Megginson <rmeggins@redhat.com> - 1.2.9.10-1
- Bug 735114 - renaming a managed entry does not update mepmanagedby

* Thu Sep  1 2011 Rich Megginson <rmeggins@redhat.com> - 1.2.9.9-1
- Bug 735121 - simple paged search + ip/dns based ACI hangs server
- Bug 722292 - (cov#11030) Leak of mapped_sdn in winsync rename code
- Bug 703990 - cross-platform - Support upgrade from Red Hat Directory Server
- Introducing an environment variable USE_VALGRIND to clean up the entry cache and dn cache on exit.

* Wed Aug 31 2011 Rich Megginson <rmeggins@redhat.com> - 1.2.9.8-1
- Bug 732153 - subtree and user account lockout policies implemented?
- Bug 722292 - Entries in DS are not updated properly when using WinSync API

* Wed Aug 24 2011 Rich Megginson <rmeggins@redhat.com> - 1.2.9.7-1
- Bug 733103 - large targetattr list with syntax errors cause server to crash or hang
- Bug 633803 - passwordisglobalpolicy attribute brakes TLS chaining
- Bug 732541 - Ignore error 32 when adding automember config
- Bug 728592 - Allow ns-slapd to start with an invalid server cert

* Wed Aug 10 2011 Rich Megginson <rmeggins@redhat.com> - 1.2.9.6-1
- Bug 728510 - Run dirsync after sending updates to AD
- Bug 729717 - Fatal error messages when syncing deletes from AD
- Bug 729369 - upgrade DB to upgrade from entrydn to entryrdn format is not working.
- Bug 729378 - delete user subtree container in AD + modify password in DS == DS crash
- Bug 723937 - Slapi_Counter API broken on  32-bit F15
-   fixed again - separate tests for atomic ops and atomic bool cas

* Mon Aug  8 2011 Rich Megginson <rmeggins@redhat.com> - 1.2.9.5-1
- Bug 727511 - ldclt SSL search requests are failing with "illegal error number -1" error
-  Fix another coverity NULL deref in previous patch

* Thu Aug  4 2011 Rich Megginson <rmeggins@redhat.com> - 1.2.9.4-1
- Bug 727511 - ldclt SSL search requests are failing with "illegal error number -1" error
-  Fix coverity NULL deref in previous patch

* Wed Aug  3 2011 Rich Megginson <rmeggins@redhat.com> - 1.2.9.3-1
- Bug 727511 - ldclt SSL search requests are failing with "illegal error number -1" error
-  previous patch broke build on el5

* Wed Aug  3 2011 Rich Megginson <rmeggins@redhat.com> - 1.2.9.2-1
- Bug 727511 - ldclt SSL search requests are failing with "illegal error number -1" error

* Tue Aug  2 2011 Rich Megginson <rmeggins@redhat.com> - 1.2.9.1-2
- Bug 723937 - Slapi_Counter API broken on  32-bit F15
-   fixed to use configure test for GCC provided 64-bit atomic functions

* Wed Jul 27 2011 Rich Megginson <rmeggins@redhat.com> - 1.2.9.1-1
- Bug 663752 - Cert renewal for attrcrypt and encchangelog
-   this was "re-fixed" due to a deadlock condition with cl2ldif task cancel
- Bug 725953 - Winsync: DS entries fail to sync to AD, if the User's CN entry contains a comma
- Bug 725743 - Make memberOf use PRMonitor for it's operation lock
- Bug 725542 - Instance upgrade fails when upgrading 389-ds-base package
- Bug 723937 - Slapi_Counter API broken on  32-bit F15

* Thu Jul 21 2011 Petr Sabata <contyk@redhat.com> - 1.2.9.0-1.2
- Perl mass rebuild

* Wed Jul 20 2011 Petr Sabata <contyk@redhat.com> - 1.2.9.0-1.1
- Perl mass rebuild

* Fri Jul 15 2011 Rich Megginson <rmeggins@redhat.com> - 1.2.9.0-1
- Bug 720059 - RDN with % can cause crashes or missing entries
- Bug 709468 - RSA Authentication Server timeouts when using simple paged results on RHDS 8.2.
- Bug 691313 - Need TLS/SSL error messages in repl status and errors log
- Bug 712855 - Directory Server 8.2 logs "Netscape Portable Runtime error -5961 (TCP connection reset by peer.)" to error log whereas Directory Server 8.1 did not
- Bug 713209 - Update sudo schema
- Bug 719069 - clean up compiler warnings in 389-ds-base 1.2.9
- Bug 718303 - Intensive updates on masters could break the consumer's cache
- Bug 711679 - unresponsive LDAP service when deleting vlv on replica

* Mon Jun 27 2011 Rich Megginson <rmeggins@redhat.com> - 1.2.9-0.2.a2
- 389-ds-base-1.2.9.a2
- look for separate openldap ldif library
- Split automember regex rules into separate entries
- writing Inf file shows SchemaFile = ARRAY(0xhexnum)
- add support for ldif files with changetype: add
- Bug 716980 - winsync uses old AD entry if new one not found
- Bug 697694 - rhds82 - incr update state stop_fatal_error "requires administrator action", with extop_result: 9
- bump console version to 1.2.6
- Bug 711679 - unresponsive LDAP service when deleting vlv on replica
- Bug 703703 - setup-ds-admin.pl asks for legal agreement to a non-existant file
- Bug 706209 - LEGAL: RHEL6.1 License issue for 389-ds-base package
- Bug 663752 - Cert renewal for attrcrypt and encchangelog
- Bug 706179 - DS can not restart after create a new objectClass has entryusn attribute
- Bug 711906 - ns-slapd segfaults using suffix referrals
- Bug 707384 - only allow FIPS approved cipher suites in FIPS mode
- Bug 710377 - Import with chain-on-update crashes ns-slapd
- Bug 709826 - Memory leak: when extra referrals configured

* Fri Jun 17 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1.2.9-0.1.a1.2
- Perl mass rebuild

* Fri Jun 10 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1.2.9-0.1.a1.1
- Perl 5.14 mass rebuild

* Thu May 26 2011 Rich Megginson <rmeggins@redhat.com> - 1.2.9-0.1.a1
- 389-ds-base-1.2.9.a1
- Auto Membership
- More Coverity fixes

* Mon May  2 2011 Rich Megginson <rmeggins@redhat.com> - 1.2.8.3-1
- 389-ds-base-1.2.8.3
- Bug 700145 - userpasswd not replicating
- Bug 700557 - Linked attrs callbacks access free'd pointers after close
- Bug 694336 - Group sync hangs Windows initial Sync
- Bug 700215 - ldclt core dumps
- Bug 695779 - windows sync can lose old values when a new value is added
- Bug 697027 - 12 - minor memory leaks found by Valgrind + TET

* Thu Apr 14 2011 Rich Megginson <rmeggins@redhat.com> - 1.2.8.2-1
- 389-ds-base-1.2.8.2
- Bug 696407 - If an entry with a mixed case RDN is turned to be
-    a tombstone, it fails to assemble DN from entryrdn

* Fri Apr  8 2011 Rich Megginson <rmeggins@redhat.com> - 1.2.8.1-1
- 389-ds-base-1.2.8.1
- Bug 693962 - Full replica push loses some entries with multi-valued RDNs

* Tue Apr  5 2011 Rich Megginson <rmeggins@redhat.com> - 1.2.8.0-1
- 389-ds-base-1.2.8.0
- Bug 693473 - rhds82 rfe - windows_tot_run to log Sizelimit exceeded instead of LDAP error - -1
- Bug 692991 - rhds82 - windows_tot_run: failed to obtain data to send to the consumer; LDAP error - -1
- Bug 693466 - Unable to change schema online
- Bug 693503 - matching rules do not inherit from superior attribute type
- Bug 693455 - nsMatchingRule does not work with multiple values
- Bug 693451 - cannot use localized matching rules
- Bug 692331 - Segfault on index update during full replication push on 1.2.7.5

* Mon Apr  4 2011 Rich Megginson <rmeggins@redhat.com> - 1.2.8-0.10.rc5
- 389-ds-base-1.2.8.rc5
- Bug 692469 - Replica install fails after step for "enable GSSAPI for replication"

* Tue Mar 29 2011 Rich Megginson <rmeggins@redhat.com> - 1.2.8-0.9.rc4
- 389-ds-base-1.2.8.rc4
- Bug 668385 - DS pipe log script is executed as many times as the dirsrv serv
ice is restarted
- 389-ds-base-1.2.8.rc3
- Bug 690955 - Mrclone fails due to the replica generation id mismatch

* Tue Mar 22 2011 Rich Megginson <rmeggins@redhat.com> - 1.2.8-0.8.rc2
- 389-ds-base-1.2.8 release candidate 2 - git tag 389-ds-base-1.2.8.rc2
- Bug 689537 - (cov#10610) Fix Coverity NULL pointer dereferences
- Bug 689866 - ns-newpwpolicy.pl needs to use the new DN format
- Bug 681015 - RFE: allow fine grained password policy duration attributes
-              in days, hours, minutes, as well
- Bug 684996 - Exported tombstone cannot be imported correctly
- Bug 683250 - slapd crashing when traffic replayed
- Bug 668909 - Can't modify replication agreement in some cases
- Bug 504803 - Allow maxlogsize to be set if logmaxdiskspace is -1
- Bug 644784 - Memory leak in "testbind.c" plugin
- Bug 680558 - Winsync plugin fails to restrain itself to the configured subtree

* Mon Mar  7 2011 Caolán McNamara <caolanm@redhat.com> - 1.2.8-0.7.rc1
- rebuild for icu 4.6

* Wed Mar  2 2011 Rich Megginson <rmeggins@redhat.com> - 1.2.8-0.6.rc1
- 389-ds-base-1.2.8 release candidate 1 - git tag 389-ds-base-1.2.8.rc1
- Bug 518890 - setup-ds-admin.pl - improve hostname validation
- Bug 681015 - RFE: allow fine grained password policy duration attributes in 
-     days, hours, minutes, as well
- Bug 514190 - setup-ds-admin.pl --debug does not log to file
- Bug 680555 - ns-slapd segfaults if I have more than 100 DBs
- Bug 681345 - setup-ds.pl should set SuiteSpotGroup automatically
- Bug 674852 - crash in ldap-agent when using OpenLDAP
- Bug 679978 - modifying attr value crashes the server, which is supposed to
-     be indexed as substring type, but has octetstring syntax
- Bug 676655 - winsync stops working after server restart
- Bug 677705 - ds-logpipe.py script is failing to validate "-s" and
-     "--serverpid" options with "-t".
- Bug 625424 - repl-monitor.pl doesn't work in hub node

* Mon Feb 28 2011 Rich Megginson <rmeggins@redhat.com> - 1.2.8-0.5.a3
- Bug 676598 - 389-ds-base multilib: file conflicts
- split off libs into a separate -libs package

* Thu Feb 24 2011 Rich Megginson <rmeggins@redhat.com> - 1.2.8-0.4.a3
- do not create /var/run/dirsrv - setup will create it instead
- remove the fedora-ds initscript upgrade stuff - we do not support that anymore
- convert the remaining lua stuff to plain old shell script

* Wed Feb  9 2011 Rich Megginson <rmeggins@redhat.com> - 1.2.8-0.3.a3
- 1.2.8.a3 release - git tag 389-ds-base-1.2.8.a3
- Bug 675320 - empty modify operation with repl on or lastmod off will crash server
- Bug 675265 - preventryusn gets added to entries on a failed delete
- Bug 677774 - added support for tmpfiles.d
- Bug 666076 - dirsrv crash (1.2.7.5) with multiple simple paged result search
es
- Bug 672468 - Don't use empty path elements in LD_LIBRARY_PATH
- Bug 671199 - Don't allow other to write to rundir
- Bug 678646 - Ignore tombstone operations in managed entry plug-in
- Bug 676053 - export task followed by import task causes cache assertion
- Bug 677440 - clean up compiler warnings in 389-ds-base 1.2.8
- Bug 675113 - ns-slapd core dump in windows_tot_run if oneway sync is used
- Bug 676689 - crash while adding a new user to be synced to windows
- Bug 604881 - admin server log files have incorrect permissions/ownerships
- Bug 668385 - DS pipe log script is executed as many times as the dirsrv serv
ice is restarted
- Bug 675853 - dirsrv crash segfault in need_new_pw()

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.8-0.2.a2.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Feb  3 2011 Rich Megginson <rmeggins@redhat.com> - 1.2.8-0.2.a2
- 1.2.8.a2 release - git tag 389-ds-base-1.2.8.a2
- Bug 674430 - Improve error messages for attribute uniqueness
- Bug 616213 - insufficient stack size for HP-UX on PA-RISC
- Bug 615052 - intrinsics and 64-bit atomics code fails to compile
-    on PA-RISC
- Bug 151705 - Need to update Console Cipher Preferences with new ciphers
- Bug 668862 - init scripts return wrong error code
- Bug 670616 - Allow SSF to be set for local (ldapi) connections
- Bug 667935 - DS pipe log script's logregex.py plugin is not redirecting the 
-    log output to the text file
- Bug 668619 - slapd stops responding
- Bug 624547 - attrcrypt should query the given slot/token for
-    supported ciphers
- Bug 646381 - Faulty password for nsmultiplexorcredentials does not give any 
-    error message in logs

* Fri Jan 21 2011 Nathan Kinder <nkinder@redhat.com> - 1.2.8-0.1.a1
- 1.2.8-0.1.a1 release - git tag 389-ds-base-1.2.8.a1
- many bug fixes

* Thu Dec 16 2010 Rich Megginson <rmeggins@redhat.com> - 1.2.7.5-1
- 1.2.7.5 release - git tag 389-ds-base-1.2.7.5
- Bug 663597 - Memory leaks in normalization code

* Tue Dec 14 2010 Rich Megginson <rmeggins@redhat.com> - 1.2.7.4-2
- Resolves: bug 656541 - use %ghost on files in /var/lock

* Fri Dec 10 2010 Rich Megginson <rmeggins@redhat.com> - 1.2.7.4-1
- 1.2.7.4 release - git tag 389-ds-base-1.2.7.4
- Bug 661792 - Valid managed entry config rejected

* Wed Dec  8 2010 Rich Megginson <rmeggins@redhat.com> - 1.2.7.3-1
- 1.2.7.3 release - git tag 389-ds-base-1.2.7.3
- Bug 658312 - Invalid free in Managed Entry plug-in
- Bug 641944 - Don't normalize non-DN RDN values

* Fri Dec  3 2010 Rich Megginson <rmeggins@redhat.com> - 1.2.7.2-1
- 1.2.7.2 release - git tag 389-ds-base-1.2.7.2
- Bug 659456 - Incorrect usage of ber_printf() in winsync code
- Bug 658309 - Process escaped characters in managed entry mappings
- Bug 197886 - Initialize return value for UUID generation code
- Bug 658312 - Allow mapped attribute types to be quoted
- Bug 197886 - Avoid overflow of UUID generator

* Tue Nov 23 2010 Rich Megginson <rmeggins@redhat.com> - 1.2.7.1-2
- last commit had bogus commit log

* Tue Nov 23 2010 Rich Megginson <rmeggins@redhat.com> - 1.2.7.1-1
- 1.2.7.1 release - git tag 389-ds-base-1.2.7.1
- Bug 656515 - Allow Name and Optional UID syntax for grouping attributes
- Bug 656392 - Remove calls to ber_err_print()
- Bug 625950 - hash nsslapd-rootpw changes in audit log

* Tue Nov 16 2010 Nathan Kinder <nkinder@redhat.com> - 1.2.7-2
- 1.2.7 release - git tag 389-ds-base-1.2.7

* Fri Nov 12 2010 Nathan Kinder <nkinder@redhat.com> - 1.2.7-1
- Bug 648949 - Merge dirsrv and dirsrv-admin policy modules into base policy

* Tue Nov  9 2010 Rich Megginson <rmeggins@redhat.com> - 1.2.7-0.6.a5
- 1.2.7.a5 release - git tag 389-ds-base-1.2.7.a5
- Bug 643979 - Strange byte sequence for attribute with no values (nsslapd-ref
erral)
- Bug 635009 - Add one-way AD sync capability
- Bug 572018 - Upgrading from 1.2.5 to 1.2.6.a2 deletes userRoot
- put replication config entries in separate file
- Bug 567282 - server can not abandon searchRequest of "simple paged results"
- Bug 329751 - "nested" filtered roles searches candidates more than needed
- Bug 521088 - DNA should check ACLs before getting a value from the range

* Mon Nov  1 2010 Rich Megginson <rmeggins@redhat.com> - 1.2.7-0.5.a4
- 1.2.7.a4 release - git tag 389-ds-base-1.2.7.a4
- Bug 647932 - multiple memberOf configuration adding memberOf where there is 
no member
- Bug 491733 - dbtest crashes
- Bug 606545 - core schema should include numSubordinates
- Bug 638773 - permissions too loose on pid and lock files
- Bug 189985 - Improve attribute uniqueness error message
- Bug 619623 - attr-unique-plugin ignores requiredObjectClass on modrdn operat
ions
- Bug 619633 - Make attribute uniqueness obey requiredObjectClass

* Wed Oct 27 2010 Rich Megginson <rmeggins@redhat.com> - 1.2.7-0.4.a3
- 1.2.7.a3 release - a2 was never released - this is a rebuild to pick up
- Bug 644608 - RHDS 8.1->8.2 upgrade fails to properly migrate ACIs
- Adding the ancestorid fix code to ##upgradednformat.pl.

* Fri Oct 22 2010 Rich Megginson <rmeggins@redhat.com> - 1.2.7-0.3.a3
- 1.2.7.a3 release - a2 was never released
- Bug 644608 - RHDS 8.1->8.2 upgrade fails to properly migrate ACIs
- Bug 629681 - Retro Changelog trimming does not behave as expected
- Bug 645061 - Upgrade: 06inetorgperson.ldif and 05rfc4524.ldif
-              are not upgraded in the server instance schema dir

* Tue Oct 19 2010 Rich Megginson <rmeggins@redhat.com> - 1.2.7-0.2.a2
- 1.2.7.a2 release - a1 was the OpenLDAP testday release
- git tag 389-ds-base-1.2.7.a2
- added openldap support on platforms that use openldap with moznss
- for crypto (F-14 and later)
- many bug fixes
- Account Policy Plugin (keep track of last login, disable old accounts)

* Fri Oct  8 2010 Rich Megginson <rmeggins@redhat.com> - 1.2.7-0.1.a1
- added openldap support

* Wed Sep 29 2010 Rich Megginson <rmeggins@redhat.com> - 1.2.6.1-3
- bump rel to rebuild again

* Mon Sep 27 2010 Rich Megginson <rmeggins@redhat.com> - 1.2.6.1-2
- bump rel to rebuild

* Thu Sep 23 2010 Rich Megginson <rmeggins@redhat.com> - 1.2.6.1-1
- This is the 1.2.6.1 release - git tag 389-ds-base-1.2.6.1
- Bug 634561 - Server crushes when using Windows Sync Agreement
- Bug 635987 - Incorrect sub scope search result with ACL containing ldap:///self
- Bug 612264 - ACI issue with (targetattr='userPassword')
- Bug 606920 - anonymous resource limit- nstimelimit - also applied to "cn=directory manager"
- Bug 631862 - crash - delete entries not in cache + referint

* Thu Aug 26 2010 Rich Megginson <rmeggins@redhat.com> - 1.2.6-1
- This is the final 1.2.6 release

* Tue Aug 10 2010 Rich Megginson <rmeggins@redhat.com> - 1.2.6-0.11.rc7
- 1.2.6 release candidate 7
- git tag 389-ds-base-1.2.6.rc7
- Bug 621928 - Unable to enable replica (rdn problem?) on 1.2.6 rc6

* Mon Aug  2 2010 Rich Megginson <rmeggins@redhat.com> - 1.2.6-0.10.rc6
- 1.2.6 release candidate 6
- git tag 389-ds-base-1.2.6.rc6
- Bug 617013 - repl-monitor.pl use cpu upto 90%
- Bug 616618 - 389 v1.2.5 accepts 2 identical entries with different DN formats
- Bug 547503 - replication broken again, with 389 MMR replication and TCP errors
- Bug 613833 - Allow dirsrv_t to bind to rpc ports
- Bug 612242 - membership change on DS does not show on AD
- Bug 617629 - Missing aliases in new schema files
- Bug 619595 - Upgrading sub suffix under non-normalized suffix disappears
- Bug 616608 - SIGBUS in RDN index reads on platforms with strict alignments
- Bug 617862 - Replication: Unable to delete tombstone errors
- Bug 594745 - Get rid of dirsrv_lib_t label

* Wed Jul 14 2010 Rich Megginson <rmeggins@redhat.com> - 1.2.6-0.9.rc3
- make selinux-devel explicit Require the base package in order
- to comply with Fedora Licensing Guidelines

* Thu Jul  1 2010 Rich Megginson <rmeggins@redhat.com> - 1.2.6-0.8.rc3
- 1.2.6 release candidate 3
- git tag 389-ds-base-1.2.6.rc3
- Bug 603942 - null deref in _ger_parse_control() for subjectdn
- 609256  - Selinux: pwdhash fails if called via Admin Server CGI
- 578296  - Attribute type entrydn needs to be added when subtree rename switch is on
- 605827 - In-place upgrade: upgrade dn format should not run in setup-ds-admin.pl
- Bug 604453 - SASL Stress and Server crash: Program quits with the assertion failure in PR_Poll
- Bug 604453 - SASL Stress and Server crash: Program quits with the assertion failure in PR_Poll
- 606920 - anonymous resource limit - nstimelimit - also applied to "cn=directory manager"

* Wed Jun 16 2010 Rich Megginson <rmeggins@redhat.com> - 1.2.6-0.7.rc2
- 1.2.6 release candidate 2

* Mon Jun 14 2010 Nathan Kinder <nkinder@redhat.com> - 1.2.6-0.6.rc1
- install replication session plugin header with devel package

* Wed Jun  9 2010 Rich Megginson <rmeggins@redhat.com> - 1.2.6-0.5.rc1
- 1.2.6 release candidate 1

* Tue Jun 01 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.2.6-0.4.a4.1
- Mass rebuild with perl-5.12.0

* Wed May 26 2010 Rich Megginson <rmeggins@redhat.com> - 1.2.6-0.4.a4
- 1.2.6.a4 release

* Wed Apr  7 2010 Nathan Kinder <nkinder@redhat.com> - 1.2.6-0.4.a3
- 1.2.6.a3 release
- add managed entries plug-in
- many bug fixes
- moved selinux subpackage into base package

* Fri Apr  2 2010 Caolán McNamara <caolanm@redhat.com> - 1.2.6-0.3.a2
- rebuild for icu 4.4

* Tue Mar  2 2010 Rich Megginson <rmeggins@redhat.com> - 1.2.6-0.2.a2
- 1.2.6.a2 release
- add support for matching rules
- many bug fixes

* Thu Jan 14 2010 Nathan Kinder <nkinder@redhat.com> - 1.2.6-0.1.a1
- 1.2.6.a1 release
- Added SELinux policy and subpackages

* Tue Jan 12 2010 Rich Megginson <rmeggins@redhat.com> - 1.2.5-1
- 1.2.5 final release

* Mon Jan  4 2010 Rich Megginson <rmeggins@redhat.com> - 1.2.5-0.5.rc4
- 1.2.5.rc4 release

* Thu Dec 17 2009 Rich Megginson <rmeggins@redhat.com> - 1.2.5-0.4.rc3
- 1.2.5.rc3 release

* Mon Dec  7 2009 Rich Megginson <rmeggins@redhat.com> - 1.2.5-0.3.rc2
- 1.2.5.rc2 release

* Wed Dec  2 2009 Rich Megginson <rmeggins@redhat.com> - 1.2.5-0.2.rc1
- 1.2.5.rc1 release

* Thu Nov 12 2009 Rich Megginson <rmeggins@redhat.com> - 1.2.5-0.1.a1
- 1.2.5.a1 release

* Thu Oct 29 2009 Rich Megginson <rmeggins@redhat.com> - 1.2.4-1
- 1.2.4 release
- resolves bug 221905 - added support for Salted MD5 (SMD5) passwords - primarily for migration
- resolves bug 529258 - Make upgrade remove obsolete schema from 99user.ldif

* Mon Sep 14 2009 Rich Megginson <rmeggins@redhat.com> - 1.2.3-1
- 1.2.3 release
- added template-initconfig to %files
- %posttrans now runs update to update the server instances
- servers are shutdown, then restarted if running before install
- scriptlets mostly use lua now to pass data among scriptlet phases

* Tue Sep 01 2009 Caolán McNamara <caolanm@redhat.com> - 1.2.2-2
- rebuild with new openssl to fix dependencies

* Tue Aug 25 2009 Rich Megginson <rmeggins@redhat.com> - 1.2.2-1
- backed out - added template-initconfig to %files - this change is for the next major release
- bump version to 1.2.2
- fix reopened 509472 db2index all does not reindex all the db backends correctly
- fix 518520 -  pre hashed salted passwords do not work
- see https://bugzilla.redhat.com/show_bug.cgi?id=518519 for the list of
- bugs fixed in 1.2.2

* Fri Aug 21 2009 Tomas Mraz <tmraz@redhat.com> - 1.2.1-5
- rebuilt with new openssl

* Wed Aug 19 2009 Noriko Hosoi <nhosoi@redhat.com> - 1.2.1-4
- added template-initconfig to %files

* Wed Aug 12 2009 Rich Megginson <rmeggins@redhat.com> - 1.2.1-3
- added BuildRequires pcre

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon May 18 2009 Rich Megginson <rmeggins@redhat.com> - 1.2.1-1
- change name to 389
- change version to 1.2.1
- added initial support for numeric string syntax
- added initial support for syntax validation
- added initial support for paged results including sorting

* Tue Apr 28 2009 Rich Megginson <rmeggins@redhat.com> - 1.2.0-4
- final release 1.2.0
- Resolves: bug 475338 - LOG: the intenal type of maxlogsize, maxdiskspace and minfreespace should be 64-bit integer
- Resolves: bug 496836 - SNMP ldap-agent on Solaris: Unable to open semaphore for server: 389
- CVS tag: FedoraDirSvr_1_2_0 FedoraDirSvr_1_2_0_20090428

* Mon Apr  6 2009 Rich Megginson <rmeggins@redhat.com> - 1.2.0-3
- re-enable ppc builds

* Thu Apr  2 2009 Rich Megginson <rmeggins@redhat.com> - 1.2.0-2
- exclude ppc builds - needs extensive porting work

* Mon Mar 30 2009 Rich Megginson <rmeggins@redhat.com> - 1.2.0-1
- new release 1.2.0
- Made devel package depend on mozldap-devel
- only create run dir if it does not exist
- CVS tag: FedoraDirSvr_1_2_0_RC1 FedoraDirSvr_1_2_0_RC1_20090330

* Thu Oct 30 2008 Noriko Hosoi <nhosoi@redhat.com> - 1.1.3-7
- added db4-utils to Requires for verify-db.pl

* Mon Oct 13 2008 Noriko Hosoi <nhosoi@redhat.com> - 1.1.3-6
- Enabled LDAPI autobind

* Thu Oct  9 2008 Rich Megginson <rmeggins@redhat.com> - 1.1.3-5
- updated update to patch bug463991-bdb47.patch

* Thu Oct  9 2008 Rich Megginson <rmeggins@redhat.com> - 1.1.3-4
- updated patch bug463991-bdb47.patch

* Mon Sep 29 2008 Rich Megginson <rmeggins@redhat.com> - 1.1.3-3
- added patch bug463991-bdb47.patch
- make ds work with bdb 4.7

* Wed Sep 24 2008 Rich Megginson <rmeggins@redhat.com> - 1.1.3-2
- rolled back bogus winsync memory leak fix

* Tue Sep 23 2008 Rich Megginson <rmeggins@redhat.com> - 1.1.3-1
- winsync api improvements for modify operations

* Fri Jun 13 2008 Rich Megginson <rmeggins@redhat.com> - 1.1.2-1
- This is the 1.1.2 release.  The bugs fixed can be found here
- https://bugzilla.redhat.com/showdependencytree.cgi?id=452721
- Added winsync-plugin.h to the devel subpackage

* Fri Jun  6 2008 Rich Megginson <rmeggins@redhat.com> - 1.1.1-2
- bump rev to rebuild and pick up new version of ICU

* Fri May 23 2008 Rich Megginson <rmeggins@redhat.com> - 1.1.1-1
- 1.1.1 release candidate - several bug fixes

* Wed Apr 16 2008 Rich Megginson <rmeggins@redhat.com> - 1.1.0.1-4
- fix bugzilla 439829 - patch to allow working with NSS 3.11.99 and later

* Tue Mar 18 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.1.0.1-3
- add patch to allow server to work with NSS 3.11.99 and later
- do NSS_Init after fork but before detaching from console

* Tue Mar 18 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.1.0.1-3
- add Requires for versioned perl (libperl.so)

* Wed Feb 27 2008 Rich Megginson <rmeggins@redhat.com> - 1.1.0.1-2
- previous fix for 434403 used the wrong patch
- this is the right one

* Wed Feb 27 2008 Rich Megginson <rmeggins@redhat.com> - 1.1.0.1-1
- Resolves bug 434403 - GCC 4.3 build fails
- Rolled new source tarball which includes Nathan's fix for the struct ucred
- NOTE: Change version back to 1.1.1 for next release
- this release was pulled from CVS tag FedoraDirSvr110_gcc43

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.1.0-5
- Autorebuild for GCC 4.3

* Thu Dec 20 2007 Rich Megginson <rmeggins@redhat.com> - 1.1.0-4
- This is the GA release of Fedora DS 1.1
- Removed version numbers for BuildRequires and Requires
- Added full URL to source tarball

* Fri Dec 07 2007 Release Engineering <rel-eng at fedoraproject dot org> - 1.1.0-3
- Rebuild for deps

* Wed Nov  7 2007 Rich Megginson <rmeggins@redhat.com> - 1.1.0-2.0
- This is the beta2 release
- new file added to package - /etc/sysconfig/dirsrv - for setting
- daemon environment as is usual in other linux daemons

* Thu Aug 16 2007 Rich Megginson <rmeggins@redhat.com> - 1.1.0-1.2
- fix build breakage due to open()
- mock could not find BuildRequires: db4-devel >= 4.2.52
- mock works if >= version is removed - it correctly finds db4.6

* Fri Aug 10 2007 Rich Megginson <rmeggins@redhat.com> - 1.1.0-1.1
- Change pathnames to use the pkgname macro which is dirsrv
- get rid of cvsdate in source name

* Fri Jul 20 2007 Rich Megginson <rmeggins@redhat.com> - 1.1.0-0.3.20070720
- Added Requires for perldap, cyrus sasl plugins
- Removed template-migrate* files
- Added perl module directory
- Removed install.inf - setup-ds.pl can now easily generate one

* Mon Jun 18 2007 Nathan Kinder <nkinder@redhat.com> - 1.1.0-0.2.20070320
- added requires for mozldap-tools

* Tue Mar 20 2007 Rich Megginson <rmeggins@redhat.com> - 1.1.0-0.1.20070320
- update to latest sources
- added migrateTo11 to allow migrating instances from 1.0.x to 1.1
- ldapi support
- fixed pam passthru plugin ENTRY method

* Fri Feb 23 2007 Rich Megginson <rmeggins@redhat.com> - 1.1.0-0.1.20070223
- Renamed package to fedora-ds-base, but keep names of paths/files/services the same
- use the shortname macro (fedora-ds) for names of paths, files, and services instead
- of name, so that way we can continue to use e.g. /etc/fedora-ds instead of /etc/fedora-ds-base
- updated to latest sources

* Tue Feb 13 2007 Rich Megginson <rmeggins@redhat.com> - 1.1.0-0.1.20070213
- More cleanup suggested by Dennis Gilmore
- This is the fedora extras candidate based on cvs tag FedoraDirSvr110a1

* Fri Feb  9 2007 Rich Megginson <rmeggins@redhat.com> - 1.1.0-1.el4.20070209
- latest sources
- added init scripts
- use /etc as instconfigdir

* Wed Feb  7 2007 Rich Megginson <rmeggins@redhat.com> - 1.1.0-1.el4.20070207
- latest sources
- moved all executables to _bindir

* Mon Jan 29 2007 Rich Megginson <rmeggins@redhat.com> - 1.1.0-1.el4.20070129
- latest sources
- added /var/tmp/fedora-ds to dirs

* Fri Jan 26 2007 Rich Megginson <rmeggins@redhat.com> - 1.1.0-8.el4.20070125
- added logconv.pl
- added slapi-plugin.h to devel package
- added explicit dirs for /var/log/fedora-ds et. al.

* Thu Jan 25 2007 Rich Megginson <rmeggins@redhat.com> - 1.1.0-7.el4.20070125
- just move all .so files into the base package from the devel package

* Thu Jan 25 2007 Rich Megginson <rmeggins@redhat.com> - 1.1.0-6.el4.20070125
- Move the plugin *.so files into the main package instead of the devel
- package because they are loaded directly by name via dlopen

* Fri Jan 19 2007 Rich Megginson <rmeggins@redhat.com> - 1.1.0-5.el4.20070125
- Move the script-templates directory to datadir/fedora-ds

* Fri Jan 19 2007 Rich Megginson <rmeggins@redhat.com> - 1.1.0-4.el4.20070119
- change mozldap to mozldap6

* Fri Jan 19 2007 Rich Megginson <rmeggins@redhat.com> - 1.1.0-3.el4.20070119
- remove . from cvsdate define

* Fri Jan 19 2007 Rich Megginson <rmeggins@redhat.com> - 1.1.0-2.el4.20070119
- Having a problem building in Brew - may be Release format

* Fri Jan 19 2007 Rich Megginson <rmeggins@redhat.com> - 1.1.0-1.el4.cvs20070119
- Changed version to 1.1.0 and added Release 1.el4.cvs20070119
- merged in changes from Fedora Extras candidate spec file

* Mon Jan 15 2007 Rich Megginson <rmeggins@redhat.com> - 1.1-0.1.cvs20070115
- Bump component versions (nspr, nss, svrcore, mozldap) to their latest
- remove unneeded patches

* Tue Jan 09 2007 Dennis Gilmore <dennis@ausil.us> - 1.1-0.1.cvs20070108
- update to a cvs snapshot
- fedorafy the spec 
- create -devel subpackage
- apply a patch to use mozldap not mozldap6
- apply a patch to allow --prefix to work correctly

* Mon Dec 4 2006 Rich Megginson <rmeggins@redhat.com> - 1.0.99-16
- Fixed the problem where the server would crash upon shutdown in dblayer
- due to a race condition among the database housekeeping threads
- Fix a problem with normalized absolute paths for db directories

* Tue Nov 28 2006 Rich Megginson <rmeggins@redhat.com> - 1.0.99-15
- Touch all of the ldap/admin/src/scripts/*.in files so that they
- will be newer than their corresponding script template files, so
- that make will rebuild them.

* Mon Nov 27 2006 Rich Megginson <rmeggins@redhat.com> - 1.0.99-14
- Chown new schema files when copying during instance creation

* Tue Nov 21 2006 Rich Megginson <rmeggins@redhat.com> - 1.0.99-13
- Configure will get ldapsdk_bindir from pkg-config, or $libdir/mozldap6

* Tue Nov 21 2006 Rich Megginson <rmeggins@redhat.com> - 1.0.99-12
- use eval to sed ./configure into ../configure

* Tue Nov 21 2006 Rich Megginson <rmeggins@redhat.com> - 1.0.99-11
- jump through hoops to be able to run ../configure

* Tue Nov 21 2006 Rich Megginson <rmeggins@redhat.com> - 1.0.99-10
- Need to make built dir in setup section

* Tue Nov 21 2006 Rich Megginson <rmeggins@redhat.com> - 1.0.99-9
- The template scripts needed to use @libdir@ instead of hardcoding
- /usr/lib
- Use make DESTDIR=$RPM_BUILD_ROOT install instead of % makeinstall
- do the actual build in a "built" subdirectory, until we remove
- the old script templates

* Thu Nov 16 2006 Rich Megginson <rmeggins@redhat.com> - 1.0.99-8
- Make replication plugin link with libdb

* Wed Nov 15 2006 Rich Megginson <rmeggins@redhat.com> - 1.0.99-7
- Have make define LIBDIR, BINDIR, etc. for C code to use
- especially for create_instance.h

* Tue Nov 14 2006 Rich Megginson <rmeggins@redhat.com> - 1.0.99-6
- Forgot to checkin new config.h.in for AC_CONFIG_HEADERS

* Tue Nov 14 2006 Rich Megginson <rmeggins@redhat.com> - 1.0.99-5
- Add perldap as a Requires; update sources

* Thu Nov 9 2006 Rich Megginson <rmeggins@redhat.com> - 1.0.99-4
- Fix ds_newinst.pl
- Remove obsolete #defines

* Thu Nov 9 2006 Rich Megginson <rmeggins@redhat.com> - 1.0.99-3
- Update sources; rebuild to populate brew yum repo with dirsec-nss

* Tue Nov 7 2006 Rich Megginson <rmeggins@redhat.com> - 1.0.99-2
- Update sources

* Thu Nov 2 2006 Rich Megginson <rmeggins@redhat.com> - 1.0.99-1
- initial revision

