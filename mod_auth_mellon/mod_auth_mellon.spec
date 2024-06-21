%{!?_httpd_confdir:    %{expand: %%global _httpd_confdir %%{_sysconfdir}/httpd/conf.d}}
%{!?_httpd_modconfdir: %{expand: %%global _httpd_modconfdir %%{_sysconfdir}/httpd/conf.d}}
%{!?_httpd_moddir:     %{expand: %%global _httpd_moddir %%{_libdir}/httpd/modules}}
Summary: A SAML 2.0 authentication module for the Apache Httpd Server
Name: mod_auth_mellon
Version: 0.8.0
Release: 4%{?dist}
Group: System Environment/Daemons
Source0: https://github.com/UNINETT/mod_auth_mellon/releases/download/v0.8.0/%{name}-%{version}.tar.gz
Source1: auth_mellon.conf
Source2: 10-auth_mellon.conf
Source4: mellon_create_metadata.sh
License: GPLv2+
BuildRequires: curl-devel, glib2-devel, httpd-devel, lasso-devel, openssl-devel, xmlsec1-devel
Requires: httpd-mmn = %(cat %{_includedir}/httpd/.mmn || echo missing)
Requires: lasso >= 2.4.0
Url: https://github.com/UNINETT/mod_auth_mellon

Patch01: 0001-Add-support-for-AssertionConsumerServiceURL.patch
Patch02: multi-CVE-0.8.0.patch
Patch03: 0001-Define-envirnment-size-spacious-enough-to-hold-large.patch
Patch04: 0002-Adding-MellonMergeEnvVars-optional-functionality.patch
Patch05: 0003-am_check_permissions-env.-variable-mapping-fix.patch

%description
The mod_auth_mellon module is an authentication service that implements the
SAML 2.0 federation protocol. It grants access based on the attributes
received in assertions generated by a IdP server.

%prep
%setup -q -n %{name}-%{version}
%patch01 -p1
%patch02 -p1
%patch03 -p1
%patch04 -p1
%patch05 -p1

%build
export APXS=%{_httpd_apxs}
%configure
make %{?_smp_mflags}

%install
# install module
mkdir -p %{buildroot}%{_httpd_moddir}
install -m 755 .libs/%{name}.so %{buildroot}%{_httpd_moddir}

# install module configuration
mkdir -p %{buildroot}%{_httpd_confdir}
install -m 644 %{SOURCE1} %{buildroot}%{_httpd_confdir}
mkdir -p %{buildroot}%{_httpd_modconfdir}
install -m 644 %{SOURCE2} %{buildroot}%{_httpd_modconfdir}

mkdir -p %{buildroot}/var/run/%{name}

# install script to generate metadata
mkdir -p %{buildroot}/%{_libexecdir}/%{name}
install -m 755 %{SOURCE4} %{buildroot}/%{_libexecdir}/%{name}

%files
%defattr(-,root,root)
%doc README COPYING
%config(noreplace) %{_httpd_modconfdir}/10-auth_mellon.conf
%config(noreplace) %{_httpd_confdir}/auth_mellon.conf
%{_httpd_moddir}/mod_auth_mellon.so
%{_libexecdir}/%{name}
%dir /var/run/%{name}/

%changelog
* Mon Dec  8 2014 Simo Sorce <simo@redhat.com> 0.8.0-4
- Large scale intreop patches
- Resolves: #1167796

* Tue Oct 28 2014 Simo Sorce <simo@redhat.com> 0.8.0-3
- CVE-2014-8566 CVE-2014-8567
- Resolves: bz1157284
- Resolves: bz1157957

* Wed Aug 20 2014 Simo Sorce <simo@redhat.com> 0.8.0-2
- Fix interop issue with PicketLink
- Resolves: bz1130604

* Tue Jun 24 2014 Simo Sorce <simo@redhat.com> 0.8.0-1
- New upstream realease version 0.8.0
- Upstream moved to github
- Drops patches as they have been all included upstream

* Fri Jun 20 2014 Simo Sorce <simo@redhat.com> 0.7.0-4
- Backport of useful patches from upstream
  - Better handling of IDP reported errors
  - Better handling of session data storage size

* Wed Jun 11 2014 Simo Sorce <simo@redhat.com> 0.7.0-3
Fix httpd-mmn require to work on RHEL6

* Fri May 23 2014 Simo Sorce <simo@redhat.com> 0.7.0-2
Fix paths and variables to work on RHEL6

* Thu Apr 24 2014 Simo Sorce <simo@redhat.com> 0.7.0-1
Initial RHEL 6 import