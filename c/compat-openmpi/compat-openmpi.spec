# We only compile with gcc, but other people may want other compilers.
# Set the compiler here.
%global opt_cc gcc
# Optional CFLAGS to use with the specific compiler...gcc doesn't need any,
# so uncomment and define to use
#global opt_cflags
%global opt_cxx g++
#global opt_cxxflags
%global opt_f77 gfortran
#global opt_fflags
%global opt_fc gfortran
#global opt_fcflags

%{!?python_sitearch: %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}
# Optional name suffix to use...we leave it off when compiling with gcc, but
# for other compiled versions to install side by side, it will need a
# suffix in order to keep the names from conflicting.
#global _cc_name_suffix -gcc

Name:			compat-openmpi%{?_cc_name_suffix}
Version:		1.4.3
Release:		5%{?dist}
Summary:		Open Message Passing Interface
Group:			Development/Libraries
License:		BSD, MIT and Romio
URL:			http://www.open-mpi.org/
# openmpi-1.4.3 for compat with RHEL 6.0, 6.1.
# We can't use %{name} here because of _cc_name_suffix
#Source0:		http://www.open-mpi.org/software/ompi/v1.4/downloads/openmpi-%{version}.tar.bz2
# openmpi-1.4.3-RH.tar.bz2 was generated by taking the upstream 1.4.3 tarball
# and removing license-incompatible files
# (MoreDebugging/* is AML but unused in our configuration),
# (ras_loadleveler_module.c ...)
# and packaging-guidelines-incompatable (MUST use system versions of libltdl
# and libplpa, not the (formerly included ones), and also remove the generated
# Makefile.in and configure related files.
Source0:		openmpi-%{version}-RH.tar.bz2
Source1:		openmpi.module.in
Source2:		macros.openmpi.in
Patch0:			openmpi-1.4.3-autogen.patch

# openmpi-1.5.3 for compat with RHEL 6.2.
# openmpi-1.5.3-RH.tar.bz2 was generated by taking the upstream 1.5.3 tarball
# and removing license-incompatible files
# (MoreDebugging/* is AML but unused in our configuration),
Source100:		openmpi-1.5.3-RH.tbz
Patch100:		openmpi-1.5-dt-textrel.patch
Patch101:		openmpi-1.5.3-build.patch

# openmpi-1.5.4 for compat with RHEL 6.3, 6.4, 6.5.
# openmpi-1.5.4-RH.tbz was generated by taking the upstream 1.5.4 tarball
# and removing license-incompatible files
# (MoreDebugging/* is AML but unused in our configuration),
Source200:		openmpi-1.5.4-RH.tbz

# openmpi-1.8.1 for compat with RHEL 6.6, 6.7.
Source300:		http://www.open-mpi.org/software/ompi/v1.8/downloads/openmpi-1.8.1.tar.bz2
# Patch to use system ltdl for tests
Patch300:		openmpi-ltdl.patch
# Patch to fix errors detected by running mpitests-IMB_EXT with infinipath-psm
Patch301:		openmpi-1.8.1-onesided.patch

BuildRequires:		flex
BuildRequires:		gcc-gfortran, libtool, numactl-devel
BuildRequires:		libibverbs-devel >= 1.1.3, opensm-devel > 3.3.0
BuildRequires:		librdmacm librdmacm-devel libibcm libibcm-devel
BuildRequires:		papi-devel
BuildRequires:		python libtool-ltdl-devel plpa-devel
BuildRequires:		libesmtp-devel
#sparc 64 doesnt have valgrind
%ifnarch %{sparc}
BuildRequires:          valgrind-devel
%endif
#%ifnarch ppc
#BuildRequires:		compat-dapl-devel
#%endif
%ifarch x86_64
BuildRequires:		infinipath-psm-devel
%endif

# s390 is unlikely to have the hardware we want, and some of the -devel
# packages we require aren't available there.
# ARM has issues with a lack of "atomic primitives" so we'll exclude it as well for the moment
ExcludeArch: s390 s390x %{arm}

# Private openmpi libraries
%{?filter_setup:           
%filter_from_provides /^libmca_common_sm.so.2/d
%filter_from_provides /^libompi_dbg_msgq.so/d  
%filter_from_provides /^libompitrace.so.0/d  
%filter_from_provides /^libopen-pal.so.3/d 
%filter_from_provides /^libopen-rte.so.3/d
%filter_from_provides /^libotf.so.0/d     
%filter_from_provides /^libvt-hyb.so.0/d
%filter_from_provides /^libvt-mpi.so.0/d
%filter_from_provides /^libvt-mt.so.0/d 
%filter_from_provides /^libvt.so.0/d   
%filter_from_provides /^mca_/d      
%filter_from_requires /^libmca_common_sm.so.2/d
%filter_from_requires /^libompitrace.so.0/d    
%filter_from_requires /^libopen-pal.so.3/d 
%filter_from_requires /^libopen-rte.so.3/d
%filter_from_requires /^libotf.so.0/d     
%filter_from_requires /^libvt-hyb.so.0/d
%filter_from_requires /^libvt-mpi.so.0/d
%filter_from_requires /^libvt-mt.so.0/d 
%filter_from_requires /^libvt.so.0/d   
%filter_setup                       
}            
%global __provides_exclude_from %{_libdir}/openmpi/lib/(lib(mca|ompi|open-(pal|rte|trace)|otf|v)|openmpi/).*.so
%global __requires_exclude lib(mca|ompi|open-(pal|rte|trace)|otf|vt).*

%global common_desc Open MPI is an open source, freely available implementation of both the\
MPI-1 and MPI-2 standards, combining technologies and resources from\
several other projects (FT-MPI, LA-MPI, LAM/MPI, and PACX-MPI) in\
order to build the best MPI library available.  A completely new MPI-2\
compliant implementation, Open MPI offers advantages for system and\
software vendors, application developers, and computer science\
researchers. For more information, see http://www.open-mpi.org/ .

%description
%{common_desc}

%package -n openmpi-1.4%{?_cc_name_suffix}
Summary:	Open Message Passing Interface 1.4
Group:		Development/Libraries
Version:	1.4.3
Release:	%{release}
Provides:	mpi
Requires:	environment-modules
Obsoletes:	openmpi < 1.4.3-3
Obsoletes:	compat-openmpi < 1.4.3-3

%description -n openmpi-1.4%{?_cc_name_suffix}
%{common_desc}

This package provides compatibility for applications compiled with Open MPI
version 1.4.

%package -n openmpi-1.4%{?_cc_name_suffix}-devel
Summary:        Development files for openmpi-1.4
Group:          Development/Libraries
Version:	1.4.3
Release:	%{release}
Requires:       openmpi-1.4%{?_cc_name_suffix}%{?_isa} = %{version}-%{release}, gcc-gfortran
Provides:	mpi-devel
Obsoletes:	openmpi-devel < 1.4.3-3
Obsoletes:	compat-openmpi-devel < 1.4.3-3

