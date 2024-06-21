Name:           hivex
Version:        1.3.3
Release:        4.3%{?dist}
Summary:        Read and write Windows Registry binary hive files

Group:          Development/Libraries
License:        LGPLv2
URL:            http://libguestfs.org/
Source0:        http://libguestfs.org/download/hivex/%{name}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

# Doesn't build on s390 because of lack of OCaml.  Actually, OCaml
# would work perfectly well on s390 is we fixed a minor build problem
# there.  Or we could disable to OCaml hivex bindings on s390.
ExcludeArch:    s390 s390x

BuildRequires:  perl
BuildRequires:  perl-Test-Simple
BuildRequires:  perl-Test-Pod
BuildRequires:  perl-Test-Pod-Coverage
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl-IO-stringy
BuildRequires:  perl-libintl
BuildRequires:  ocaml
BuildRequires:  ocaml-findlib-devel
BuildRequires:  python-devel
#BuildRequires:  ruby-devel
#BuildRequires:  rubygem-rake
BuildRequires:  readline-devel
BuildRequires:  libxml2-devel

# This library used to be part of libguestfs.  It won't install alongside
# the old version of libguestfs that included this library:
Conflicts:      libguestfs <= 1:1.0.84

# Fix Perl directory install path.
Patch0:         %{name}-1.2.3-dirs.patch

# Upstream patches.
Patch1:         0001-hivexml-Remove-unused-variable.patch
Patch2:         0001-hivex-Added-gnulib-includes-from-builddir-as-suggest.patch
Patch3:         0001-hivex-Added-gnulib-includes-from-builddir-as-suggest-AUTOMAKE.patch
Patch4:         0001-patch-for-read-support-of-li-records-from-ri-interme.patch
Patch5:         hivex-1.3.3-missing-checks-for-small-truncated-files.patch
Patch6:         hivex-1.3.3-fix-typos-rhbz1164693.patch


%description
Hive files are undocumented binary files that Windows uses to store
the Windows Registry on the disk.  Hivex is a library that can read
and write to these files.

'hivexsh' is a shell you can use to interactively navigate a hive
binary file.

'hivexregedit' lets you export and merge to the textual regedit
format.

'hivexml' can be used to convert a hive file to a more useful XML
format.

In order to get access to the hive files themselves, you can copy them
from a Windows machine.  They are usually found in
%%systemroot%%\system32\config.  For virtual machines we recommend
using libguestfs or guestfish to copy out these files.  libguestfs
also provides a useful high-level tool called 'virt-win-reg' (based on
hivex technology) which can be used to query specific registry keys in
an existing Windows VM.

For OCaml bindings, see 'ocaml-hivex-devel'.

For Perl bindings, see 'perl-hivex'.

For Python bindings, see 'python-hivex'.


%package devel
Summary:        Development tools and libraries for %{name}
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}
Requires:       pkgconfig


%description devel
%{name}-devel contains development tools and libraries
for %{name}.


%package -n ocaml-%{name}
Summary:       OCaml bindings for %{name}
Group:         Development/Libraries
Requires:      %{name} = %{version}-%{release}


%description -n ocaml-%{name}
ocaml-%{name} contains OCaml bindings for %{name}.

This is for toplevel and scripting access only.  To compile OCaml
programs which use %{name} you will also need ocaml-%{name}-devel.


%package -n ocaml-%{name}-devel
Summary:       OCaml bindings for %{name}
Group:         Development/Libraries
Requires:      ocaml-%{name} = %{version}-%{release}


%description -n ocaml-%{name}-devel
ocaml-%{name}-devel contains development libraries
required to use the OCaml bindings for %{name}.


%package -n perl-%{name}
Summary:       Perl bindings for %{name}
Group:         Development/Libraries
Requires:      %{name} = %{version}-%{release}
Requires:      perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))


%description -n perl-%{name}
perl-%{name} contains Perl bindings for %{name}.


%package -n python-%{name}
Summary:       Python bindings for %{name}
Group:         Development/Libraries
Requires:      %{name} = %{version}-%{release}

%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}
%{!?python_sitearch: %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}

%description -n python-%{name}
python-%{name} contains Python bindings for %{name}.


%prep
%setup -q

%patch0 -p1 -b .dirs
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1


%build
%configure --disable-static
make %{?_smp_mflags}


%check
make check


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

# Remove unwanted libtool *.la file:
rm $RPM_BUILD_ROOT%{_libdir}/libhivex.la

# Remove unwanted Perl files:
find $RPM_BUILD_ROOT -name perllocal.pod -delete
find $RPM_BUILD_ROOT -name .packlist -delete
find $RPM_BUILD_ROOT -name '*.bs' -delete

# Remove unwanted Python files:
rm $RPM_BUILD_ROOT%{python_sitearch}/libhivexmod.la

# configure can't --disable-ruby, so remove Ruby files instead.
find $RPM_BUILD_ROOT -name 'ruby' -a -type d | xargs rm -rf

