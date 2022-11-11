# SPDX-License-Identifier: BSD-3-Clause
# (c) Copyright 2014,2022 Advanced Micro Devices, Inc.

Name: sfptpd
Version: %{pkgversion}
Release: 1
Summary: Solarflare Enhanced PTP Daemon
License: BSD
Group: System Environment/Daemons
Source0: sfptpd-%{version}.tgz
URL: https://www.xilinx.com/download/drivers
Vendor: Advanced Micro Devices, Inc.
BuildRequires: gcc
BuildRequires: make
BuildRequires: systemd-rpm-macros

%description
This package provides the Xilinx 'sfptpd' daemon which implements PTP
(IEEE 1588-2019) over UDP, synchronizes to PPS signals received by
supported Ethernet controllers and performs local clock synchronization.
The application manages multiple time sources and bonded interfaces.

%prep
%autosetup
sed -i 's,^\(#define SFPTPD_VERSION_TEXT *"\).*",\1%{version}",g' src/include/sfptpd_version.h

%build
%make_build

%install
export CC='false # no compilation at installation stage #'
export PACKAGE_NAME=%{name}
export INST_SBINDIR=%{buildroot}%{_sbindir}
export INST_DOCDIR=%{buildroot}%{_docdir}
export INST_MANDIR=%{buildroot}%{_mandir}
export INST_CONFDIR=%{buildroot}%{_sysconfdir}
export INST_UNITDIR=%{buildroot}%{_unitdir}
export INST_PKGDOCDIR=%{buildroot}%{_pkgdocdir}
export INST_OMIT="license"
export INST_INITS="systemd"
%make_install

%check
make fast_test

%post
%systemd_post %{name}.service

%preun
%systemd_preun %{name}.service

%postun
%systemd_postun_with_restart %{name}.service

%files
%attr(755, root, root) %{_sbindir}/sfptpd
%attr(755, root, root) %{_sbindir}/sfptpdctl
%attr(644, root, root) %{_unitdir}/sfptpd.service
%attr(644, root, root) %config(noreplace) %{_sysconfdir}/sfptpd.conf
%attr(644, root, root) %config(noreplace) %{_sysconfdir}/sysconfig/sfptpd
%license LICENSE PTPD2_COPYRIGHT NTP_COPYRIGHT.html
%doc %{_pkgdocdir}
%{_mandir}/man8/*.8*

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