%description -n openmpi-1.4%{?_cc_name_suffix}-devel
Contains development headers and libraries for openmpi-1.4.

%ifarch x86_64

%package -n openmpi-1.4-psm%{?_cc_name_suffix}
Summary:	Open Message Passing Interface 1.4 using InfiniPath
Group:		Development/Libraries
Version:	1.4.3
Release:	%{release}
Provides:	mpi
Requires:	environment-modules
Obsoletes:	openmpi-psm < 1.4.3-3
Obsoletes:	compat-openmpi-psm < 1.4.3-3

%description -n openmpi-1.4-psm%{?_cc_name_suffix}
%{common_desc}

This package provides compatibility for applications compiled with Open MPI
version 1.4 using InfiniPath.

%package -n openmpi-1.4-psm%{?_cc_name_suffix}-devel
Summary:        Development files for openmpi-1.4-psm
Group:          Development/Libraries
Version:	1.4.3
Release:	%{release}
Requires:       openmpi-1.4-psm%{?_cc_name_suffix}%{?_isa} = %{version}-%{release}, gcc-gfortran
Provides:	mpi-devel
Obsoletes:	openmpi-psm-devel < 1.4.3-3
Obsoletes:	compat-openmpi-psm-devel < 1.4.3-3

%description -n openmpi-1.4-psm%{?_cc_name_suffix}-devel
Contains development headers and libraries for openmpi-1.4-psm.

%endif

%package -n openmpi-1.5.3%{?_cc_name_suffix}
Summary:	Open Message Passing Interface 1.5.3
Group:		Development/Libraries
Version:	1.5.3
Release:	%{release}
Provides:	mpi
Requires:	environment-modules
Obsoletes:	openmpi < 1.5.3-4
Obsoletes:	compat-openmpi < 1.4.3-3

%description -n openmpi-1.5.3%{?_cc_name_suffix}
%{common_desc}

This package provides compatibility for applications compiled with Open MPI
version 1.5.3.

%package -n openmpi-1.5.3%{?_cc_name_suffix}-devel
Summary:        Development files for openmpi-1.5.3
Group:          Development/Libraries
Version:	1.5.3
Release:	%{release}
Requires:       openmpi-1.5.3%{?_cc_name_suffix}%{?_isa} = %{version}-%{release}, gcc-gfortran
Provides:	mpi-devel
Obsoletes:	openmpi-devel < 1.5.3-4
Obsoletes:	compat-openmpi-devel < 1.4.3-3

%description -n openmpi-1.5.3%{?_cc_name_suffix}-devel
Contains development headers and libraries for openmpi-1.5.3.

%ifarch x86_64

%package -n openmpi-1.5.3-psm%{?_cc_name_suffix}
Summary:	Open Message Passing Interface 1.5.3 using InfiniPath
Group:		Development/Libraries
Version:	1.5.3
Release:	%{release}
Provides:	mpi
Requires:	environment-modules
Obsoletes:	openmpi-psm < 1.5.3-4
Obsoletes:	compat-openmpi-psm < 1.4.3-3

%description -n openmpi-1.5.3-psm%{?_cc_name_suffix}
%{common_desc}

This package provides compatibility for applications compiled with Open MPI
version 1.5.3 using InfiniPath.

%package -n openmpi-1.5.3-psm%{?_cc_name_suffix}-devel
Summary:        Development files for openmpi-1.5.3-psm
Group:          Development/Libraries
Version:	1.5.3
Release:	%{release}
Requires:       openmpi-1.5.3-psm%{?_cc_name_suffix}%{?_isa} = %{version}-%{release}, gcc-gfortran
Provides:	mpi-devel
Obsoletes:	openmpi-psm-devel < 1.5.3-4
Obsoletes:	compat-openmpi-psm-devel < 1.4.3-3

%description -n openmpi-1.5.3-psm%{?_cc_name_suffix}-devel
Contains development headers and libraries for openmpi-1.5.3-psm.

%endif

%package -n openmpi-1.5.4%{?_cc_name_suffix}
Summary:	Open Message Passing Interface 1.5.4
Group:		Development/Libraries
Version:	1.5.4
Release:	%{release}
Provides:	mpi
Requires:	environment-modules
Obsoletes:	openmpi < 1.5.4-3
Obsoletes:	openmpi-psm < 1.5.4-3

%description -n openmpi-1.5.4%{?_cc_name_suffix}
%{common_desc}

This package provides compatibility for applications compiled with Open MPI
version 1.5.4.

%package -n openmpi-1.5.4%{?_cc_name_suffix}-devel
Summary:        Development files for openmpi-1.5.4
Group:          Development/Libraries
Version:	1.5.4
Release:	%{release}
Requires:       openmpi-1.5.4%{?_cc_name_suffix}%{?_isa} = %{version}-%{release}, gcc-gfortran
Provides:	mpi-devel
Obsoletes:	openmpi-devel < 1.5.4-3
Obsoletes:	openmpi-psm-devel < 1.5.4-3

%description -n openmpi-1.5.4%{?_cc_name_suffix}-devel
Contains development headers and libraries for openmpi-1.5.4.

%package -n openmpi-1.8%{?_cc_name_suffix}
Summary:	Open Message Passing Interface 1.8
Group:		Development/Libraries
Version:	1.8.1
Release:	%{release}
Provides:	mpi
Requires:	environment-modules
# openmpi currently requires ssh to run
# https://svn.open-mpi.org/trac/ompi/ticket/4228
Requires:	openssh-clients

Obsoletes:	openmpi < 1.8.1-3
Provides:	openmpi = 1.8.1-%{release}
Provides:	openmpi%{?_isa} = 1.8.1-%{release}

%description -n openmpi-1.8%{?_cc_name_suffix}
%{common_desc}

This package provides compatibility for applications compiled with Open MPI
version 1.8.

%package -n openmpi-1.8%{?_cc_name_suffix}-devel
Summary:        Development files for openmpi-1.8
Group:          Development/Libraries
Version:	1.8.1
Release:	%{release}
Requires:       openmpi-1.8%{?_cc_name_suffix}%{?_isa} = %{version}-%{release}, gcc-gfortran
Provides:	mpi-devel
Obsoletes:	openmpi-devel < 1.8.1-3
Provides:	openmpi-devel = 1.8.1-%{release}
Provides:	openmpi-devel%{?_isa} = 1.8.1-%{release}

%description -n openmpi-1.8%{?_cc_name_suffix}-devel
Contains development headers and libraries for openmpi-1.8.

