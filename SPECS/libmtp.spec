# SPEC file for libmtp, primary target is the Fedora
# RPM repository.

Name:           libmtp
Version:        1.1.18
Release:        6%{?dist}
Summary:        Software library for MTP media players
URL:            http://libmtp.sourceforge.net/

Source0:        https://download.sourceforge.net/%{name}/%{name}-%{version}.tar.gz
License:        LGPLv2+
Requires:       udev
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  pkgconfig(libusb-1.0)
BuildRequires:  doxygen
%if ! 0%{?rhel}
BuildRequires:  libgcrypt-devel
%endif
BuildRequires:  chrpath

Patch0:         0001-doc-Don-t-document-internal-endian-macros.patch

%description
This package provides a software library for communicating with MTP
(Media Transfer Protocol) media players, typically audio players, video
players etc.

%package examples
Summary:        Example programs for libmtp
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description examples
This package provides example programs for communicating with MTP
devices.

%package devel
Summary:        Development files for libmtp
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
This package provides development files for the libmtp
library for MTP media players.

%prep
%setup -q
%patch0 -p1

%build
%configure --disable-static \
           --with-udev-rules=69-libmtp.rules \
%if 0%{?rhel}
           --disable-mtpz \
%endif
            %{nil}
%make_build

%install
%make_install
# Remove libtool archive remnant
rm -f $RPM_BUILD_ROOT%{_libdir}/libmtp.la
# Replace links with relative links
rm -f $RPM_BUILD_ROOT%{_bindir}/mtp-delfile
rm -f $RPM_BUILD_ROOT%{_bindir}/mtp-getfile
rm -f $RPM_BUILD_ROOT%{_bindir}/mtp-newfolder
rm -f $RPM_BUILD_ROOT%{_bindir}/mtp-sendfile
rm -f $RPM_BUILD_ROOT%{_bindir}/mtp-sendtr
pushd $RPM_BUILD_ROOT%{_bindir}
ln -sf mtp-connect mtp-delfile
ln -sf mtp-connect mtp-getfile
ln -sf mtp-connect mtp-newfolder
ln -sf mtp-connect mtp-sendfile
ln -sf mtp-connect mtp-sendtr
popd
# Convert COPYING file to UTF-8
iconv -f iso-8859-1 -t utf-8 -o COPYING.utf8 COPYING
touch -r COPYING COPYING.utf8; mv -f COPYING.utf8 COPYING
# Copy documentation to a good place
mkdir -p -m 755 $RPM_BUILD_ROOT%{_pkgdocdir}
install -p -m 644 AUTHORS README TODO \
      $RPM_BUILD_ROOT%{_pkgdocdir}
# Move some autogenerated documentation where we want it
if [ $RPM_BUILD_ROOT/usr/share/doc/%{name}-%{version}/html != $RPM_BUILD_ROOT%{_pkgdocdir}/html ] ; then \
	mv $RPM_BUILD_ROOT/usr/share/doc/%{name}-%{version}/html \
		$RPM_BUILD_ROOT%{_pkgdocdir} ; \
