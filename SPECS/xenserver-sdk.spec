Summary: XenServer SDK
Name:   xenserver-sdk
Version: 1.12.1
Release: 3%{dist}
License: BSD 2-Clause
Vendor:  Citrix
URL:     https://github.com/xapi-project/xen-api-sdk
Source0: https://code.citrite.net/rest/archive/latest/projects/XSU/repos/xen-api-sdk/archive?at=v%{version}&format=tar.gz#/xen-api-sdk-%{version}.tar.gz
Source1: build-after.sh
Source2: build-before.sh
Source3: build-win.bat
Source4: deps-map.json
Source5: pipeline.groovy
Source6: sign.bat

BuildArch: noarch
BuildRequires: ocaml
BuildRequires: opam
BuildRequires: xs-opam-repo
BuildRequires: branding-xenserver
BuildRequires: ocaml-xen-api-libs-transitional
BuildRequires: xapi-client-devel
BuildRequires: xapi-datamodel-devel
BuildRequires: xenserver-multipath
BuildRequires: xenserver-lvm2
BuildRequires: busybox
BuildRequires: vmss
BuildRequires: xapi-core
BuildRequires: sm

%description
XenServer SDK.

%prep
%autosetup -p1 -c


%build
export OPAMROOT=/usr/lib/opamroot
eval `opam config env`

VERSIONS=/usr/src/branding/toplevel-versions
MAJOR=$(cat ${VERSIONS} | grep -F "PRODUCT_MAJOR_VERSION := " | sed -e 's/PRODUCT_MAJOR_VERSION := //g')
MINOR=$(cat ${VERSIONS} | grep -F "PRODUCT_MINOR_VERSION := " | sed -e 's/PRODUCT_MINOR_VERSION := //g')
MICRO=$(cat ${VERSIONS} | grep -F "PRODUCT_MICRO_VERSION := " | sed -e 's/PRODUCT_MICRO_VERSION := //g')

#===============================================================================
# Normally the SDK will have the same version as the server. If we need to
# hotfix it independently, it should get its own microversion. In this case,
# the ${MICRO} variable should be replaced with a hardcoded number to override
# the one from branding. This should be subsequently bumped for each new hotfix.
#===============================================================================
MICRO_OVERRIDE=${MICRO}

export SDK_VERSION=${MAJOR}.${MINOR}.${MICRO_OVERRIDE}
echo ${SDK_VERSION}
make


%define sdk_dir %{_datarootdir}/xapi/sdk

%install
%{__install} -d %{buildroot}%{sdk_dir}/c
%{__install} -d %{buildroot}%{sdk_dir}/csharp
%{__install} -d %{buildroot}%{sdk_dir}/java
%{__install} -d %{buildroot}%{sdk_dir}/powershell
%{__install} -d %{buildroot}%{sdk_dir}/python

cp -r c/autogen/*          %{buildroot}%{sdk_dir}/c
cp -r csharp/autogen/*     %{buildroot}%{sdk_dir}/csharp
cp -r java/autogen/*       %{buildroot}%{sdk_dir}/java
cp -r powershell/autogen/* %{buildroot}%{sdk_dir}/powershell
cp %{python_sitelib}/XenAPI.py %{buildroot}%{sdk_dir}/python
cp -r python/samples       %{buildroot}%{sdk_dir}/python

cp %{SOURCE1} %{SOURCE2} %{SOURCE3} %{SOURCE4} %{SOURCE5} %{SOURCE6} %{buildroot}%{sdk_dir}/

find %{buildroot}%{sdk_dir} -type f -exec chmod 644 {} \;

#we need only sources, without compiling anything
exit 0


%files
%{sdk_dir}/*


%changelog
* Fri Apr 28 2017 Konstantina Chremmou <konstantina.chremmou@citrix.com> - 1.12.1-3
- Removed obsolete script.

* Wed Apr 26 2017 Konstantina Chremmou <konstantina.chremmou@citrix.com> - 1.12.1-2
- Included build scripts in the rpm.

* Mon Apr 24 2017 Mihaela Stoica <mihaela.stoica@citrix.com> - 1.12.1-1
- Update to version v1.12.1, which contains the fix for CA-249845

* Mon Apr 10 2017 Konstantina Chremmou <konstantina.chremmou@citrix.com> - 1.12.0-1
- Bumped API version.

* Thu Mar 30 2017 Konstantina Chremmou <konstantina.chremmou@citrix.com> - 1.11.0-1
- Included python samples. C# project file minor simplification.

* Thu Mar 23 2017 Konstantina Chremmou <konstantina.chremmou@citrix.com> - 1.10.0-2
- Included the python module.

* Fri Mar 17 2017 Konstantina Chremmou <konstantina.chremmou@citrix.com> - 1.10.0-1
- Update to version v1.10.0. Changed installation folder.

* Thu Mar 16 2017 Konstantina Chremmou <konstantina.chremmou@citrix.com> - 1.0-7
- Re-packaging

* Mon Mar 13 2017 Konstantina Chremmou <konstantina.chremmou@citrix.com> - 1.0-1
- Initial implementation