# When dealing with multilib installations, aka the ability to run either
# i386 or x86_64 binaries on x86_64 machines, we install the native i386
# openmpi libs/compilers and the native x86_64 libs/compilers.  Obviously,
# on i386 you can only run i386, so you don't really need the -m32 flag
# to gcc in order to force 32 bit mode.  However, since we use the native
# i386 package to support i386 operation on x86_64, and since on x86_64
# the default is x86_64, the i386 package needs to force i386 mode.  This
# is true of all the multilib arches, hence the non-default arch (aka i386
# on x86_64) must force the non-default mode (aka 32 bit compile) in it's
# native-arch package (aka, when built on i386) so that it will work
# properly on the non-native arch as a multilib package (aka i386 installed
# on x86_64).  Just to be safe, we also force the default mode (aka 64 bit)
# in default arch packages (aka, the x86_64 package).  There are, however,
# some arches that don't support forcing *any* mode, those we just leave
# undefined.
%ifarch %{ix86} ppc sparcv9
%define mode 32
%define modeflag -m32
%endif
%ifarch ia64
%define mode 64
%endif
%ifarch x86_64 ppc64 sparc64
%define mode 64
%define modeflag -m64
%endif

%prep
%setup -q -n openmpi-1.4.3 -b 100 -b 200 -b 300
%patch0 -p1 -b .ltversion
cd ..

cd openmpi-1.5.3
%patch100 -p1 -b .dt-textrel
%patch101 -p1 -b .build
cd ..

cd openmpi-1.8.1
%patch300 -p1 -b .ltdl
%patch301 -p1 -b .onesided
cd ..

cd openmpi-1.4.3
  mkdir .non-psm
  mv * .non-psm
  mv .non-psm non-psm

