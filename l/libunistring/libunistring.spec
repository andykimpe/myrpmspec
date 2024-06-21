Name: libunistring
Version: 0.9.3
Release: 5%{?dist}
Group: System Environment/Libraries
Summary: GNU Unicode string library
License: LGPLv3+
Url: http://www.gnu.org/software/libunistring/
Source0: http://ftp.gnu.org/gnu/libunistring/%{name}-%{version}.tar.gz
BuildRoot: %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
Requires(post): info
Requires(preun): info

# Patches
Patch0001: 0001-Add-NULL-check-for-malloc-in-two-uninorm-files.patch

%description
This portable C library implements Unicode string types in three flavours:
(UTF-8, UTF-16, UTF-32), together with functions for character processing
(names, classifications, properties) and functions for string processing
(iteration, formatted output, width, word breaks, line breaks, normalization,
case folding and regular expressions).

%package devel
Group: Development/Libraries
Summary: GNU Unicode string library - development files
Requires: %{name} = %{version}-%{release}

%description devel
Development files for programs using libunistring.

%prep
%setup -q

%patch0001 -p1

%build
%configure --disable-static --disable-rpath
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p"
rm -f $RPM_BUILD_ROOT/%{_infodir}/dir
rm -f $RPM_BUILD_ROOT/%{_libdir}/%{name}.la

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc AUTHORS NEWS README
%{_libdir}/%{name}.so.*

%files devel
%defattr(-,root,root,-)
%doc HACKING DEPENDENCIES THANKS ChangeLog
%doc %{_datadir}/doc/%{name}/*.html
%{_infodir}/%{name}.info*
%{_libdir}/%{name}.so
%{_includedir}/unistring
%{_includedir}/*.h

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%post devel
/sbin/install-info %{_infodir}/%{name}.info %{_infodir}/dir || :

%preun devel
if [ $1 = 0 ]; then
   /sbin/install-info --delete %{_infodir}/%{name}.info %{_infodir}/dir || :
fi

%changelog
* Wed Feb 29 2012 Stephen Gallagher <sgallagh@redhat.com> - 0.9.3-5
- Resolves: rhbz#732017 - Malloc without NULL check

* Mon Sep 12 2011 Stephen Gallagher <sgallagh@redhat.com> - 0.9.3-4
- Resolves: rhbz#737592 - %%preun error while uninstalling libunistring-devel

* Tue Aug 02 2011 Stephen Gallagher <sgallagh@redhat.com> - 0.9.3-3
- Imported from Fedora
- Resolves: rhbz#726463 - Add libunistring as a separate component/package
                          into RHEL