fi
# Touch generated files to make them always have the same time stamp.
touch -r configure.ac \
      $RPM_BUILD_ROOT%{_includedir}/*.h \
      $RPM_BUILD_ROOT%{_libdir}/pkgconfig/*.pc
# Get rid of -rpath
chrpath --delete $RPM_BUILD_ROOT{%{_bindir},/usr/lib/udev}/mtp*

%ldconfig_scriptlets

%files
%license COPYING
%{_libdir}/libmtp.so.9*
/usr/lib/udev/rules.d/69-libmtp.rules
/usr/lib/udev/hwdb.d/69-libmtp.hwdb
/usr/lib/udev/mtp-probe

%files examples
%{_bindir}/mtp-*

%files devel
%{_libdir}/libmtp.so
%{_pkgdocdir}
%{_includedir}/libmtp.h
%{_libdir}/pkgconfig/libmtp.pc

%changelog
* Fri Jan 21 2022 Ondrej Holy <oholy@redhat.com> - 1.1.18-6
- Ship libmtp-devel in CRB (#2026310)

* Mon Aug 09 2021 Mohan Boddu <mboddu@redhat.com> - 1.1.18-5
- Rebuilt for IMA sigs, glibc 2.34, aarch64 flags
  Related: rhbz#1991688

* Wed May 26 2021 Ondrej Holy <oholy@redhat.com> - 1.1.18-4
- Drop redundant devel requires
- Disable MTPZ support in RHEL
- Use pkgconfig for libusb

* Fri Apr 16 2021 Mohan Boddu <mboddu@redhat.com> - 1.1.18-3
- Rebuilt for RHEL 9 BETA on Apr 15th 2021. Related: rhbz#1947937

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.18-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jan 05 2021 Robert Scheck <robert@fedoraproject.org> - 1.1.18-1
- Upgrade to 1.1.18

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.16-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.16-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.16-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.16-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Nov 16 2018 Linus Walleij <linus.ml.walleij@gmail.com> - 1.1.16
+ libmtp-1.1.16-1
- New upstream release 1.1.16.
- Suddenly reappear doing package maintenance duties.

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.14-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.14-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sat Feb 03 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 1.1.14-2
- Switch to %%ldconfig_scriptlets

* Mon Oct 09 2017 Bastien Nocera <bnocera@redhat.com> - 1.1.14-1
+ libmtp-1.1.14-1
- Update to 1.1.14

* Mon Oct 09 2017 Bastien Nocera <bnocera@redhat.com> - 1.1.13-7
+ libmtp-1.1.13-7
- Fix multilib conflicts in host specific internal header

* Wed Sep 06 2017 Bastien Nocera <bnocera@redhat.com> - 1.1.13-6
+ libmtp-1.1.13-5
- Fix build on EPEL7 where the doc directory is versioned

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.13-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Mon Jul 31 2017 Florian Weimer <fweimer@redhat.com> - 1.1.13-4
- Rebuild with binutils fix for ppc64le (#1475636)

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.13-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Jul 10 2017 Dominik Mierzejewski <dominik@greysector.net> - 1.1.13-2
- Use https source URL
- Drop obsolete spec elements
- Use license macro
- Update libusbx-devel build dependency
- Drop ancient (F15) Obsoletes:
- Tighten file list

* Tue Jun 27 2017 Robert Scheck <robert@fedoraproject.org> - 1.1.13-1
- Update to 1.1.13 (#1412546, #1465038, #1465040)

* Mon Jun 26 2017 Debarshi Ray <rishi@fedoraproject.org> - 1.1.12-1
- Update to 1.1.12

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.11-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sun Jun 12 2016 Linus Walleij <triad@dflund.se> - 1.1.11-1
- Update to 1.1.11
- New upstream version with many fixes and additional devices
- Notably Nexus 6P is fixed to work in this release

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Dec 29 2015 Robert Scheck <robert@fedoraproject.org> - 1.1.10-1
- Update to 1.1.10

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon May 11 2015 Linus Walleij <triad@df.lth.se> - 1.1.9-1
- New upstream version with many fixes.
- Require libgrypt-devel to build, build libmtpz.
- Install hwdb file.
- Move documentation to a good place.

* Tue Aug 26 2014 Linus Walleij <triad@df.lth.se> - 1.1.8-1
- Get the bug fix below from upstream instead.

* Tue Aug 26 2014 Linus Walleij <triad@df.lth.se> - 1.1.7-2
- Fix an include problem. Or try to.

* Sun Aug 24 2014 Linus Walleij <triad@df.lth.se> - 1.1.7-1
- New upstream version.

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.6-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Aug  7 2013 Ville Skyttä <ville.skytta@iki.fi> - 1.1.6-2
- Install docs to %%{_pkgdocdir} where available.
- Move license file to main package.
- Fix bogus dates in %%changelog.

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.6-1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Mar 15 2013 Linus Walleij <triad@df.lth.se> 1.1.6-0
- New upstream version, several bug fixes, apropriate for GVFS etc.

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Oct 17 2012 Linus Walleij <triad@df.lth.se> 1.1.5-2
- Explicit disable MTPZ for now.

* Thu Sep 13 2012 Linus Walleij <triad@df.lth.se> 1.1.5-1
- New upstream version with several bug fixes.

* Sat Aug 18 2012 Linus Walleij <triad@df.lth.se> 1.1.4-1
- New upstream version with several bug fixes.

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Apr 03 2012 Linus Walleij <triad@df.lth.se> 1.1.3-2
- Use libusb-1.0 for sure, come on.

* Tue Apr 03 2012 Linus Walleij <triad@df.lth.se> 1.1.3-1
- Upstream update with several bug fixes including Fedora patch

* Sat Jan 28 2012 Linus Walleij <triad@df.lth.se> 1.1.2-2
- Bugfix to avoid probing Canon scanners

* Thu Jan 12 2012 Linus Walleij <triad@df.lth.se> 1.1.2-1
- Upstream update to use libusb-1.0 and other fixes.

* Thu Nov 10 2011 Linus Walleij <triad@df.lth.se> 1.1.1-2
- Add an Obsoletes: libmtp-hal so that users can upgrade from F15

* Sat Oct 22 2011 Linus Walleij <triad@df.lth.se> 1.1.1-1
- New upstream version fixing problems with a few color devices
  plus adding new device support. Move udev rules from level
  60 to level 69 to come after SANE and avoid probing these
  devices.

* Fri Jun 10 2011 Rex Dieter <rdieter@fedoraproject.org> 1.1.0-2
- %%files: track abi/soname, so bumps aren't a surprise

* Wed Jun 08 2011 Linus Walleij <triad@df.lth.se> 1.1.0-1
- New upstream version including fixed bugs and the patch we
  used to carry. Dependecies need to be rebuilt. (New
  soversion)

* Tue Jun 07 2011 Linus Walleij <triad@df.lth.se> 1.0.6-3
- Nuke HAL dependency.

* Fri Apr 01 2011 Linus Walleij <triad@df.lth.se> 1.0.6-2
- Maybe fixing a probing issue on an input device.

* Sat Feb 12 2011 Linus Walleij <triad@df.lth.se> 1.0.6-1
- New upstream release fixing bugs & more things we patched.

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Feb 5 2011 Linus Walleij <triad@df.lth.se> 1.0.5-1
- New upstream release fixing all the things we patched.

* Mon Jan 24 2011 Linus Walleij <triad@df.lth.se> 1.0.4-3
- Screwed up boolean logic in last patch, fixing it.

* Wed Jan 19 2011 Linus Walleij <triad@df.lth.se> 1.0.4-2
- Testing out a patch to be more careful when probing devices.

* Sun Jan 9 2011 Linus Walleij <triad@df.lth.se> 1.0.4-1
- New upstream version with mucho udev fixes.

* Wed Dec 1 2010 Linus Walleij <triad@df.lth.se> 1.0.3-7
- Now even with correct commas and stuff in udev actions.

* Tue Nov 30 2010 Linus Walleij <triad@df.lth.se> 1.0.3-6
- It appears adding ENV{ID_MTP_DEVICE}="1",
  ENV{ID_MEDIA_PLAYER}="1" is the way forward so testing this
  before pushing a new libmtp release.

* Thu Jun 17 2010 Bastien Nocera <bnocera@redhat.com> 1.0.3-5
- Split out hal sub-package

* Thu Jun 10 2010 Linus Walleij <triad@df.lth.se> 1.0.3-4
- Set ENV{ACL_MANAGE}="0" and TAG+="udev-acl" akin to rfkill
  apparently this may be an interrim solution.

* Sat Jun 05 2010 Linus Walleij <triad@df.lth.se> 1.0.3-3
- Remove ENV{ACL_MANAGE} after Bastiens bug report.

* Tue May 25 2010 Linus Walleij <triad@df.lth.se> 1.0.3-2
- Replace hal-filesystem dependence with hal-info
  We can remove this altogether once all apps are cleansed
  from HAL.

* Sun May 23 2010 Linus Walleij <triad@df.lth.se> 1.0.3-1
- New upstream version, bug fixes.

* Wed Feb 3 2010 Linus Walleij <triad@df.lth.se> 1.0.2-1
- New upstream version, lots of bug fixes.

* Wed Jan 20 2010 Bastien Nocera <bnocera@redhat.com> 1.0.1-3
- Require hal-filesystem, instead of HAL

* Tue Dec 1 2009 Linus Walleij <triad@df.lth.se> 1.0.1-2
- Two patches from Dan Nicholson to fix up the udev rules a bit.

* Sat Sep 12 2009 Linus Walleij <triad@df.lth.se> 1.0.1-1
- New upstream release. No interface changes!

* Tue Aug 4 2009 Linus Walleij <triad@df.lth.se> 1.0.0-1
- New upstream release. Dependent packages need to be rebuilt against this.

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Mar 17 2009 Linus Walleij <triad@df.lth.se> 0.3.7-1
- New upstream bugfix release.

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Jan 22 2009 Linus Walleij <triad@df.lth.se> 0.3.6-1
- New upstream bugfix release.

* Sun Dec 21 2008 Linus Walleij <triad@df.lth.se> 0.3.5-1
- New upstream bugfix release.
- Nuke documentation again. Multilib no like.

* Fri Nov 7 2008 Linus Walleij <triad@df.lth.se> 0.3.4-1
- New upstream bugfix release.
- Bastiens patch is upstreamed, dropping that patch.

* Sat Oct 25 2008 - Bastien Nocera <bnocera@redhat.com> - 0.3.3-4
- Update device list from CVS and fix the build

* Sat Oct 25 2008 - Bastien Nocera <bnocera@redhat.com> - 0.3.3-3
- Add support for more Nokia phones from their WMP10 drivers

* Fri Oct 24 2008 - Bastien Nocera <bnocera@redhat.com> - 0.3.3-2
- Add support for the Nokia N82

* Fri Sep 26 2008 Linus Walleij <triad@df.lth.se> 0.3.3-1
- New upstream bugfix release.

* Sat Sep 20 2008 Linus Walleij <triad@df.lth.se> 0.3.2-1
- New upstream version. (API and ABI compatible.) Fixes
  bugs on Creative devices.

* Tue Aug 26 2008 Linus Walleij <triad@df.lth.se> 0.3.1-1
- New upstream version. (API and ABI compatible.)

* Thu Aug 7 2008 Linus Walleij <triad@df.lth.se> 0.3.0-1
- Upgrade to 0.3.0. This has to happen some way, perhaps the
  painful way: I upgrade to gnomad2 2.9.2 that use 0.3.0 and
  then I write patches to Rhythmbox and Amarok to use 0.3.0
  and also send these upstream.

* Fri Jul 11 2008 Linus Walleij <triad@df.lth.se> 0.2.6.1-3
- Loose PAM console permissions, also assume that we can ship
  documentation again since Doxygen has been updated. Fedora
  HALd rules for the portable_audio_player capability in
  20-acl-management.fdi will change permissions on the device
  node for each plugged-in device.

* Fri May 23 2008 Adam Jackson <ajax@redhat.com> 0.2.6.1-2
- libmtp-0.2.6.1-simpler-rules.patch: Simplify udev rules for faster bootup.

* Sat Mar 8 2008 Linus Walleij <triad@df.lth.se> 0.2.6.1-1
- New upstream bugfix release.

* Sun Mar 2 2008 Linus Walleij <triad@df.lth.se> 0.2.6-1
- New upstream release.

* Sat Feb 9 2008 Linus Walleij <triad@df.lth.se> 0.2.5-2
- Rebuild for GCC 4.3.

* Wed Jan 9 2008 Linus Walleij <triad@df.lth.se> 0.2.5-1
- New upstream release.

* Thu Nov 22 2007 Linus Walleij <triad@df.lth.se> 0.2.4-1
- New upstream release.

* Thu Oct 25 2007 Linus Walleij <triad@df.lth.se> 0.2.3-1
- New upstream release.
- New soname libmtp.so.7 so all apps using libmtp have to
  be recompiled, have fun.
- If it works out we'll try to reserve a spot to backport
  this fixed version to F8 and F7 in a controlled manner.

* Wed Oct 24 2007 Linus Walleij <triad@df.lth.se> 0.2.2-2
- Flat out KILL the Doxygen HTML docs to resolve multiarch conflicts.
  Either upstream (that's me!) needs to work around the HTML files being
  different each time OR Doxygen must stop generating anchors that
  hash the system time, creating different files with each generation.
  Pre-generating the docs is deemed silly. (Someone will disagree.)

* Fri Aug 17 2007 Linus Walleij <triad@df.lth.se> 0.2.2-1
- New upstream release.

* Fri Aug 17 2007 Linus Walleij <triad@df.lth.se> 0.2.1-2
- License field update from LGPL to LGPLv2+

* Tue Aug 7 2007 Linus Walleij <triad@df.lth.se> 0.2.1-1
- Upstream bugfix release.

* Sat Aug 4 2007 Linus Walleij <triad@df.lth.se> 0.2.0-1
- New upstream release.
- Fixes (hopefully) the issues found by Harald.
- Dependent apps will need to recompile and patch some minor code.

* Mon Jul 30 2007 Harald Hoyer <harald@redhat.com> - 0.1.5-2
- changed udev rules for new kernel and udev versions

* Mon Mar 26 2007 Linus Walleij <triad@df.lth.se> 0.1.5-1
- New upstream release.
- Candidate for FC5, FC6 backport.
- Hopefully API/ABI compatible, testing in devel tree.

* Wed Mar 7 2007 Linus Walleij <triad@df.lth.se> 0.1.4-1
- New upstream release.
- Candidate for FC5, FC6 backport.
- Hopefully API/ABI compatible, testing in devel tree.

* Wed Jan 17 2007 Linus Walleij <triad@df.lth.se> 0.1.3-1
- New upstream release.
- Candidate for FC5, FC6 backport.

* Thu Dec 7 2006 Linus Walleij <triad@df.lth.se> 0.1.0-1
- New upstream release.
- Start providing HAL rules.

* Fri Oct 20 2006 Linus Walleij <triad@df.lth.se> 0.0.21-1
- New upstream release.

* Tue Sep 26 2006 Linus Walleij <triad@df.lth.se> 0.0.20-1
- New upstream release.
- Updated after review by Parag AN, Kevin Fenzi and Ralf Corsepius.
- Fixed pkgconfig bug upstream after being detected by Ralf...

* Sun Aug 27 2006 Linus Walleij <triad@df.lth.se> 0.0.15-1
- New upstream release.

* Wed Aug 23 2006 Linus Walleij <triad@df.lth.se> 0.0.13-1
- First RPM'ed