%ifarch x86_64
  mkdir psm
  cp -pr non-psm/* psm
%endif

  cd non-psm
    ./autogen.sh
    cd opal/libltdl
      ../../autogen.sh
    cd ../..
  cd ..

%ifarch x86_64
  cd psm
    ./autogen.sh
    cd opal/libltdl
      ../../autogen.sh
    cd ../..
  cd ..
%endif
cd ..

cd openmpi-1.5.3
  mkdir .non-psm
  mv * .non-psm
  mv .non-psm non-psm

%ifarch x86_64
  mkdir psm
  cp -pr non-psm/* psm
%endif

  cd non-psm
    ./autogen.sh
  cd ..

%ifarch x86_64
  cd psm
    ./autogen.sh
  cd ..
%endif
cd ..

cd openmpi-1.8.1
  # Make sure we don't use the local libltdl library
  rm -r opal/libltdl
cd ..

%build
cd ..
XFLAGS="-fPIC"

# We set this to for convenience, since this is the unique dir we use for this
# particular package, version, compiler
%global variant openmpi-1.4
%global libname %{variant}%{?_cc_name_suffix}
%global namearch %{variant}-%{_arch}%{?_cc_name_suffix}

cd openmpi-1.4.3/non-psm
./configure --prefix=%{_libdir}/%{libname} --with-libnuma=/usr \
	--with-openib=/usr \
	--mandir=%{_mandir}/%{namearch} \
	--includedir=%{_includedir}/%{namearch} \
	--sysconfdir=%{_sysconfdir}/%{namearch} \
	--enable-mpi-threads \
	--enable-openib-ibcm \
	--with-psm=no \
	--with-sge \
	--with-valgrind \
	--with-wrapper-cflags="%{?opt_cflags} %{?modeflag}" \
	--with-wrapper-cxxflags="%{?opt_cxxflags} %{?modeflag}" \
	--with-wrapper-fflags="%{?opt_fflags} %{?modeflag}" \
	--with-wrapper-fcflags="%{?opt_fcflags} %{?modeflag}" \
	CC=%{opt_cc} CXX=%{opt_cxx} \
	LDFLAGS='-Wl,-z,noexecstack' \
	CFLAGS="%{?opt_cflags} $RPM_OPT_FLAGS $XFLAGS" \
	CXXFLAGS="%{?opt_cxxflags} $RPM_OPT_FLAGS $XFLAGS" \
	FC=%{opt_fc} FCFLAGS="%{?opt_fcflags} $RPM_OPT_FLAGS $XFLAGS" \
	F77=%{opt_f77} FFLAGS="%{?opt_fflags} $RPM_OPT_FLAGS $XFLAGS"

make %{?_smp_mflags}
cd ../..

%ifarch x86_64
%global variant openmpi-1.4-psm
%global libname %{variant}%{?_cc_name_suffix}
%global namearch %{variant}-%{_arch}%{?_cc_name_suffix}

cd openmpi-1.4.3/psm
./configure --prefix=%{_libdir}/%{libname} --with-libnuma=/usr \
	--with-openib=/usr \
	--mandir=%{_mandir}/%{namearch} \
	--includedir=%{_includedir}/%{namearch} \
	--sysconfdir=%{_sysconfdir}/%{namearch} \
	--enable-mpi-threads \
	--enable-openib-ibcm \
	--with-sge \
	--with-valgrind \
	--with-wrapper-cflags="%{?opt_cflags} %{?modeflag}" \
	--with-wrapper-cxxflags="%{?opt_cxxflags} %{?modeflag}" \
	--with-wrapper-fflags="%{?opt_fflags} %{?modeflag}" \
	--with-wrapper-fcflags="%{?opt_fcflags} %{?modeflag}" \
	CC=%{opt_cc} CXX=%{opt_cxx} \
	LDFLAGS='-Wl,-z,noexecstack' \
	CFLAGS="%{?opt_cflags} $RPM_OPT_FLAGS $XFLAGS" \
	CXXFLAGS="%{?opt_cxxflags} $RPM_OPT_FLAGS $XFLAGS" \
	FC=%{opt_fc} FCFLAGS="%{?opt_fcflags} $RPM_OPT_FLAGS $XFLAGS" \
	F77=%{opt_f77} FFLAGS="%{?opt_fflags} $RPM_OPT_FLAGS $XFLAGS"

make %{?_smp_mflags}
cd ../..
%endif

# openmpi-1.5.3 owns the name "compat-openmpi" it had in RHEL 6.7.
%global variant compat-openmpi
%global libname %{variant}%{?_cc_name_suffix}
%global namearch %{variant}-%{_arch}%{?_cc_name_suffix}

cd openmpi-1.5.3/non-psm
./configure --prefix=%{_libdir}/%{libname} --with-libnuma=/usr \
	--with-openib=/usr \
	--mandir=%{_mandir}/%{namearch} \
	--includedir=%{_includedir}/%{namearch} \
	--sysconfdir=%{_sysconfdir}/%{namearch} \
	--with-sge \
	--with-libltdl=external \
%ifnarch %{sparc}
	--with-valgrind \
	--enable-memchecker \
%endif
%ifarch x86_64
	--with-psm=no \
%endif
	--with-esmtp \
	--with-wrapper-cflags="%{?opt_cflags} %{?modeflag}" \
	--with-wrapper-cxxflags="%{?opt_cxxflags} %{?modeflag}" \
	--with-wrapper-fflags="%{?opt_fflags} %{?modeflag}" \
	--with-wrapper-fcflags="%{?opt_fcflags} %{?modeflag}" \
	CC=%{opt_cc} CXX=%{opt_cxx} \
	LDFLAGS='-Wl,-z,noexecstack' \
	CFLAGS="%{?opt_cflags} $RPM_OPT_FLAGS $XFLAGS" \
	CXXFLAGS="%{?opt_cxxflags} $RPM_OPT_FLAGS $XFLAGS" \
	FC=%{opt_fc} FCFLAGS="%{?opt_fcflags} $RPM_OPT_FLAGS $XFLAGS" \
	F77=%{opt_f77} FFLAGS="%{?opt_fflags} $RPM_OPT_FLAGS $XFLAGS"

# removed, disabled in 1.5.3 because it is broken
#	--enable-openib-ibcm \

make %{?_smp_mflags}
cd ../..

%ifarch x86_64
%global variant compat-openmpi-psm
%global libname %{variant}%{?_cc_name_suffix}
%global namearch %{variant}-%{_arch}%{?_cc_name_suffix}

cd openmpi-1.5.3/psm
./configure --prefix=%{_libdir}/%{libname} --with-libnuma=/usr \
	--with-openib=/usr \
	--mandir=%{_mandir}/%{namearch} \
	--includedir=%{_includedir}/%{namearch} \
	--sysconfdir=%{_sysconfdir}/%{namearch} \
	--with-sge \
	--with-libltdl=external \
	--with-valgrind \
	--enable-memchecker \
	--with-esmtp \
	--with-wrapper-cflags="%{?opt_cflags} %{?modeflag}" \
	--with-wrapper-cxxflags="%{?opt_cxxflags} %{?modeflag}" \
	--with-wrapper-fflags="%{?opt_fflags} %{?modeflag}" \
	--with-wrapper-fcflags="%{?opt_fcflags} %{?modeflag}" \
	CC=%{opt_cc} CXX=%{opt_cxx} \
	LDFLAGS='-Wl,-z,noexecstack' \
	CFLAGS="%{?opt_cflags} $RPM_OPT_FLAGS $XFLAGS" \
	CXXFLAGS="%{?opt_cxxflags} $RPM_OPT_FLAGS $XFLAGS" \
	FC=%{opt_fc} FCFLAGS="%{?opt_fcflags} $RPM_OPT_FLAGS $XFLAGS" \
	F77=%{opt_f77} FFLAGS="%{?opt_fflags} $RPM_OPT_FLAGS $XFLAGS"

# removed, disabled in 1.5.3 because it is broken
#	--enable-openib-ibcm \
# Removed to close rhbz#741794
#	--enable-mpi-threads \

make %{?_smp_mflags}
cd ../..
%endif

%global variant openmpi-1.5.4
%global libname %{variant}%{?_cc_name_suffix}
%global namearch %{variant}-%{_arch}%{?_cc_name_suffix}

cd openmpi-1.5.4
./configure --prefix=%{_libdir}/%{libname} --with-libnuma=/usr \
	--with-openib=/usr \
	--mandir=%{_mandir}/%{namearch} \
	--includedir=%{_includedir}/%{namearch} \
	--sysconfdir=%{_sysconfdir}/%{namearch} \
	--with-sge \
	--with-libltdl=external \
%ifnarch %{sparc}
	--with-valgrind \
	--enable-memchecker \
%endif
	--with-esmtp \
	--with-wrapper-cflags="%{?opt_cflags} %{?modeflag}" \
	--with-wrapper-cxxflags="%{?opt_cxxflags} %{?modeflag}" \
	--with-wrapper-fflags="%{?opt_fflags} %{?modeflag}" \
	--with-wrapper-fcflags="%{?opt_fcflags} %{?modeflag}" \
	CC=%{opt_cc} CXX=%{opt_cxx} \
	LDFLAGS='-Wl,-z,noexecstack' \
	CFLAGS="%{?opt_cflags} $RPM_OPT_FLAGS $XFLAGS" \
	CXXFLAGS="%{?opt_cxxflags} $RPM_OPT_FLAGS $XFLAGS" \
	FC=%{opt_fc} FCFLAGS="%{?opt_fcflags} $RPM_OPT_FLAGS $XFLAGS" \
	F77=%{opt_f77} FFLAGS="%{?opt_fflags} $RPM_OPT_FLAGS $XFLAGS"

make %{?_smp_mflags}
cd ..

# openmpi-1.8.1 owns the name "openmpi" it had in RHEL 6.7.
%global variant openmpi
%global libname %{variant}%{?_cc_name_suffix}
%global namearch %{variant}-%{_arch}%{?_cc_name_suffix}

cd openmpi-1.8.1
# Note that the versions of libevent and hwloc shipped in RHEL-6 are too
# old for openmpi-1.8.1 to use, therefore we have to use the internal version.
./configure --prefix=%{_libdir}/%{libname} \
	--mandir=%{_mandir}/%{namearch} \
	--includedir=%{_includedir}/%{namearch} \
	--sysconfdir=%{_sysconfdir}/%{namearch} \
	--disable-silent-rules \
	--with-libevent=internal \
	--with-hwloc=internal \
	--with-verbs=/usr \
	--with-sge \
%ifnarch %{sparc} aarch64
	--with-valgrind \
	--enable-memchecker \
%endif
	--with-libltdl=/usr \
	CC=%{opt_cc} CXX=%{opt_cxx} \
	CFLAGS="%{?opt_cflags} %{!?opt_cflags:$RPM_OPT_FLAGS}" \
	CXXFLAGS="%{?opt_cxxflags} %{!?opt_cxxflags:$RPM_OPT_FLAGS}" \
	FC=%{opt_fc} FCFLAGS="%{?opt_fcflags} %{!?opt_fcflags:$RPM_OPT_FLAGS}" \
	F77=%{opt_f77} FFLAGS="%{?opt_fflags} %{!?opt_fflags:$RPM_OPT_FLAGS}"

make %{?_smp_mflags} V=1
cd ..


%install
cd ..

finish_install() {
	local VARIANT=$1
	local LIBNAME="$VARIANT%{?_cc_name_suffix}"
	local NAMEARCH="$VARIANT-%{_arch}%{?_cc_name_suffix}"

	rm -fr %{buildroot}%{_libdir}/$LIBNAME/lib/pkgconfig
	find %{buildroot}%{_libdir}/$LIBNAME/lib -name \*.la | xargs rm
	find %{buildroot}%{_mandir}/$NAMEARCH -type f | xargs gzip -9
	ln -s mpicc.1.gz %{buildroot}%{_mandir}/$NAMEARCH/man1/mpiCC.1.gz
	rm -f %{buildroot}%{_mandir}/$NAMEARCH/man1/mpiCC.1
	rm -f %{buildroot}%{_mandir}/$NAMEARCH/man1/orteCC.1*
	rm -f %{buildroot}%{_libdir}/$LIBNAME/share/vampirtrace/doc/opari/lacsi01.ps.gz
	mkdir %{buildroot}%{_mandir}/$NAMEARCH/man{2,4,5,6,8,9,n}
	mkdir -p %{buildroot}/%{_fmoddir}/$NAMEARCH
	mkdir -p %{buildroot}/%{python_sitearch}/$LIBNAME

	# Make the environment-modules file
	mkdir -p %{buildroot}%{_sysconfdir}/modulefiles
	# Since we're doing our own substitution here, use our own definitions.
	sed "s#@LIBDIR@#%{_libdir}/$LIBNAME#g;
	     s#@ETCDIR@#%{_sysconfdir}/$NAMEARCH#g;
	     s#@FMODDIR@#%{_fmoddir}/$NAMEARCH#g;
	     s#@INCDIR@#%{_includedir}/$NAMEARCH#g;
	     s#@MANDIR@#%{_mandir}/$NAMEARCH#g;
	     s#@PYSITEARCH@#%{python_sitearch}/$LIBNAME#g;
	     s#@COMPILER@#$VARIANT-%{_arch}%{?_cc_name_suffix}#g;
	     s#@SUFFIX@#%{?_cc_name_suffix}_$VARIANT#g" \
		< %SOURCE1 \
		> %{buildroot}%{_sysconfdir}/modulefiles/$NAMEARCH

	# make the rpm config file
	mkdir -p %{buildroot}/%{_sysconfdir}/rpm
	# do not expand _arch
	sed "s#@MACRONAME@#${LIBNAME//[-.]/_}#g;
	     s#@MODULENAME@#$VARIANT-%%{_arch}%{?_cc_name_suffix}#" \
		< %SOURCE2 \
		> %{buildroot}/%{_sysconfdir}/rpm/macros.$NAMEARCH
}

cd openmpi-1.4.3/non-psm
make install DESTDIR=%{buildroot}
cd ../..
finish_install openmpi-1.4

%ifarch x86_64
cd openmpi-1.4.3/psm
make install DESTDIR=%{buildroot}
cd ../..
finish_install openmpi-1.4-psm
%endif

cd openmpi-1.5.3/non-psm
make install DESTDIR=%{buildroot}
cd ../..
finish_install compat-openmpi

ln -s compat-openmpi-%{_arch}%{?_cc_name_suffix} \
	%{buildroot}%{_sysconfdir}/modulefiles/openmpi-1.5.3-%{_arch}%{?_cc_name_suffix}
ln -s compat-openmpi-%{_arch}%{?_cc_name_suffix} \
	%{buildroot}%{_sysconfdir}/openmpi-1.5.3-%{_arch}%{?_cc_name_suffix}

%ifarch x86_64
cd openmpi-1.5.3/psm
make install DESTDIR=%{buildroot}
cd ../..
finish_install compat-openmpi-psm

ln -s compat-openmpi-psm-%{_arch}%{?_cc_name_suffix} \
	%{buildroot}%{_sysconfdir}/modulefiles/openmpi-1.5.3-psm-%{_arch}%{?_cc_name_suffix}
ln -s compat-openmpi-psm-%{_arch}%{?_cc_name_suffix} \
	%{buildroot}%{_sysconfdir}/openmpi-1.5.3-psm-%{_arch}%{?_cc_name_suffix}

%endif

cd openmpi-1.5.4
make install DESTDIR=%{buildroot}
cd ..
finish_install openmpi-1.5.4

%global variant openmpi
%global libname %{variant}%{?_cc_name_suffix}
%global namearch %{variant}-%{_arch}%{?_cc_name_suffix}

cd openmpi-1.8.1
make install DESTDIR=%{buildroot}
cd ..
finish_install openmpi

# Remove extraneous wrapper link libraries (bug 814798)
sed -i -e s/-ldl// -e s/-lhwloc// \
  %{buildroot}%{_libdir}/%{libname}/share/openmpi/*-wrapper-data.txt

ln -s openmpi-%{_arch}%{?_cc_name_suffix} \
	%{buildroot}%{_sysconfdir}/modulefiles/openmpi-1.8-%{_arch}%{?_cc_name_suffix}
ln -s openmpi-%{_arch}%{?_cc_name_suffix} \
	%{buildroot}%{_sysconfdir}/openmpi-1.8-%{_arch}%{?_cc_name_suffix}

%check
cd ..

cd openmpi-1.8.1
make check
cd ..

%global variant openmpi-1.4
%global libname %{variant}%{?_cc_name_suffix}
%global namearch %{variant}-%{_arch}%{?_cc_name_suffix}

%files -n openmpi-1.4%{?_cc_name_suffix}
%dir %{_libdir}/%{libname}
%dir %{_sysconfdir}/%{namearch}
%dir %{_libdir}/%{libname}/bin
%dir %{_libdir}/%{libname}/lib
%dir %{_libdir}/%{libname}/lib/openmpi
%dir %{_mandir}/%{namearch}
%dir %{_mandir}/%{namearch}/man*
%dir %{_fmoddir}/%{namearch}
%dir %{python_sitearch}/%{libname}
%config(noreplace) %{_sysconfdir}/%{namearch}/*
%{_libdir}/%{libname}/bin/mpi[er]*
%{_libdir}/%{libname}/bin/ompi*
#%{_libdir}/%{libname}/bin/opal-*
%{_libdir}/%{libname}/bin/opari
%{_libdir}/%{libname}/bin/orte*
%{_libdir}/%{libname}/bin/otf*
%{_libdir}/%{libname}/lib/*.so.*
%{_mandir}/%{namearch}/man1/mpi[er]*
%{_mandir}/%{namearch}/man1/ompi*
#%{_mandir}/%{namearch}/man1/opal-*
%{_mandir}/%{namearch}/man1/orte*
%{_mandir}/%{namearch}/man7/ompi*
%{_mandir}/%{namearch}/man7/orte*
%{_libdir}/%{libname}/lib/openmpi/*
%{_sysconfdir}/modulefiles/%{namearch}
%dir %{_libdir}/%{libname}/share
%dir %{_libdir}/%{libname}/share/openmpi
%{_libdir}/%{libname}/share/openmpi/doc
%{_libdir}/%{libname}/share/openmpi/amca-param-sets
%{_libdir}/%{libname}/share/openmpi/help*.txt
%{_libdir}/%{libname}/share/openmpi/mca-btl-openib-device-params.ini

%files -n openmpi-1.4%{?_cc_name_suffix}-devel
%dir %{_includedir}/%{namearch}
%dir %{_libdir}/%{libname}/share/vampirtrace
%{_libdir}/%{libname}/bin/mpi[cCf]*
%{_libdir}/%{libname}/bin/vt*
%{_libdir}/%{libname}/bin/opal_*
%{_includedir}/%{namearch}/*
%{_libdir}/%{libname}/lib/*.so
%{_libdir}/%{libname}/lib/lib*.a
%{_libdir}/%{libname}/lib/mpi.mod
%{_mandir}/%{namearch}/man1/mpi[cCf]*
%{_mandir}/%{namearch}/man1/opal_*
%{_mandir}/%{namearch}/man3/*
%{_mandir}/%{namearch}/man7/opal*
%{_libdir}/%{libname}/share/openmpi/openmpi-valgrind.supp
%{_libdir}/%{libname}/share/openmpi/mpi*.txt
%{_libdir}/%{libname}/share/vampirtrace/*
%{_sysconfdir}/rpm/macros.%{namearch}

%ifarch x86_64
%global variant openmpi-1.4-psm
%global libname %{variant}%{?_cc_name_suffix}
%global namearch %{variant}-%{_arch}%{?_cc_name_suffix}

%files -n openmpi-1.4-psm%{?_cc_name_suffix}
%dir %{_libdir}/%{libname}
%dir %{_sysconfdir}/%{namearch}
%dir %{_libdir}/%{libname}/bin
%dir %{_libdir}/%{libname}/lib
%dir %{_libdir}/%{libname}/lib/openmpi
%dir %{_mandir}/%{namearch}
%dir %{_mandir}/%{namearch}/man*
%dir %{_fmoddir}/%{namearch}
%dir %{python_sitearch}/%{libname}
%config(noreplace) %{_sysconfdir}/%{namearch}/*
%{_libdir}/%{libname}/bin/mpi[er]*
%{_libdir}/%{libname}/bin/ompi*
#%{_libdir}/%{libname}/bin/opal-*
%{_libdir}/%{libname}/bin/opari
%{_libdir}/%{libname}/bin/orte*
%{_libdir}/%{libname}/bin/otf*
%{_libdir}/%{libname}/lib/*.so.*
%{_mandir}/%{namearch}/man1/mpi[er]*
%{_mandir}/%{namearch}/man1/ompi*
#%{_mandir}/%{namearch}/man1/opal-*
%{_mandir}/%{namearch}/man1/orte*
%{_mandir}/%{namearch}/man7/ompi*
%{_mandir}/%{namearch}/man7/orte*
%{_libdir}/%{libname}/lib/openmpi/*
%{_sysconfdir}/modulefiles/%{namearch}
%dir %{_libdir}/%{libname}/share
%dir %{_libdir}/%{libname}/share/openmpi
%{_libdir}/%{libname}/share/openmpi/doc
%{_libdir}/%{libname}/share/openmpi/amca-param-sets
%{_libdir}/%{libname}/share/openmpi/help*.txt
%{_libdir}/%{libname}/share/openmpi/mca-btl-openib-device-params.ini

%files -n openmpi-1.4-psm%{?_cc_name_suffix}-devel
%dir %{_includedir}/%{namearch}
%dir %{_libdir}/%{libname}/share/vampirtrace
%{_libdir}/%{libname}/bin/mpi[cCf]*
%{_libdir}/%{libname}/bin/vt*
%{_libdir}/%{libname}/bin/opal_*
%{_includedir}/%{namearch}/*
%{_libdir}/%{libname}/lib/*.so
%{_libdir}/%{libname}/lib/lib*.a
%{_libdir}/%{libname}/lib/mpi.mod
%{_mandir}/%{namearch}/man1/mpi[cCf]*
%{_mandir}/%{namearch}/man1/opal_*
%{_mandir}/%{namearch}/man3/*
%{_mandir}/%{namearch}/man7/opal*
%{_libdir}/%{libname}/share/openmpi/openmpi-valgrind.supp
%{_libdir}/%{libname}/share/openmpi/mpi*.txt
%{_libdir}/%{libname}/share/vampirtrace/*
%{_sysconfdir}/rpm/macros.%{namearch}
%endif

%global variant compat-openmpi
%global libname %{variant}%{?_cc_name_suffix}
%global namearch %{variant}-%{_arch}%{?_cc_name_suffix}

%files -n openmpi-1.5.3%{?_cc_name_suffix}
%dir %{_libdir}/%{libname}
%dir %{_sysconfdir}/%{namearch}
%dir %{_sysconfdir}/openmpi-1.5.3-%{_arch}%{?_cc_name_suffix}
%dir %{_libdir}/%{libname}/bin
%dir %{_libdir}/%{libname}/lib
%dir %{_libdir}/%{libname}/lib/openmpi
%dir %{_mandir}/%{namearch}
%dir %{_mandir}/%{namearch}/man*
%dir %{_fmoddir}/%{namearch}
%dir %{python_sitearch}/%{libname}
%config(noreplace) %{_sysconfdir}/%{namearch}/*
%{_libdir}/%{libname}/bin/mpi[er]*
%{_libdir}/%{libname}/bin/ompi*
#%{_libdir}/%{libname}/bin/opal-*
%{_libdir}/%{libname}/bin/opari
%{_libdir}/%{libname}/bin/orte*
%{_libdir}/%{libname}/bin/otf*
%{_libdir}/%{libname}/lib/*.so.*
%{_mandir}/%{namearch}/man1/mpi[er]*
%{_mandir}/%{namearch}/man1/ompi*
#%{_mandir}/%{namearch}/man1/opal-*
%{_mandir}/%{namearch}/man1/orte*
%{_mandir}/%{namearch}/man7/ompi*
%{_mandir}/%{namearch}/man7/orte*
%{_libdir}/%{libname}/lib/openmpi/*
%{_sysconfdir}/modulefiles/%{namearch}
%{_sysconfdir}/modulefiles/openmpi-1.5.3-%{_arch}%{?_cc_name_suffix}
%dir %{_libdir}/%{libname}/share
%dir %{_libdir}/%{libname}/share/openmpi
%{_libdir}/%{libname}/share/openmpi/doc
%{_libdir}/%{libname}/share/openmpi/amca-param-sets
%{_libdir}/%{libname}/share/openmpi/help*.txt
%{_libdir}/%{libname}/share/openmpi/mca-btl-openib-device-params.ini

%files -n openmpi-1.5.3%{?_cc_name_suffix}-devel
%dir %{_includedir}/%{namearch}
%dir %{_libdir}/%{libname}/share/vampirtrace
%{_libdir}/%{libname}/bin/mpi[cCf]*
%{_libdir}/%{libname}/bin/vt*
%{_libdir}/%{libname}/bin/opal_*
%{_includedir}/%{namearch}/*
%{_libdir}/%{libname}/lib/*.so
%{_libdir}/%{libname}/lib/lib*.a
%{_libdir}/%{libname}/lib/mpi.mod
%{_mandir}/%{namearch}/man1/mpi[cCf]*
%{_mandir}/%{namearch}/man1/opal_*
%{_mandir}/%{namearch}/man3/*
%{_mandir}/%{namearch}/man7/opal*
%{_libdir}/%{libname}/share/openmpi/openmpi-valgrind.supp
%{_libdir}/%{libname}/share/openmpi/mpi*.txt
%{_libdir}/%{libname}/share/openmpi/orte*.txt
%{_libdir}/%{libname}/share/vampirtrace/*
%{_sysconfdir}/rpm/macros.%{namearch}

%ifarch x86_64
%global variant compat-openmpi-psm
%global libname %{variant}%{?_cc_name_suffix}
%global namearch %{variant}-%{_arch}%{?_cc_name_suffix}

%files -n openmpi-1.5.3-psm%{?_cc_name_suffix}
%dir %{_libdir}/%{libname}
%dir %{_sysconfdir}/%{namearch}
%dir %{_sysconfdir}/openmpi-1.5.3-psm-%{_arch}%{?_cc_name_suffix}
%dir %{_libdir}/%{libname}/bin
%dir %{_libdir}/%{libname}/lib
%dir %{_libdir}/%{libname}/lib/openmpi
%dir %{_mandir}/%{namearch}
%dir %{_mandir}/%{namearch}/man*
%dir %{_fmoddir}/%{namearch}
%dir %{python_sitearch}/%{libname}
%config(noreplace) %{_sysconfdir}/%{namearch}/*
%{_libdir}/%{libname}/bin/mpi[er]*
%{_libdir}/%{libname}/bin/ompi*
#%{_libdir}/%{libname}/bin/opal-*
%{_libdir}/%{libname}/bin/opari
%{_libdir}/%{libname}/bin/orte*
%{_libdir}/%{libname}/bin/otf*
%{_libdir}/%{libname}/lib/*.so.*
%{_mandir}/%{namearch}/man1/mpi[er]*
%{_mandir}/%{namearch}/man1/ompi*
#%{_mandir}/%{namearch}/man1/opal-*
%{_mandir}/%{namearch}/man1/orte*
%{_mandir}/%{namearch}/man7/ompi*
%{_mandir}/%{namearch}/man7/orte*
%{_libdir}/%{libname}/lib/openmpi/*
%{_sysconfdir}/modulefiles/%{namearch}
%{_sysconfdir}/modulefiles/openmpi-1.5.3-psm-%{_arch}%{?_cc_name_suffix}
%dir %{_libdir}/%{libname}/share
%dir %{_libdir}/%{libname}/share/openmpi
%{_libdir}/%{libname}/share/openmpi/doc
%{_libdir}/%{libname}/share/openmpi/amca-param-sets
%{_libdir}/%{libname}/share/openmpi/help*.txt
%{_libdir}/%{libname}/share/openmpi/mca-btl-openib-device-params.ini

%files -n openmpi-1.5.3-psm%{?_cc_name_suffix}-devel
%dir %{_includedir}/%{namearch}
%dir %{_libdir}/%{libname}/share/vampirtrace
%{_libdir}/%{libname}/bin/mpi[cCf]*
%{_libdir}/%{libname}/bin/vt*
%{_libdir}/%{libname}/bin/opal_*
%{_includedir}/%{namearch}/*
%{_libdir}/%{libname}/lib/*.so
%{_libdir}/%{libname}/lib/lib*.a
%{_libdir}/%{libname}/lib/mpi.mod
%{_mandir}/%{namearch}/man1/mpi[cCf]*
%{_mandir}/%{namearch}/man1/opal_*
%{_mandir}/%{namearch}/man3/*
%{_mandir}/%{namearch}/man7/opal*
%{_libdir}/%{libname}/share/openmpi/openmpi-valgrind.supp
%{_libdir}/%{libname}/share/openmpi/mpi*.txt
%{_libdir}/%{libname}/share/openmpi/orte*.txt
%{_libdir}/%{libname}/share/vampirtrace/*
%{_sysconfdir}/rpm/macros.%{namearch}

%endif

%global variant openmpi-1.5.4
%global libname %{variant}%{?_cc_name_suffix}
%global namearch %{variant}-%{_arch}%{?_cc_name_suffix}

%files -n openmpi-1.5.4%{?_cc_name_suffix}
%dir %{_libdir}/%{libname}
%dir %{_sysconfdir}/%{namearch}
%dir %{_libdir}/%{libname}/bin
%dir %{_libdir}/%{libname}/lib
%dir %{_libdir}/%{libname}/lib/openmpi
%dir %{_mandir}/%{namearch}
%dir %{_mandir}/%{namearch}/man*
%dir %{_fmoddir}/%{namearch}
%dir %{python_sitearch}/%{libname}
%config(noreplace) %{_sysconfdir}/%{namearch}/*
%{_libdir}/%{libname}/bin/mpi[er]*
%{_libdir}/%{libname}/bin/ompi*
#%{_libdir}/%{libname}/bin/opal-*
%{_libdir}/%{libname}/bin/opari
%{_libdir}/%{libname}/bin/orte*
%{_libdir}/%{libname}/bin/otf*
%{_libdir}/%{libname}/lib/*.so.*
%{_mandir}/%{namearch}/man1/mpi[er]*
%{_mandir}/%{namearch}/man1/ompi*
#%{_mandir}/%{namearch}/man1/opal-*
%{_mandir}/%{namearch}/man1/orte*
%{_mandir}/%{namearch}/man7/ompi*
%{_mandir}/%{namearch}/man7/orte*
%{_libdir}/%{libname}/lib/openmpi/*
%{_sysconfdir}/modulefiles/%{namearch}
%dir %{_libdir}/%{libname}/share
%dir %{_libdir}/%{libname}/share/openmpi
%{_libdir}/%{libname}/share/openmpi/doc
%{_libdir}/%{libname}/share/openmpi/amca-param-sets
%{_libdir}/%{libname}/share/openmpi/help*.txt
%{_libdir}/%{libname}/share/openmpi/mca-btl-openib-device-params.ini

%files -n openmpi-1.5.4%{?_cc_name_suffix}-devel
%dir %{_includedir}/%{namearch}
%dir %{_libdir}/%{libname}/share/vampirtrace
%{_libdir}/%{libname}/bin/mpi[cCf]*
%{_libdir}/%{libname}/bin/vt*
%{_libdir}/%{libname}/bin/opal_*
%{_includedir}/%{namearch}/*
%{_libdir}/%{libname}/lib/*.so
%{_libdir}/%{libname}/lib/lib*.a
%{_libdir}/%{libname}/lib/mpi.mod
%{_mandir}/%{namearch}/man1/mpi[cCf]*
%{_mandir}/%{namearch}/man1/opal_*
%{_mandir}/%{namearch}/man3/*
%{_mandir}/%{namearch}/man7/opal*
%{_libdir}/%{libname}/share/openmpi/openmpi-valgrind.supp
%{_libdir}/%{libname}/share/openmpi/mpi*.txt
%{_libdir}/%{libname}/share/openmpi/orte*.txt
%{_libdir}/%{libname}/share/vampirtrace/*
%{_sysconfdir}/rpm/macros.%{namearch}

%global variant openmpi
%global libname %{variant}%{?_cc_name_suffix}
%global namearch %{variant}-%{_arch}%{?_cc_name_suffix}

%files -n openmpi-1.8%{?_cc_name_suffix}
%dir %{_libdir}/%{libname}
%dir %{_sysconfdir}/%{namearch}
%dir %{_sysconfdir}/openmpi-1.8-%{_arch}%{?_cc_name_suffix}
%dir %{_libdir}/%{libname}/bin
%dir %{_libdir}/%{libname}/lib
%dir %{_libdir}/%{libname}/lib/openmpi
%dir %{_mandir}/%{namearch}
%dir %{_mandir}/%{namearch}/man*
%dir %{_fmoddir}/%{namearch}
%dir %{python_sitearch}/%{libname}
%config(noreplace) %{_sysconfdir}/%{namearch}/*
%{_libdir}/%{libname}/bin/mpi[er]*
%{_libdir}/%{libname}/bin/ompi*
%{_libdir}/%{libname}/bin/opari
%{_libdir}/%{libname}/bin/orte[-dr_]*
%{_libdir}/%{libname}/bin/oshmem_info
%{_libdir}/%{libname}/bin/oshrun
%{_libdir}/%{libname}/bin/otf*
%{_libdir}/%{libname}/bin/shmemrun
%{_libdir}/%{libname}/lib/*.so.*
%{_mandir}/%{namearch}/man1/mpi[er]*
%{_mandir}/%{namearch}/man1/ompi*
%{_mandir}/%{namearch}/man1/orte[-dr_]*
%{_mandir}/%{namearch}/man1/oshmem_info*
%{_mandir}/%{namearch}/man7/ompi*
%{_mandir}/%{namearch}/man7/orte*
%{_libdir}/%{libname}/lib/openmpi/*
%{_sysconfdir}/modulefiles/%{namearch}
%{_sysconfdir}/modulefiles/openmpi-1.8-%{_arch}%{?_cc_name_suffix}
%dir %{_libdir}/%{libname}/share
%dir %{_libdir}/%{libname}/share/openmpi
%{_libdir}/%{libname}/share/openmpi/doc
%{_libdir}/%{libname}/share/openmpi/amca-param-sets
%{_libdir}/%{libname}/share/openmpi/help*.txt
%{_libdir}/%{libname}/share/openmpi/mca-btl-openib-device-params.ini
%{_libdir}/%{libname}/share/openmpi/mca-coll-ml.config

%files -n openmpi-1.8%{?_cc_name_suffix}-devel
%dir %{_includedir}/%{namearch}
%dir %{_libdir}/%{libname}/share/vampirtrace
%{_libdir}/%{libname}/bin/mpi[cCf]*
%{_libdir}/%{libname}/bin/opal_*
%{_libdir}/%{libname}/bin/orte[cCf]*
%{_libdir}/%{libname}/bin/osh[cf]*
%{_libdir}/%{libname}/bin/shmem[cf]*
%{_libdir}/%{libname}/bin/vt*
%{_includedir}/%{namearch}/*
%{_libdir}/%{libname}/lib/*.so
%{_libdir}/%{libname}/lib/lib*.a
%{_libdir}/%{libname}/lib/mpi.mod
%{_mandir}/%{namearch}/man1/mpi[cCf]*
%{_mandir}/%{namearch}/man1/opal_*
%{_mandir}/%{namearch}/man3/*
%{_mandir}/%{namearch}/man7/opal*
%{_libdir}/%{libname}/share/openmpi/openmpi-valgrind.supp
%{_libdir}/%{libname}/share/openmpi/*-wrapper-data.txt
%{_libdir}/%{libname}/share/vampirtrace/*
%{_sysconfdir}/rpm/macros.%{namearch}

%changelog
* Wed Jan 27 2016 Michal Schmidt <mschmidt@redhat.com> 1.4.3-5
- Rename compat-openmpiXY to openmpi-X.Y. Package names, directories,
  modulefiles.
- Ship multiple openmpi versions:
  - openmpi-1.4   (compat with RHEL 6.0, 6.1)
  - openmpi-1.5.3 (compat with RHEL 6.2)
  - openmpi-1.5.4 (compat with RHEL 6.3, 6.4, 6.5)
  - openmpi-1.8   (compat with RHEL 6.6, 6.7)
- Avoid breakage in transition from the compat-openmpi package from RHEL 6.7
  (was versioned as 1.4.3, but was in fact a chimera of 1.4.3 and 1.5.3,
   where really only 1.5.3 had any chance of working) by keeping the
  "compat-openmpi", "compat-openmpi-$arch" directory and module names
  for openmpi-1.5.3.
- openmpi-1.8 keeps the module and directory unversioned names "openmpi",
  "openmpi-$arch" it had in RHEL 6.7.
- Related: rhbz1158864

* Tue Jan 19 2016 Michal Schmidt <mschmidt@redhat.com> 1.4.3-2
- Split into subpackages per OpenMPI version (compat-openmpi14,
  compat-openmpi15)
- Add compat-openmpi18.
- Resolves: rhbz1158864, rhbz1142157

* Tue Jun 3 2014 Jay Fenlason <fenlason@redhat.com> 1.4.3-1.2
- Don't bother passing in options that the 1.4.3 configure doesn't
  understand.
- set XFLAGS on all archs, not just x86_64.
- Copy requires/provides filtering from openmpi so this will stop
  providing libotf.so.0
  Resolves: rhbz1097290

* Wed Aug 14 2013 Jay Fenlason <fenlason@redhat.com> 1.4.3-1.1
* Also include 1.5.3 libraries so users of RHEL-6.5+ can run
  programs compiled on RHEL-6.2-
  Resolves: rhbz876315

* Thu Oct 13 2011 Jay Fenlason <fenlason@redhat.com> 1.4.3-1
- New compat package to make users of openmpi-1.4 on RHEL-6 happy.
  Resolves: rhbz741009