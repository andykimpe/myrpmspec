%{!?python_sitelib: %define python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}

%define packagename prioritized_methods

Name:           python-prioritized-methods
Version:        0.2.1
Release:        5.2%{?dist}
Summary:        An extension to PEAK-Rules to prioritize methods in order

Group:          Development/Languages
License:        MIT
URL:            http://pypi.python.org/pypi/prioritized_methods
Source0:        http://pypi.python.org/packages/source/p/%{packagename}/%{packagename}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch

BuildRequires:  python-devel
BuildRequires:  python-setuptools-devel

# following for UpdateTimestamps sanitization function
BuildRequires:  diffstat

Requires:       python-peak-rules

Patch0:         bz1321133-prioritized_methods-fix-requires.patch


%description
This module provides four decorators: `prioritized_when`, `prioritized_around`,
`prioritized_before`, and `prioritized_after`.  These behave like their
`peak.rules` counterparts except that they accept an optional `prio`
argument which can be used to provide a comparable object (usually an integer)
that will be used to disambiguate situations in which more than rule applies to
the given arguments and no rule is more specific than another. That is,
situations in which an `peak.rules.AmbiguousMethods` would have been raised.

This is useful for libraries which want to be extensible via generic functions
but want their users to easily override a method without figuring out how to
write a more specific rule or when it is not feasible.


%prep
%setup -q -n %{packagename}-%{version}

# -- following borrowed from python-simplejon.el5 --
# Update timestamps on the files touched by a patch, to avoid non-equal
# .pyc/.pyo files across the multilib peers within a build, where "Level"
# is the patch prefix option (e.g. -p1)
UpdateTimestamps() {
  Level=$1
  PatchFile=$2
  # Locate the affected files:
  for f in $(diffstat $Level -l $PatchFile); do
    # Set the files to have the same timestamp as that of the patch:
    touch -r $PatchFile $f
  done
}
%patch0 -p1
UpdateTimestamps -p1 %{PATCH0}

%build
%{__python} setup.py build

%install
rm -rf %{buildroot}
%{__python} setup.py install --skip-build --root %{buildroot}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{python_sitelib}/*

%changelog
* Thu Mar 24 2016 Jan Pokorny <jpokorny@redhat.com> - 0.2.1-5.2
- Fix install_requires contains forward-incompatible
  "PEAK-Rules>=0.5a1.dev-r2562,==dev" specification
Resolves: rhbz#1321133

* Mon Nov 30 2009 Dennis Gregorovic <dgregor@redhat.com> - 0.2.1-5.1
- Rebuilt for RHEL 6

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 0.2.1-3
- Rebuild for Python 2.6

* Wed Oct 15 2008 Luke Macken <lmacken@redhat.com> - 0.2.1-2
- Fix our python-peak-rules dependency

* Tue Sep 16 2008 Luke Macken <lmacken@redhat.com> - 0.2.1-1
- Initial package for Fedora
