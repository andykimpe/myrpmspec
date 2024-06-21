%if 0%{?rhel} >= 6
%global debug_package %{nil}
%endif

%global eclipse_base     %{_libdir}/eclipse
%global eclipse_dropin   %{_datadir}/eclipse/dropins

Name:      eclipse-birt
Version:   2.6.0
Release:   1.1%{?dist}
Summary:   Eclipse-based reporting system
Group:     System Environment/Libraries
License:   EPL
URL:       http://www.eclipse.org/birt/

# Generate Source0 using Source1
Source0:   %{name}-%{version}-fetched-src.tar.bz2
Source1:   fetch-birt.sh

# smil in Fedora is merged in xml-commons-apis-ext.jar, reflecting upstream changes
Patch0:    birt-remove-smil.patch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%if 0%{?rhel} >= 6
ExclusiveArch: i686 x86_64
%else
BuildArch: noarch
%endif

BuildRequires:    java-devel 
BuildRequires:    jpackage-utils
BuildRequires:    eclipse-pde >= 1:3.4.1
BuildRequires:    eclipse-dtp
BuildRequires:    eclipse-emf
BuildRequires:    eclipse-gef
BuildRequires:    rhino
BuildRequires:    batik >= 1.7-3
BuildRequires:    fop >= 0.95-2
BuildRequires:    jakarta-commons-codec >= 1.3-9.4
BuildRequires:    sac >= 1.3-3.3

Requires:         java
Requires:         jpackage-utils
Requires:         eclipse-platform >= 1:3.4.1
Requires:         eclipse-dtp
Requires:         eclipse-emf
Requires:         eclipse-gef
Requires:         rhino
Requires:         batik >= 1.7-3
Requires:         fop >= 0.95-2
Requires:         jakarta-commons-codec >= 1.3-9.4
Requires:         sac >= 1.3-3.3

%description
BIRT is an Eclipse-based open source reporting system for web applications,
especially those based on Java and J2EE. BIRT has two main components: 
a report designer based on Eclipse, and a runtime component that you 
can add to your app server. BIRT also offers a charting engine that lets 
you add charts to your own application. 

%prep
%setup -q 
%patch0
# make sure upstream hasn't snuck in any jars we don't know about
find -name "*.jar" -exec rm {} \; 

# symlink rhino in its plugin
pushd org.mozilla.rhino/lib
ln -s %{_javadir}/js.jar js.jar
popd

# symlink orbit deps
mkdir orbitDeps
pushd orbitDeps
ln -s %{_javadir}/commons-codec.jar org.apache.commons.codec_1.3.0.jar
ln -s %{_javadir}/batik/batik-bridge.jar 
ln -s %{_javadir}/batik/batik-css.jar 
ln -s %{_javadir}/batik/batik-dom.jar 
ln -s %{_javadir}/batik/batik-svg-dom.jar
ln -s %{_javadir}/batik/batik-awt-util.jar 
ln -s %{_javadir}/batik/batik-extension.jar 
ln -s %{_javadir}/batik/batik-parser.jar 
ln -s %{_javadir}/batik/batik-svggen.jar 
ln -s %{_javadir}/batik/batik-swing.jar 
ln -s %{_javadir}/batik/batik-transcoder.jar
ln -s %{_javadir}/batik/batik-gui-util.jar 
ln -s %{_javadir}/batik/batik-util.jar 
ln -s %{_javadir}/batik/batik-xml.jar 
ln -s %{_javadir}/xml-commons-apis-ext.jar
ln -s %{_javadir}/fop.jar
ln -s %{_javadir}/sac.jar
popd

%build
# build only chart feature until dependencies (full dtp and wtp) are ready
%{eclipse_base}/buildscripts/pdebuild -f org.eclipse.birt.chart \
                       -d "emf gef dtp-enablement dtp-connectivity dtp-modelbase dtp-sqldevtools" \
                       -o `pwd`/orbitDeps -v

%install
rm -rf %{buildroot}
install -d -m 755 %{buildroot}%{eclipse_dropin}
unzip -q -d %{buildroot}%{eclipse_dropin}/birt build/rpmBuild/org.eclipse.birt.chart.zip