%find_lang %{name}


%clean
rm -rf $RPM_BUILD_ROOT


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files -f %{name}.lang
%defattr(-,root,root,-)
%doc README LICENSE
%{_bindir}/hivexget
%{_bindir}/hivexml
%{_bindir}/hivexregedit
%{_bindir}/hivexsh
%{_libdir}/libhivex.so.*
%{_mandir}/man1/hivexget.1*
%{_mandir}/man1/hivexml.1*
%{_mandir}/man1/hivexregedit.1*
%{_mandir}/man1/hivexsh.1*


%files devel
%defattr(-,root,root,-)
%doc LICENSE
%{_libdir}/libhivex.so
%{_mandir}/man3/hivex.3*
%{_includedir}/hivex.h
%{_libdir}/pkgconfig/hivex.pc


%files -n ocaml-%{name}
%defattr(-,root,root,-)
%doc README
%{_libdir}/ocaml/hivex
%exclude %{_libdir}/ocaml/hivex/*.a
%exclude %{_libdir}/ocaml/hivex/*.cmxa
%exclude %{_libdir}/ocaml/hivex/*.cmx
%exclude %{_libdir}/ocaml/hivex/*.mli
%{_libdir}/ocaml/stublibs/*.so
%{_libdir}/ocaml/stublibs/*.so.owner


%files -n ocaml-%{name}-devel
%defattr(-,root,root,-)
%{_libdir}/ocaml/hivex/*.a
%{_libdir}/ocaml/hivex/*.cmxa
%{_libdir}/ocaml/hivex/*.cmx
%{_libdir}/ocaml/hivex/*.mli


%files -n perl-%{name}
%defattr(-,root,root,-)
%{perl_vendorarch}/*
%{_mandir}/man3/Win::Hivex.3pm*
%{_mandir}/man3/Win::Hivex::Regedit.3pm*


%files -n python-%{name}
%defattr(-,root,root,-)
%{python_sitearch}/*.py
%{python_sitearch}/*.pyc
%{python_sitearch}/*.pyo
%{python_sitearch}/*.so


%changelog
* Fri Feb 27 2015 Richard W.M. Jones <rjones@redhat.com> - 1.3.3-4.3
- Add missing checks for small/truncated files
  resolves: rhbz#1158993
- Fix typo in man page Win::Hivex.3.pm
  resolves: rhbz#1164693

* Thu Oct 11 2012 Richard W.M. Jones <rjones@redhat.com> - 1.3.3-4.2
- Remove loaded text from description
  resolves: rhbz#822741
- Add patch to fix parsing of hives that contain large ri-records
  resolves: rhbz#841924

* Tue Dec 20 2011 Richard W.M. Jones <rjones@redhat.com> - 1.3.3-4
- Rebase to upstream version 1.3.3
  resolves: rhbz#734208
- Add upstream patch: hivexml: Remove unused variable.
- Add upstream patch: hivex: Added gnulib includes from builddir [...]

* Fri Jan 14 2011 Richard W.M. Jones <rjones@redhat.com> - 1.2.4-3
- Fix multilib conflicts in *.pyc and *.pyo files.
- Only install unversioned *.so file for Python bindings.

* Thu Dec  2 2010 Richard W.M. Jones <rjones@redhat.com> - 1.2.4-2
- Rebase to upstream version 1.2.4 (RHBZ#642631).
  * Python bindings (python-hivex subpackage).
  * Adds hivex_set_value API call (Conrad Meyer).
  * Miscellaneous small bug fixes.
- Fix Source0.
- Fix builds with recent perl (Dan Horák).

* Wed Apr 28 2010 Richard W.M. Jones <rjones@redhat.com> - 1.2.2-1
- Rebase to version 1.2.2 which contains an important fix for
  regedit importing (for V2V).

* Thu Apr  1 2010 Richard W.M. Jones <rjones@redhat.com> - 1.2.1-1
- Backport hivex package from Fedora Rawhide.
- Exclude s390, s390x because of lack of OCaml packages.

* Tue Mar 30 2010 Richard W.M. Jones <rjones@redhat.com> - 1.2.1-1
- New upstream version 1.2.1.
- Includes new tool for exporting and merging in regedit format.

* Mon Mar  1 2010 Richard W.M. Jones <rjones@redhat.com> - 1.2.0-2
- New upstream version 1.2.0.
- This includes OCaml and Perl bindings, so add these as subpackages.

* Mon Feb 22 2010 Richard W.M. Jones <rjones@redhat.com> - 1.1.2-3
- Missing Epoch in conflicts version fixed.

* Mon Feb 22 2010 Richard W.M. Jones <rjones@redhat.com> - 1.1.2-2
- Add Conflicts libguestfs <= 1.0.84.

* Mon Feb 22 2010 Richard W.M. Jones <rjones@redhat.com> - 1.1.2-1
- Initial Fedora RPM.