# Spec file for building sfptpd source rpm
#
# SPDX-License-Identifier: BSD-3-Clause
#
# (c) Copyright 2014,2022 Advanced Micro Devices, Inc.

Name: sfptpd
Version: %{pkgversion}
Release: 1%{?dist}
Summary: Solarflare Enhanced PTP Daemon
License: BSD
Group: System Environment/Daemons
Source0: sfptpd-%{version}.tgz
URL: https://www.xilinx.com/support/download/drivers
Vendor: Advanced Micro Devices, Inc.
BuildRequires: gcc
BuildRequires: make

%description
This package provides the Xilinx SFPTPD utility which
implements the PTP protocol and works with Xilinx
Ethernet Controllers.

%prep
%setup -q

%build
make %{?_smp_mflags} sfptpd sfptpdctl

%install

CC='false # no compilation at installation stage #'
PACKAGE_NAME=%{name}
INST_SBINDIR=$RPM_BUILD_ROOT%{_sbindir}
INST_DOCDIR=$RPM_BUILD_ROOT%{_docdir}
INST_MANDIR=$RPM_BUILD_ROOT%{_mandir}
INST_CONFDIR=$RPM_BUILD_ROOT%{_sysconfdir}
INST_UNITDIR=$RPM_BUILD_ROOT%{_unitdir}
INST_PKGDOCDIR=$RPM_BUILD_ROOT%{_pkgdocdir}
INST_OMIT="license"
INST_INITS="systemd"

export PACKAGE_NAME CC
export INST_SBINDIR INST_DOCDIR INST_MANDIR INST_CONFDIR INST_UNITDIR INST_PKGDOCDIR
export INST_OMIT INST_INITS

%make_install

%files
%attr(755, root, root) %{_sbindir}/sfptpd
%attr(755, root, root) %{_sbindir}/sfptpdctl
%attr(644, root, root) %{_unitdir}/sfptpd.service
%attr(644, root, root) %config(noreplace) %{_sysconfdir}/sfptpd.conf
%license LICENSE PTPD2_COPYRIGHT NTP_COPYRIGHT.html
%doc %{_pkgdocdir}/examples
%doc %{_pkgdocdir}/config
%{_mandir}/man8/*.8*

%changelog
* Mon Sep  5 2022 Andrew Bower <andrew.bower@amd.com>
- various updates
- separated packaging definitions from source repo

* Mon Jul 14 2014 Laurence Evans
- initial rpm packaging capability