pushd %{buildroot}%{eclipse_dropin}/birt/eclipse/plugins/org.mozilla.rhino_1.7.1.*/lib
rm -fr js.jar
ln -s ../../../../../../../java/js.jar
popd

pushd %{buildroot}%{eclipse_dropin}/birt/eclipse/plugins
rm -fr org.apache.batik.bridge_*.jar
ln -s ../../../../../java/batik/batik-bridge.jar
rm -fr org.apache.batik.css_*.jar
ln -s ../../../../../java/batik/batik-css.jar 
rm -fr org.apache.batik.dom_*.jar
ln -s ../../../../../java/batik/batik-dom.jar 
rm -fr org.apache.batik.dom.svg_*.jar
ln -s ../../../../../java/batik/batik-svg-dom.jar
rm -fr org.apache.batik.ext.awt_*.jar
ln -s ../../../../../java/batik/batik-awt-util.jar 
rm -fr org.apache.batik.parser_*.jar
ln -s ../../../../../java/batik/batik-parser.jar 
rm -fr org.apache.batik.pdf_*.jar
ln -s ../../../../../java/fop.jar
ln -s ../../../../../java/sac.jar
rm -fr org.apache.batik.svggen_*.jar
ln -s ../../../../../java/batik/batik-svggen.jar 
rm -fr org.apache.batik.transcoder_*.jar
ln -s ../../../../../java/batik/batik-transcoder.jar
rm -fr org.apache.batik.util_*.jar
ln -s ../../../../../java/batik/batik-util.jar 
rm -fr org.apache.batik.util.gui_*.jar
ln -s ../../../../../java/batik/batik-gui-util.jar 
rm -fr org.apache.batik.xml_*.jar
ln -s ../../../../../java/batik/batik-xml.jar 
rm -fr org.w3c*.jar
ln -s ../../../../../java/xml-commons-apis-ext.jar
rm -fr org.apache.commons.codec_*.jar
ln -s ../../../../../java/commons-codec.jar org.apache.commons.codec_1.3.0.jar
popd

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{eclipse_dropin}/birt
%doc features/org.eclipse.birt.chart.feature/license.html
%doc features/org.eclipse.birt.chart.feature/epl-v10.html

%changelog
* Thu Jan 13 2011 Alexander Kurtakov <akurtako@redhat.com> 2.6.0-1.1
- RHEL 6.1 rebase to Helios.

* Tue Aug 3 2010 Andrew Overholt <overholt@redhat.com> 2.6.0-1
- Update to 2.6.0.
- Build rhino plugin as part of BIRT chart feature.
- Remove unnecessary dependencies.

* Thu Mar 11 2010 Alexander Kurtakov <akurtako@redhat.com> 2.5.2-1
- Update to 2.5.2.

* Fri Feb 12 2010 Andrew Overholt <overholt@redhat.com> 2.5-1.2
- Don't build debuginfo if building arch-specific packages.

* Tue Dec  1 2009 Dennis Gregorovic <dgregor@redhat.com> - 2.5-1.1
- Only build on x86 and x86_64 since we only have eclipse on those arches

* Wed Aug 12 2009 Alexander Kurtakov <akurtako@redhat.com> 2.5-1
- Update to 2.5.0 final.

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.5-0.2.M7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed May 27 2009 Alexander Kurtakov <akurtako@redhat.com> 2.5-0.1.M7
- Update to 2.5.0 Milestone 7.
- Remove patch1 - merged upstream.
- Use %%global.

* Mon Mar 23 2009 Alexander Kurtakov <akurtako@redhat.com> 2.3.2-2
- Rebuild to not ship p2 context.xml.

* Fri Feb 27 2009 Alexander Kurtakov <akurtako@redhat.com> 2.3.2-1
- Update to 2.3.2.
- Add compile fix for our rhino.

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Feb 13 2009 Alexander Kurtakov <akurtako@redhat.com> 2.3.1-2
- Fix max line to 80 symbols where possible.
- Add more comments.
- Clarify rhinoqualifier.

* Fri Feb 13 2009 Alexander Kurtakov <akurtako@redhat.com> 2.3.1-1
- Initial packaging.
