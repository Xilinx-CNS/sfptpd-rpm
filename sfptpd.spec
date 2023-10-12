# SPDX-License-Identifier: BSD-3-Clause
# (c) Copyright 2014-2023 Advanced Micro Devices, Inc.

Name: sfptpd
Version: %{pkgversion}
Release: 1
Summary: System time sync daemon supporting PTP, NTP and 1PPS
License: BSD-3-Clause AND BSD-2-Clause AND NTP AND ISC
Group: System Environment/Daemons
Source0: sfptpd-%{version}.tgz
URL: https://www.xilinx.com/download/drivers
Vendor: Advanced Micro Devices, Inc.
BuildRequires: gcc
BuildRequires: make
BuildRequires: systemd-rpm-macros
BuildRequires: libmnl-devel
BuildRequires: libcap-devel

%description
sfptpd provides a system-level solution to time synchronization between local
(system and network interface) clocks and remote (PTP, PPS and NTP) time
sources and sinks. The daemon implements the 2019 edition of the IEEE 1588
Precision Time Protocol over UDP with the default or draft enterprise profile.
Key features are high quality timestamp filtering, bond & VLAN support and
instantaneous & long term monitoring.

%prep
%autosetup
scripts/sfptpd_versioning write %{version}

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
mkdir -p %{buildroot}%{_localstatedir}/lib/%{name}
touch %{buildroot}%{_localstatedir}/lib/%{name}/{config,interfaces,sync-instances,topology,version,freq-correction-system,ptp-nodes}

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
%attr(755, root, root) %{_sbindir}/sfptpmon
%attr(644, root, root) %{_unitdir}/sfptpd.service
%attr(644, root, root) %config(noreplace) %{_sysconfdir}/sfptpd.conf
%attr(644, root, root) %config(noreplace) %{_sysconfdir}/sysconfig/sfptpd
%license LICENSE PTPD2_COPYRIGHT NTP_COPYRIGHT.html
%doc %{_pkgdocdir}
%{_mandir}/man8/sfptpd.8*
%{_mandir}/man8/sfptpdctl.8*
%{_mandir}/man8/sfptpmon.8*
%dir %{_localstatedir}/lib/%{name}
%ghost %{_localstatedir}/lib/%{name}/config
%ghost %{_localstatedir}/lib/%{name}/interfaces
%ghost %{_localstatedir}/lib/%{name}/sync-instances
%ghost %{_localstatedir}/lib/%{name}/topology
%ghost %{_localstatedir}/lib/%{name}/version
%ghost %{_localstatedir}/lib/%{name}/ptp-nodes

%changelog
* Thu Oct 12 2023 Andrew Bower <andrew.bower@amd.com> - 3.7.1.1000-1
- add '--console' and '-f -' options to command line
- ignore irrelevant PTP packets in sfptpmon script
- fix teaming netlink handler
- fix initial clock correction issues in rare cases
- avoid complication of package owning system frequency correction file

* Tue Aug  8 2023 Andrew Bower <andrew.bower@amd.com> - 3.7.0.1006-1
- add sfptpmon tool
- expand licence to full SPDX expression
- avoid deprecated wildcard usage
- own state directory in package
- mark state files as ghost
- run as root and don't create resulting unused sfptpd user or udev rules

* Thu Jan 26 2023 Andrew Bower <andrew.bower@amd.com> - 3.7.0.1000~1-1
- create sfptpd user
- add udev rules
- add new dependencies

* Tue Jan  3 2023 Andrew Bower <andrew.bower@amd.com> - 3.6.0.1015-1
- use versioning script to encode version

* Wed Nov  9 2022 Andrew Bower <andrew.bower@amd.com> - 3.6.0.1009~1-1
- use buildroot macro, fast_test target and sysconfig options

* Wed Oct 26 2022 Andrew Bower <andrew.bower@amd.com> - 3.6.0.1008-1
- release candidate

* Mon Sep  5 2022 Andrew Bower <andrew.bower@amd.com>
- various updates
- separated packaging definitions from source repo

* Mon Jul 14 2014 Laurence Evans
- initial rpm packaging capability
