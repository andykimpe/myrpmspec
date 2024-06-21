# Spec file for Qpid QMF packages
# svn revision: $Rev$

%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}
%{!?python_sitearch: %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")}

%{!?ruby_sitelib: %global ruby_sitelib %(/usr/bin/ruby -rrbconfig  -e 'puts Config::CONFIG["sitelibdir"] ')}
%{!?ruby_sitearch: %global ruby_sitearch %(/usr/bin/ruby -rrbconfig -e 'puts Config::CONFIG["sitearchdir"] ')}

# NOTE: no more than one of these flags should be set at the same time!
# RHEL-6 builds (the default) should have all these flags set to 0.
%global fedora              0
%global rhel_5              0

# LIBRARY VERSIONS
# Update these lib numbers in accordance with library numbering policy
# and best practices.
# http://www.gnu.org/software/libtool/manual/libtool.html#Versioning
#
# Fromat: current[:revision[:age]]
#
# current:  The most recent interface number that this library
#           implements.
# revision: The implementation number of the current interface.
# age:      The difference between the newest and oldest interfaces that
#           this library implements.  In other words, the library
#           implements all the interface numbers in the range from
#           number current - age to current.
#
#  1. Start with version information of ‘0:0:0’ for each libtool
#     library.
#  2. Update the version information only immediately before a public
#     release of your software.  More frequent updates are
#     unnecessary, and only guarantee that the current interface
#     number gets larger faster.
#  3. If the library source code has changed at all since the last
#     update, then increment revision (‘c:r:a’ becomes ‘c:r+1:a’).
#  4. If any interfaces have been added, removed, or changed since the
#     last update, increment current, and set revision to 0.
#  5. If any interfaces have been added since the last public release,
#     then increment age.
#  6. If any interfaces have been removed or changed since the last
#     public release, then set age to 0.

%global QPIDCOMMON_VERSION_INFO             7:0:0
%global QPIDTYPES_VERSION_INFO              3:1:2
%global QPIDBROKER_VERSION_INFO             7:0:0
%global QPIDCLIENT_VERSION_INFO             7:0:0
%global QPIDMESSAGING_VERSION_INFO          5:1:2
%global RDMAWRAP_VERSION_INFO               7:0:0
%global SSLCOMMON_VERSION_INFO              7:0:0

%global QMF_VERSION_INFO                    5:0:0
%global QMF2_VERSION_INFO                   1:1:0
%global QMFENGINE_VERSION_INFO              5:0:0
%global QMFCONSOLE_VERSION_INFO             6:0:0

# Single var with all lib version params (except store) for make
%global LIB_VERSION_MAKE_PARAMS QPIDCOMMON_VERSION_INFO=%{QPIDCOMMON_VERSION_INFO} QPIDTYPES_VERSION_INFO=%{QPIDTYPES_VERSION_INFO} QPIDBROKER_VERSION_INFO=%{QPIDBROKER_VERSION_INFO} QPIDCLIENT_VERSION_INFO=%{QPIDCLIENT_VERSION_INFO} QPIDMESSAGING_VERSION_INFO=%{QPIDMESSAGING_VERSION_INFO} QMF_VERSION_INFO=%{QMF_VERSION_INFO} QMF2_VERSION_INFO=%{QMF2_VERSION_INFO} QMFENGINE_VERSION_INFO=%{QMFENGINE_VERSION_INFO} QMFCONSOLE_VERSION_INFO=%{QMFCONSOLE_VERSION_INFO} RDMAWRAP_VERSION_INFO=%{RDMAWRAP_VERSION_INFO} SSLCOMMON_VERSION_INFO=%{SSLCOMMON_VERSION_INFO}

Name:          qpid-qmf
Version:       0.14
Release:       14%{?dist}
Summary:       The Qpid Management Framework
Group:         System Environment/Libraries
License:       ASL 2.0
URL:           http://qpid.apache.org
Vendor:        Red Hat, Inc.
Source0:       qpid-%{version}.tar.gz
Patch0:        mrg.patch
Patch1:        s390.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%if %{rhel_5}
ExclusiveArch: i386 x86_64
%endif

BuildRequires: boost-devel
BuildRequires: libtool
BuildRequires: pkgconfig
BuildRequires: ruby
BuildRequires: ruby-devel
BuildRequires: python-devel
BuildRequires: swig
BuildRequires: nss-devel
BuildRequires: nspr-devel

%if %{rhel_5}
BuildRequires: e2fsprogs-devel
%else
BuildRequires: boost-program-options
BuildRequires: boost-filesystem
BuildRequires: libuuid-devel
%endif


# === Package: qpid-qmf ===

Requires:      qpid-cpp-client = %{version}
Provides:      qmf = %{version}-%{release}
Obsoletes:     qmf < %{version}-%{release}

%description
An extensible management framework layered on Qpid messaging

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%{_libdir}/libqmf.so.*
%{_libdir}/libqmf2.so.*
%{_libdir}/libqmfengine.so.*
%{_libdir}/libqmfconsole.so.*
%exclude %{_libdir}/*.la


# === Package: qpid-qmf-devel ===
%package devel
Summary:       Header files and tools for developing QMF extensions
Group:         Development/System
Requires:      qpid-qmf = %{version}-%{release}
Requires:      qpid-cpp-client-devel = %{version}
Provides:      qmf-devel = %{version}-%{release}
Obsoletes:     qmf-devel < %{version}-%{release}

%description devel
Header files and code-generation tools needed for developers of QMF-managed
components.

%post devel -p /sbin/ldconfig

%postun devel -p /sbin/ldconfig

%files devel
%defattr(-,root,root,-)
%{_libdir}/libqmf.so
%{_libdir}/libqmf2.so
%{_libdir}/libqmfengine.so
%{_libdir}/libqmfconsole.so
%{_bindir}/qmf-gen
%{python_sitearch}/qmfgen
%{_includedir}/qmf
%{_includedir}/qpid/agent
%{_includedir}/qpid/console


#%ifnarch s390 s390x ppc ppc64
# === Package: python-qpid-qmf ===
%package -n python-qpid-qmf
Summary:       Python QMF library for Apache Qpid
Group:         Development/Python
Requires:      qpid-qmf = %{version}-%{release}
Requires:      qpid-cpp-client = %{version}
Requires:      python-qpid = %{version}
Provides:      python-qmf = %{version}-%{release}
Obsoletes:     python-qmf < %{version}-%{release}

%description -n python-qpid-qmf
Python QMF library for Apache Qpid

%files -n python-qpid-qmf
%defattr(-,root,root,-)
%{python_sitearch}/qmf
%{python_sitearch}/cqpid.py*
%{python_sitearch}/_cqpid.so
%{python_sitearch}/qmf.py*
%{python_sitearch}/qmfengine.py*
%{python_sitearch}/_qmfengine.so
%{python_sitearch}/qmf2.py*
%{python_sitearch}/cqmf2.py*
%{python_sitearch}/_cqmf2.so
%exclude %{python_sitearch}/mllib
%exclude %{python_sitearch}/qpid
#%exclude %{python_sitelib}/*.egg-info

#%endif

# === Package: ruby-qpid-qmf ===

%ifnarch s390 s390x ppc ppc64

%package -n ruby-qpid-qmf
Summary:       The QPID Management Framework bindings for ruby
Group:         System Environment/Libraries
Requires:      qpid-cpp-client = %{version}
Requires:      qpid-qmf = %{version}-%{release}
Provides:      ruby-qmf = %{version}-%{release}
Obsoletes:     ruby-qmf < %{version}-%{release}

%description -n ruby-qpid-qmf
An extensible managememt framework layered on QPID messaging, bindings
for ruby.

%post -n ruby-qpid-qmf -p /sbin/ldconfig

%postun -n ruby-qpid-qmf -p /sbin/ldconfig

%files -n ruby-qpid-qmf
%defattr(-,root,root,-)
%{ruby_sitelib}/qmf.rb
%{ruby_sitelib}/qmf2.rb
%{ruby_sitearch}/qmfengine.so
%{ruby_sitearch}/cqpid.so
%{ruby_sitearch}/cqmf2.so
%exclude %{ruby_sitearch}/*.la

%endif

# ===

%prep
%setup -q -n qpid-%{version}
%patch0 -p2
%patch1 -p2

%build
(
    cd cpp
    ./bootstrap
    export CXXFLAGS="%{optflags} -DNDEBUG -O3"
    %configure --with-swig --without-sasl --without-ssl \
        --without-help2man --without-cpg --without-libcman --without-xml \
        --without-rdma --without-doxygen
    %{__make} %{LIB_VERSION_MAKE_PARAMS}
)

(cd python; %{__python} setup.py build)
(cd extras/qmf; %{__python} setup.py build)

%install
rm -rf %{buildroot}

(cd cpp; make install DESTDIR=%{buildroot})
(cd python; %{__python} setup.py install --skip-build --root %{buildroot} --install-purelib %{python_sitearch})
(cd extras/qmf; %{__python} setup.py install --skip-build --root %{buildroot} --install-purelib %{python_sitearch})


#%ifnarch s390 s390x ppc ppc64
install -d %{buildroot}%{python_sitearch}
install -pm 644 %{_builddir}/qpid-%{version}/cpp/bindings/qpid/python/cqpid.py %{buildroot}%{python_sitearch}
install -pm 755 %{_builddir}/qpid-%{version}/cpp/bindings/qpid/python/.libs/_cqpid.so %{buildroot}%{python_sitearch}
install -pm 644 %{_builddir}/qpid-%{version}/cpp/bindings/qmf/python/*.py %{buildroot}%{python_sitearch}
install -pm 755 %{_builddir}/qpid-%{version}/cpp/bindings/qmf/python/.libs/_qmfengine.so %{buildroot}%{python_sitearch}
install -pm 644 %{_builddir}/qpid-%{version}/cpp/bindings/qmf2/python/*.py %{buildroot}%{python_sitearch}
install -pm 755 %{_builddir}/qpid-%{version}/cpp/bindings/qmf2/python/.libs/_cqmf2.so %{buildroot}%{python_sitearch}
#%endif


shopt -s extglob

rm -fr %{buildroot}%{_libdir}/!(libqmf*|ruby|python*)
rm -fr %{buildroot}%{_localstatedir}
rm -fr %{buildroot}%{_mandir}
rm -fr %{buildroot}%{_bindir}/!(qmf*)
rm -fr %{buildroot}%{_includedir}/qpid/!(agent|console)
rm -fr %{buildroot}%{_includedir}/qmf/org
rm -fr %{buildroot}%{_libexecdir}
rm -fr %{buildroot}%{_sbindir}
rm -fr %{buildroot}%{_sysconfdir}
rm -fr %{buildroot}%{_datadir}
rm -fr %{buildroot}%{python_sitelib}/qpid*.egg-info
rm -fr %{buildroot}%{python_sitearch}/qpid*.egg-info
rm -fr %{buildroot}%{python_sitelib}/_*.la

#%ifarch s390 s390x ppc ppc64
#rm -fr %{buildroot}%{python_sitearch}/qmf
#rm -fr %{buildroot}%{python_sitearch}/cqpid.py*
#rm -fr %{buildroot}%{python_sitearch}/_cqpid.so
#rm -fr %{buildroot}%{python_sitearch}/qmf.py*
#rm -fr %{buildroot}%{python_sitearch}/qmfengine.py*
#rm -fr %{buildroot}%{python_sitearch}/_qmfengine.so
#rm -fr %{buildroot}%{python_sitearch}/qmf2.py*
#rm -fr %{buildroot}%{python_sitearch}/cqmf2.py*
#rm -fr %{buildroot}%{python_sitearch}/_cqmf2.so
#rm -fr %{buildroot}%{python_sitearch}/mllib
#rm -fr %{buildroot}%{python_sitearch}/qpid
%ifarch s390 s390x ppc ppc64
rm -fr %{buildroot}%{ruby_sitelib}/qmf.rb
rm -fr %{buildroot}%{ruby_sitelib}/qmf2.rb
rm -fr %{buildroot}%{ruby_sitearch}/qmfengine.so
rm -fr %{buildroot}%{ruby_sitearch}/cqpid.so
rm -fr %{buildroot}%{ruby_sitearch}/cqmf2.so
rm -fr %{buildroot}%{ruby_sitearch}/*.la
%endif

%clean
rm -rf %{buildroot}

%changelog
* Thu Aug 16 2012 Justin Ross <jross@redhat.com> - 0.14-14
- BZs: 693845, 773700, 806869, 847331
* Fri Mar 16 2012 Nuno Santos <nsantos@redhat.com> - 0.14-6
- rhbz#801358
* Thu Mar 15 2012 Nuno Santos <nsantos@redhat.com> - 0.14-5
- rhbz#745600
* Fri Feb 10 2012 Nuno Santos <nsantos@redhat.com> - 0.14-4
- rhbz#765856
* Thu Dec  8 2011 Nuno Santos <nsantos@redhat.com> - 0.14-2
- Fixed install paths
* Tue Nov 29 2011 Justin Ross <jross@redhat.com> - 0.14-1
- Rebase to 0.14
- rhbz#743657 - The pure-python QMF console unnecessarily retains
  references to query results
- rhbz#699499 - [RFE] qmfv2 must provide mainloop integration
- rhbz#681680 - QMF agents wake up several times a second
- rhbz#663461 - Enable new architectures
- Remove python-qpid-qmf and ruby-qpid-qmf from ppc and s390 architectures
* Mon Oct 31 2011 Justin Ross <jross@redhat.com> - 0.10-11
- BZs 743657, 748738 - Prevent memory leak in python console
* Mon May 27 2011 Ted Ross <tross@redhat.com> - 0.10-10
- BZ 709343 - Packaging problem in qpid-qmf-devel (qmf-gen templates)
* Mon May 24 2011 Ted Ross <tross@redhat.com> - 0.10-9
- BZ 707023 - Fix rpmdiff errors
* Mon May  2 2011 Ted Ross <tross@redhat.com> - 0.10-7
- BZ 689907 - Fix rpmdiff errors
* Wed Apr 20 2011 Justin Ross <jross@redhat.com> - 0.10-6
- BZ 694416 - missing dependency of python-qpid-qmf
* Wed Mar 30 2011 Nuno Santos <nsantos@redhat.com> - 0.10-3
- BZ691812
* Tue Mar 22 2011 Nuno Santos <nsantos@redhat.com> - 0.10-1
- Initial version of consolidated, renamed qpid-qmf packages
