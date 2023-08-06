# SPDX-License-Identifier: BSD-3-Clause
# (c) Copyright 2014-2023 Advanced Micro Devices, Inc.

Name: sfptpd
Version: %{pkgversion}
Release: 1%{?dist}
Summary: System time sync daemon supporting PTP, NTP and 1PPS
License: BSD-3-Clause AND BSD-2-Clause AND NTP AND ISC
Group: System Environment/Daemons
Source0: sfptpd-%{version}.tgz
URL: https://www.xilinx.com/download/drivers
Vendor: Advanced Micro Devices, Inc.
BuildRequires: sed
BuildRequires: gcc
BuildRequires: make
BuildRequires: libmnl-devel
BuildRequires: libcap-devel
BuildRoot: %{_tmppath}/%{name}-%{version}-root

%define pkgdocdir %{_defaultdocdir}/%{name}-%{version}

%description
sfptpd provides a system-level solution to time synchronization between local
(system and network interface) clocks and remote (PTP, PPS and NTP) time
sources and sinks. The daemon implements the 2019 edition of the IEEE 1588
Precision Time Protocol over UDP with the default or draft enterprise profile.
Key features are high quality timestamp filtering, bond & VLAN support and
instantaneous & long term monitoring.

%prep
%autosetup
find -iregex '.*\.py' | xargs sed -i -r -e '1s,^(#!).*python3,\1/usr/bin/python2,'
scripts/sfptpd_versioning write %{version}

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
export INST_OMIT="sfptpmon"
export INST_INITS="sysv"
rm -rf $RPM_BUILD_ROOT
%make_install
mkdir -p %{buildroot}%{_localstatedir}/lib/%{name}
touch %{buildroot}%{_localstatedir}/lib/%{name}/{config,interfaces,sync-instances,topology,version,freq-correction-system,ptp-nodes}

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
%{_mandir}/man8/sfptpd.8*
%{_mandir}/man8/sfptpdctl.8*
%dir %{_localstatedir}/lib/%{name}
%ghost %{_localstatedir}/lib/%{name}/config
%ghost %{_localstatedir}/lib/%{name}/interfaces
%ghost %{_localstatedir}/lib/%{name}/sync-instances
%ghost %{_localstatedir}/lib/%{name}/topology
%ghost %{_localstatedir}/lib/%{name}/version
%ghost %config %{_localstatedir}/lib/%{name}/freq-correction-system
%ghost %{_localstatedir}/lib/%{name}/ptp-nodes

%clean
rm -rf $RPM_BUILD_ROOT

%changelog
* Sun Aug  6 2023 Andrew Bower <andrew.bower@amd.com> - 3.7.0.1005-1
- add sed build dependency
- expand licence to full SPDX expression
- avoid deprecated wildcard usage
- own state directory in package
- mark state files as ghost

* Thu Jan 26 2023 Andrew Bower <andrew.bower@amd.com> - 3.7.0.1000~1-1
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
