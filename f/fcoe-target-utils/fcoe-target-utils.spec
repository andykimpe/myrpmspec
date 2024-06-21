%global oname targetcli-fb

Name:           fcoe-target-utils
License:        AGPLv3
Group:          System Environment/Libraries
Summary:        An administration shell for FCoE storage targets
Version:        2.0rc1.fb16
Release:        6%{?dist}
URL:            https://github.com/agrover/targetcli-fb
Source:         https://github.com/downloads/agrover/%{oname}/%{oname}-%{version}.tar.gz
Source1:        fcoe-target.init
Patch0:         0001-suggest-driverload.patch
Patch1:         0002-man-ignore-iscsi.patch
Patch2:         0003-no-rdmcp.patch
Patch3:         0004-no-msg-if-no-config.patch
Patch4:         0005-check-if-tpglun-exists.patch
Patch5:         0006-Add-tag-support.patch
Patch6:         0007-Simplify-tag.patch
Patch7:         0008-Fix-UINodeACL-creation.patch
Patch8:         0009-Add-error-checking-for-tag.patch
Patch9:         0010-Update-tag-doctext.patch
Patch10:        0011-Fix-re-tagging.patch
Patch11:        0012-Fix-missed-spot-in-tags-conversion.patch
Patch12:        0013-fix-missing-import.patch
Patch13:        0014-Remove-execute_command-in-UIRTSLibNode.patch
Patch14:        0015-Make-info-command-return-dump-information.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
ExcludeArch:    ppc s390 s390x
BuildRequires:  python-devel python-configshell epydoc
BuildRequires:  python-rtslib >= 2.1.fb21
Requires:       python-rtslib >= 2.1.fb21, python-configshell fcoe-utils
Requires(post): chkconfig
Requires(preun): chkconfig


%description
An administration shell for TCM/LIO storage targets, most notably
Fiber Channel over Ethernet (FCoE) targets.


%prep
%setup -q -n %{oname}-%{version}
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1
%patch9 -p1
%patch10 -p1
%patch11 -p1
%patch12 -p1
%patch13 -p1
%patch14 -p1

%build
%{__python} setup.py build
gzip --stdout targetcli.8 > targetcli.8.gz

%install
rm -rf %{buildroot}
%{__python} setup.py install --skip-build --root %{buildroot}
mkdir -p %{buildroot}%{_sysconfdir}/rc.d/init.d
mkdir -p %{buildroot}%{_sysconfdir}/target/backup
mkdir -p %{buildroot}%{_mandir}/man8/
install -m 755 %{SOURCE1} %{buildroot}%{_sysconfdir}/rc.d/init.d/fcoe-target
install -m 755 targetcli.8.gz %{buildroot}%{_mandir}/man8/

%clean
rm -rf %{buildroot}

%post
/sbin/chkconfig --add fcoe-target

%preun
if [ "$1" = 0 ]; then
        /sbin/chkconfig --del fcoe-target
fi


%files
%defattr(-,root,root,-)
%{python_sitelib}
%{_bindir}/targetcli
%attr(0755,root,root) %{_sysconfdir}/rc.d/init.d/fcoe-target
%dir %{_sysconfdir}/target/backup
%doc COPYING README
%{_mandir}/man8/targetcli.8.gz

%changelog
* Mon Jan 18 2016 Andy Grover <agrover@redhat.com> - 2.0rc1.fb16-6
- Add patches:
    0006-Add-tag-support.patch
    0007-Simplify-tag.patch
    0008-Fix-UINodeACL-creation.patch
    0009-Add-error-checking-for-tag.patch
    0010-Update-tag-doctext.patch
    0011-Fix-re-tagging.patch
    0012-Fix-missed-spot-in-tags-conversion.patch
    0013-fix-missing-import.patch
    0014-Remove-execute_command-in-UIRTSLibNode.patch
    0015-Make-info-command-return-dump-information.patch
- Rename existing patches to match new patch names

* Tue Aug 22 2013 Andy Grover <agrover@redhat.com> - 2.0rc1.fb16-5
- exclude ppc s390 and s390x arches to fix compose

* Tue Jul 2 2013 Andy Grover <agrover@redhat.com> - 2.0rc1.fb16-4
- Update patch suggest-driverload.patch

