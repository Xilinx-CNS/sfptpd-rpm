#
# Spec file for building sfptpd source rpm
#
# (c) Copyright 2012-2022 Xilinx, Inc.
#
Name: sfptpd
Version: %{pkgversion}
Release: 1
Summary: Solarflare Enhanced PTP Daemon
License: Xilinx Software License Agreement
Group: Applications/Communications
Source0: sfptpd-%{version}.tgz
URL: https://www.xilinx.com/support/download/nic-software-and-drivers.html#drivers-software
Vendor: Xilinx, Inc.
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
%make_install CC='false # no compilation at installation stage #'

%files
%attr(755, root, root) %{_sbindir}/sfptpd
%attr(755, root, root) %{_sbindir}/sfptpdctl
%attr(644, root, root) %{_prefix}/lib/systemd/system/sfptpd.service
%attr(644, root, root) %config(noreplace) %{_sysconfdir}/sfptpd.conf
%license LICENSE PTPD2_COPYRIGHT NTP_COPYRIGHT.html
%doc %{_pkgdocdir}/examples
%doc %{_pkgdocdir}/config
