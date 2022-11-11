# SPDX-License-Identifier: BSD-3-Clause
# (c) Copyright 2014,2022 Advanced Micro Devices, Inc.

Name: sfptpd
Version: %{pkgversion}
Release: 1%{?dist}
Summary: Solarflare Enhanced PTP Daemon
License: BSD
Group: System Environment/Daemons
Source0: sfptpd-%{version}.tgz
URL: https://www.xilinx.com/download/drivers
Vendor: Advanced Micro Devices, Inc.
BuildRequires: gcc
BuildRequires: make
BuildRoot: %{_tmppath}/%{name}-%{version}-root

%define pkgdocdir %{_defaultdocdir}/%{name}-%{version}

%description
This package provides the Xilinx 'sfptpd' daemon which implements PTP
(IEEE 1588-2019) over UDP, synchronizes to PPS signals received by
supported Ethernet controllers and performs local clock synchronization.
The application manages multiple time sources and bonded interfaces.

%prep
%autosetup
sed -i 's,^\(#define SFPTPD_VERSION_TEXT *"\).*",\1%{version}",g' src/include/sfptpd_version.h

find -iregex '.*\.py' | xargs sed -i -r '1s,^(#!.*)python3,\1python2,'

%build
make %{?_smp_mflags} sfptpd sfptpdctl

%install
export CC='false # no compilation at installation stage #'
export PACKAGE_NAME=%{name}
export INST_SBINDIR=%{buildroot}%{_sbindir}
export INST_DOCDIR=%{buildroot}%{_defaultdocdir}
export INST_MANDIR=%{buildroot}%{_mandir}
export INST_CONFDIR=%{buildroot}%{_sysconfdir}
export INST_UNITDIR=%{buildroot}%{_unitdir}
export INST_PKGDOCDIR=%{buildroot}%{pkgdocdir}
export INST_PKGLICENSEDIR=$INST_PKGDOCDIR
export INST_OMIT=""
export INST_INITS="sysv"
rm -rf $RPM_BUILD_ROOT
%make_install

%files
%defattr(-, root, root, -)
%attr(755, root, root) %{_sbindir}/sfptpd
%attr(755, root, root) %{_sbindir}/sfptpdctl
%attr(755, root, root) %{_sysconfdir}/init.d/sfptpd
%attr(644, root, root) %config(noreplace) %{_sysconfdir}/sfptpd.conf
%attr(644, root, root) %config(noreplace) %{_sysconfdir}/sysconfig/sfptpd
%doc %{pkgdocdir}/LICENSE
%doc %{pkgdocdir}/PTPD2_COPYRIGHT
%doc %{pkgdocdir}/NTP_COPYRIGHT.html
%doc %{pkgdocdir}/examples
%doc %{pkgdocdir}/config
%{_mandir}/man8/*.8*

%clean
rm -rf $RPM_BUILD_ROOT

%changelog
* Wed Nov  9 2022 Andrew Bower <andrew.bower@amd.com> - 3.6.0.1009~1-1
- use buildroot macro, fast_test target and sysconfig options

* Wed Oct 26 2022 Andrew Bower <andrew.bower@amd.com> - 3.6.0.1008-1
- release candidate

* Mon Sep  5 2022 Andrew Bower <andrew.bower@amd.com>
- various updates
- separated packaging definitions from source repo

* Mon Jul 14 2014 Laurence Evans
- initial rpm packaging capability