* Fri Dec 7 2012 Andy Grover <agrover@redhat.com> - 2.0rc1.fb16-3
- Add patch:
 * fcoe-target-utils-check-if-tpglun-exists.patch

* Wed Aug 8 2012 Andy Grover <agrover@redhat.com> - 2.0rc1.fb16-2
- Update rtslib version Requires to fb21

* Tue Aug 7 2012 Andy Grover <agrover@redhat.com> - 2.0rc1.fb16-1
- Update to latest upstream version
- Remove patches:
 * fcoe-target-utils-handle-no-acl-auth.patch
 * fcoe-target-utils-message-deprecated.patch

* Tue May 8 2012 Andy Grover <agrover@redhat.com> - 2.0rc1.fb10-5
- Update fcoe-target.init to handle start and shutdown properly
- Add patch fcoe-target-utils-no-msg-if-no-config.patch

* Thu Apr 19 2012 Andy Grover <agrover@redhat.com> - 2.0rc1.fb10-4
- Add patches:
 * fcoe-target-utils-handle-no-acl-auth.patch
 * fcoe-target-utils-no-rdmcp.patch
 * fcoe-target-utils-message-deprecated.patch

* Tue Mar 6 2012 Andy Grover <agrover@redhat.com> - 2.0rc1.fb10-3
- Update description text

* Tue Mar 6 2012 Andy Grover <agrover@redhat.com> - 2.0rc1.fb10-2
- Update to latest upstream release
- Add patch fcoe-target-utils-man-ignore-iscsi.patch

* Fri Feb 17 2012 Andy Grover <agrover@redhat.com> - 2.0rc1.fb8-2
- Add patch fcoe-target-utils-suggest-driverload.patch for #752699

* Thu Feb 16 2012 Andy Grover <agrover@redhat.com> - 2.0rc1.fb8-1
- Update to latest upstream release
- Remove all patches
- Executable renamed targetadmin->targetcli to match upstream

* Thu Aug 25 2011 Andy Grover <agrover@redhat.com> - 1.99.1.git37f175c-6
* Modify 0009-add-docs.patch to improve targetadmin man page readability

* Thu Aug 25 2011 Andy Grover <agrover@redhat.com> - 1.99.1.git37f175c-5
- Fix saveconfig by creating /etc/target/backup
- Add targetadmin manpage
- Add patches
 * 0008-fix-spec_root-path.patch
 * 0009-add-docs.patch

* Thu Aug 18 2011 Andy Grover <agrover@redhat.com> - 1.99.1.git37f175c-4
- Update based on reviewer comments
  - Remove commented-out todo
  - Document full archive-building process
  - Remove license txt from spec file
  - Add chkconfig line to init file
  - Fix changelog versions (1.9.9.1 -> 1.99.1)
  - Remove epydoc runtime dependency
  - Remove "." from summary
  - Remove shebang from imported *.py files

* Tue Aug 2 2011 Andy Grover <agrover@redhat.com> - 1.99.1.git37f175c-3
- Rename rtsadmin.spec to fcoe-target-utils.spec

* Mon Aug 1 2011 Andy Grover <agrover@redhat.com> - 1.99.1.git37f175c-2
- Add init script
- Add copyright to .spec
- Add Requires: fcoe-utils
- Add patches
 * 0006-Hack.-dump-scripts-aren-t-in-PATH-anymore-so-call-th.patch
 * 0007-ignore-errors-from-failure-to-set-device-attributes.patch

* Thu Jul 28 2011 Andy Grover <agrover@redhat.com> - 1.99.1.git37f175c-1
- Rebase to latest git
- Rename package to fcoe-target-utils
- Rename executable to targetadmin
- Add patches
 * 0001-rename-rtsadmin-to-targetadmin.patch
 * 0002-Remove-ads-from-cli-welcome-msg.-Add-mention-of-man-.patch
 * 0003-change-config-dir-from-.rtsadmin-to-.targetadmin.patch
 * 0004-bundle-lio-utils.patch
 * 0005-fixup-setup.py.patch

* Tue May 10 2011 Andy Grover <agrover@redhat.com> - 1.99-1
- Initial packaging
