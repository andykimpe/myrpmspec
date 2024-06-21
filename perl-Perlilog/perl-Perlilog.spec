Name:           perl-Perlilog
Version:        0.3
Release:        4%{?dist}
Summary:        Verilog environment and IP core handling in Perl
License:        GPLv2
Group:          Development/Libraries
URL:            http://search.cpan.org/dist/Perlilog/
Source0:        http://www.cpan.org/authors/id/B/BI/BILLAUER/Perlilog-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  perl(ExtUtils::MakeMaker)
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%description
Perlilog is a command-line tool which generates Verilog
modules from a set of files, which come in several other
formats. It was originally designed to integrate Verilog IP cores.

%prep
%setup -q -n Perlilog-%{version}

# rpmlint : line endings
affected=`find examples/ -type f -name "*.*"`
for i in license.txt $affected ; do
  echo "Fixing wrong-file-end-of-line-encoding : $i"
  %{__sed} 's/\r//' $i > $i.rpmlint
  touch -r $i $i.rpmlint;
  %{__mv} $i.rpmlint $i
done

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT

make pure_install PERL_INSTALL_ROOT=$RPM_BUILD_ROOT

find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} \;
find $RPM_BUILD_ROOT -depth -type d -exec rmdir {} 2>/dev/null \;

%{_fixperms} $RPM_BUILD_ROOT/*

%check
make test

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc Changes license.txt
%doc examples/
%dir %{perl_vendorlib}/Perlilog
%{perl_vendorlib}/Perlilog/*
%{perl_vendorlib}/testclass.pl
%{perl_vendorlib}/Perlilog.pm
%{_mandir}/man3/*

%changelog
* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 0.3-4
- rebuild against perl 5.10.1

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sun Dec 14 2008 Chitlesh GOORAH <chitlesh [AT] fedoraproject DOT org> 0.3-1
- Specfile autogenerated by cpanspec 1.77.