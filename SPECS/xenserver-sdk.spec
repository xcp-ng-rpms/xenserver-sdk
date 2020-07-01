Summary: XenServer SDK
Name:   xenserver-sdk
Version: 1.62.0
Release: 1.xapi.1.249.3
License: BSD 2-Clause
Vendor:  Citrix Systems, Inc.
URL:     https://github.com/xapi-project/xen-api-sdk

Source0: https://code.citrite.net/rest/archive/latest/projects/XSU/repos/xen-api-sdk/archive?at=v1.62.0&prefix=xenserver-sdk-1.62.0&format=tar.gz#/xen-api-sdk-1.62.0.tar.gz
Source1: SOURCES/xenserver-sdk/build-after.sh
Source2: SOURCES/xenserver-sdk/build-before.sh
Source3: SOURCES/xenserver-sdk/build-win.bat
Source4: SOURCES/xenserver-sdk/deps-map.json
Source5: SOURCES/xenserver-sdk/sign.bat
Source6: SOURCES/xenserver-sdk/Citrix.Hypervisor.SDK.nuspec


Provides: gitsha(https://code.citrite.net/rest/archive/latest/projects/XSU/repos/xen-api-sdk/archive?at=v1.62.0&prefix=xenserver-sdk-1.62.0&format=tar.gz#/xen-api-sdk-1.62.0.tar.gz) = ec6adc5eaf6ebb6ea52930302489387127a457eb


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
%autosetup -p1


%build
export OPAMROOT=%{_opamroot}
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
export SR_XML=/opt/xensource/sm/XE_SR_ERRORCODES.xml
export PRODUCT_GUID=$(uuidgen | tr a-z A-Z)
make
sed -e "s|@SDK_VERSION@|${SDK_VERSION}|g" %{SOURCE6} > Citrix.Hypervisor.SDK.nuspec

%define sdk_dir %{_datarootdir}/xapi/sdk

%install
%{__install} -d %{buildroot}%{sdk_dir}/c
%{__install} -d %{buildroot}%{sdk_dir}/csharp
%{__install} -d %{buildroot}%{sdk_dir}/java
%{__install} -d %{buildroot}%{sdk_dir}/powershell
%{__install} -d %{buildroot}%{sdk_dir}/python

cp -r _build/default/c/autogen/*          %{buildroot}%{sdk_dir}/c
cp -r _build/default/csharp/autogen/*     %{buildroot}%{sdk_dir}/csharp
cp -r _build/default/java/autogen/*       %{buildroot}%{sdk_dir}/java
cp -r _build/default/powershell/autogen/* %{buildroot}%{sdk_dir}/powershell
cp %{python_sitelib}/XenAPI.py    %{buildroot}%{sdk_dir}/python
cp -r python/samples              %{buildroot}%{sdk_dir}/python

cp %{SOURCE1} %{SOURCE2} %{SOURCE3} %{SOURCE4} %{SOURCE5} %{buildroot}%{sdk_dir}/
cp Citrix.Hypervisor.SDK.nuspec %{buildroot}%{sdk_dir}/csharp/Citrix.Hypervisor.SDK.nuspec

find %{buildroot}%{sdk_dir} -type f -exec chmod 644 {} \;

#we need only sources, without compiling anything
exit 0


%files
%{sdk_dir}/*
%exclude %{sdk_dir}/*/dune


%changelog
* Mon Jun 01 2020 Christian Lindig <christian.lindig@citrix.com> - 1.62.0-1
- CA-340473: Synchronous object removers do not return an object.

* Fri May 29 2020 Christian Lindig <christian.lindig@citrix.com> - 1.61.0-1
- Some script corrections:
- Fixed document format.
- Added missing line breaks and replaced non-ASCII characters.
- CA-340392: Do not allow Invoke-* cmdlets to pass through the object on
	which the API call is run if the latter returns void.

* Mon May 18 2020 Christian Lindig <christian.lindig@citrix.com> - 1.60.0-1
- CA-339331: Skip uses deferred execution and needs enumeration. Also:

* Fri Apr 24 2020 Christian Lindig <christian.lindig@citrix.com> - 1.59.0-1
- Improved parsing of SMAPIv3 errors. Deprecated Failure method that
	should not be used directly by the implementation.
- CP-32699: Added a couple of error overrides and an ISO 8601 date
	format.

* Wed Feb 12 2020 Christian Lindig <christian.lindig@citrix.com> - 1.58.0-1
- CA-333712: handle wrapped strings the same as strings

* Tue Feb 04 2020 Christian Lindig <christian.lindig@citrix.com> - 1.57.0-1
- Fixed javadoc compilation errors (needed for CP-32780).
- CP-29452: Deprecated XenObject.Changed property.
- CA-75634: C# SDK: fixed compiler warnings. Treat warnings as errors in
	C# and PS.
- CA-280976: Fixed default value of session fields.
- CA-333394: Fixed compilation error in C++ due to typename being a
	reserved keyword. Tidied up Makefile.
- Generate the MessageTypes using a mustache template.

* Mon Feb 03 2020 Konstantina Chremmou <konstantina.chremmou@citrix.com> - 1.56.0-2.xapi.1.223.0
- CA-75634: C# SDK: fixed compiler warnings. C SDK: Makefile correction.

* Tue Jan 28 2020 Christian Lindig <christian.lindig@citrix.com> - 1.56.0-1
- CA-333871: Corrected the serialization format for DateTime so the API accepts it.
- Use older C# syntax to fix build.

* Fri Jan 10 2020 Christian Lindig <christian.lindig@citrix.com> - 1.55.0-1
- travis: pull settings from xs-opam

* Wed Jan 08 2020 Konstantina Chremmou <konstantina.chremmou@citrix.com> - 1.54.0-2.xapi.1.219.0
- CA-298871: Pass the thumbprints of the self-signing certificates as parameters to the build script.

* Tue Oct 29 2019 Edvin Török <edvin.torok@citrix.com> - 1.54.0-1
- Corrected spelling to match the docs. Use en-us spelling.

* Fri Aug 23 2019 Edwin Török <edvin.torok@citrix.com> - 1.53.0-2.xapi.1.191.0
- bump packages after xs-opam update

* Tue Jul 23 2019 Rob Hoes <rob.hoes@citrix.com> - 1.53.0-1
- Simplify Travis setup

* Fri Jun 21 2019 Christian Lindig <christian.lindig@citrix.com> - 1.52.0-1
- Corrected file permissions.
- Basic implementation of mustache to generate the Proxy and i
  JsonRpcClient classes.
- Use mustache to generate the enum files. Added xml docs to the enum memebrs.
- Remove from the overrides entries that are the same as in
  xen-api (includes CA-258385).
- Remove EventHelpers file from the XenServer project file

* Wed Apr 17 2019 Konstantina Chremmou <konstantina.chremmou@citrix.com> - 1.51.0-1.xapi.1.166.0
- CP-31133: Added NuGet spec file for the C# SDK
- CP-31132: Renamed the Newtonsoft.Json.dll to avoid clashes with the upstream dll

* Wed Apr 03 2019 Christian Lindig <christian.lindig@citrix.com> - 1.50.0-1
- CA-311238 refix: when creating a session from another Session object,
  copy over its properties.
- CP-30785: Replaced xenserver.org links

* Mon Feb 25 2019 Christian Lindig <christian.lindig@citrix.com> - 1.49.0-1
- CA-311238: The constructor creating a Session from another Session object was

* Wed Jan 23 2019 Konstantina Chremmou <konstantina.chremmou@citrix.com> - 1.48.0-2.xapi.1.148.0
- Exclude dune files from packaging.

* Wed Jan 23 2019 Christian Lindig <christian.lindig@citrix.com> - 1.48.0-1
- Removed dependency on xapi-stdext-pervasives.
- Remove dependency on xapi-stdext-unix;
  moved several autogeneration operations from make to dune.
- Deprecated field BINDINGS_VERSION.

* Tue Dec 18 2018 Christian Lindig <christian.lindig@citrix.com> - 1.47.0-1
- Use OCaml 4.07.1.
- CA-305383: Correct Helper.AreEqual2 which considered identical (but
  not reference equal) generic lists or dictionaries as being different.

* Thu Nov 01 2018 Christian Lindig <christian.lindig@citrix.com> - 1.46.0-1
- Rebranding for the SDK READMEs.

* Wed Oct 31 2018 Christian Lindig <christian.lindig@citrix.com> - 1.45.0-1
- Ported xen-api-sdk to dune and fixed warnings.
- Specified profile in dune build invocations.
  Corrected opam file as per travis's warnings.

* Mon Sep 17 2018 Christian Lindig <christian.lindig@citrix.com> - 1.44.0-1
- Apply patch: helpers: Add out_indent for compat with ocaml 4.06

* Fri Sep 14 2018 Christian Lindig <christian.lindig@citrix.com> - 1.43.0-2
- Remove patch 0001-helpers-Add-out_indent-for-compat-with-ocaml-4.06.patch

* Wed Jul 25 2018 Christian Lindig <christian.lindig@citrix.com> - 1.43.0-1
- CA-293478: Always set the WebRequest properties to the values
  specified by the JsonRpcClient.
- Copy some more properties of the XmlRpcProxy to the JsonRpcClient.

* Thu May 24 2018 Christian Lindig <christian.lindig@citrix.com> - 1.42.0-1
- Documentation: "Cannot" is one word.
- CA-275120: Corrected filtering of internal messages.

* Tue May 22 2018 Konstantina Chremmou <konstantina.chremmou@citrix.com> - 1.41.0-6.xapi.1.96.0
- CA-86950: Ensure the java and C# samples are also compiled.
- Packaging: Create the management-api folder first so the html one is copied as a folder in it.

* Mon Apr 16 2018 Christian Lindig <christian.lindig@citrix.com> - 1.41.0-1
- CA-286574: Corrected null check.

* Tue Apr 10 2018 Christian Lindig <christian.lindig@citrix.com> - 1.40.0-1
- CA-281881: G11N: L10N: Hardcode issue in error messages when configure AD for server
- CA-287723: Corrected JsonRpc date-time deserialization.

* Mon Apr 09 2018 Christian Lindig <christian.lindig@citrix.com> - 1.39.0-1
- Java samples: updated the EventMonitor test; minor format changes to the output log.
- CA-286574: Do not access directly properties of the xmlrpc proxy because it is null when we use the jsonrpc backend.
- Redundant cast, using directive, partial declaration. Whitespace.
- Ocp-reindented files.

* Thu Apr 05 2018 Christian Lindig <christian.lindig@citrix.com> - 1.38.0-1
- CP-27391: Support for Option types in the Java SDK.
- CP-27391: Support for Option types in the C SDK.
- CP-27391: Added support for Option types to the C# SDK.
- README correction.

* Thu Mar 22 2018 Marcello Seri <marcello.seri@citrix.com> - 1.37.0-1
- CA-285680: Prevent the Json library from changing the format of date strings when these were deserialised as strings.
- CP-27391: Added support for Option types to the C# SDK.
- Revert "CP-27391: Added support for Option types to the C# SDK."

* Wed Mar 21 2018 Christian Lindig <christian.lindig@citrix.com> - 1.36.0-1
- CA-285349: Add shutdown.py as example script

* Fri Mar 09 2018 Christian Lindig <christian.lindig@citrix.com> - 1.35.0-1
- Fixed deserialization of error for servers using JsonRpc v1.0.
- Return null if the string to deserialize to a XenRef<T> is null.

* Wed Feb 28 2018 Christian Lindig <christian.lindig@citrix.com> - 1.34.0-1
- Reverted to use of the Marshalling methods, as the Hashtable values
  an often be null.$
- CA-284233: Added converter to serialize null values in string-string
  maps to empty strings.

* Thu Feb 22 2018 Christian Lindig <christian.lindig@citrix.com> - 1.33.0-1
- CA-40854: The Session's uuid is in reality its opaque_ref.
- CA-283613: Added missing converters for Map(Ref,Int) and
  Map(Ref,Map(String,String)).
- CA-283697: Avoid resetting a field to null when creating an object
  from a Hashtable not containing the field.

* Mon Feb 19 2018 Christian Lindig <christian.lindig@citrix.com> - 1.32.0-1.xapi.1.72.0
- Added --dev flag to build target; do not build all the generators
  if only a specific language is specified.
- Changed dependencies to use the newly defined packages. Fixed warning.
- Replaced package xapi-stdext-std with astring.

* Thu Feb 01 2018 Konstantina Chremmou <konstantina.chremmou@citrix.com> - 1.31.0-1.xapi.1.72.0
- CA-277216: User OpaqueRef:Null instead of null when assigning a cmldet parameter to the corresponding field.
- Do not use a Session's opaque_ref after logging out because the operation sets it to null.
- Updated paths and instructions after merging from master.

* Fri Jan 26 2018 Konstantina Chremmou <konstantina.chremmou@citrix.com> - 1.30.0-1.xapi.1.69.0
- Support for the JsonRpc protocol in the C# SDK.
- Corrected vendor name in specfile.

* Thu Jan 18 2018 Christian Lindig <christian.lindig@citrix.com> - 1.29.0-1.xapi.1.61.0
- Reverted setting ulimit; it's to no avail since it's outside the container.

* Thu Jan 11 2018 Christian Lindig <christian.lindig@citrix.com> - 1.28.0-1.xapi.1.61.0
- CA-277290: increased the number of tries and intermediate delay
  when checking for the feature-suspend flag.
- Removed unnecessary using directives.
- Update and minor restructuring of the XenServer.NET project file.
- Updated README to describe instructions for debugging the PS source code.
- Added project file template to facilitate building the PowerShell i
  module with MSBuild.
- Fixed travis build and updated README.

* Tue Dec 05 2017 Christian Lindig <christian.lindig@citrix.com> - 1.27.0-1.xapi.1.61.0
- Namespace and assembly metadata correction.

* Fri Nov 24 2017 Christian Lindig <christian.lindig@citrix.com> - 1.26.0-1.xapi.1.61.0
- Added copyright notice.
- Added logging so the samples can be run as automated tests.
- CA-271768: Modified sample so it's easier to run it as an automated test.
- Cleared build warnings for deprecated functions.
- Added reindent target to the Makefile and ocp-indented files.
- Autogenerate the java test GetAllRecordsOfAllTypes so it is kept up
  to date with the available API objects.

* Thu Nov 02 2017 Rob Hoes <rob.hoes@citrix.com> - 1.25.0-1-1.xapi.1.59.0
- CP-25021: Generate automatically sets of records in the C and C# SDK.
- Updated READMEs.
- CA-267062: Fixed segmentation fault in the test_get_records.c.

* Fri Oct 20 2017 Rob Hoes <rob.hoes@citrix.com> - 1.24.0-1.xapi.1.56.0
- xen-api-sdk.opam: depend on xapi-datamodel instead of xapi
- .travis.yml: avoid stack overflow error

* Fri Oct 13 2017 Rob Hoes <rob.hoes@citrix.com> - 1.23.0-1.xapi.1.55.0
- CP-25021: Basic modifications to handling of record sets in order to unblock the build.
- Updated Ocaml version.

* Mon Oct 02 2017 Rob Hoes <rob.hoes@citrix.com> - 1.22.0-1.xapi.1.51.0
- CA-267461: Fix powershell bindings generator for some constructors

* Mon Sep 04 2017 Rob Hoes <rob.hoes@citrix.com> - 1.21.0-1.xapi.1.47.0
- Removed unneeded using directives.
- Moved long hardcoded text to a mustache template.
- Use null coalescing operator.
- Consolidation of the C# sample code.

* Wed Aug 23 2017 Rob Hoes <rob.hoes@citrix.com> - 1.20.0-1.xapi.1.46.0
- Moved the build from oasis to jbuilder.
- Removed unneeded makefile targets and merged the build recipe into one instruction. Updated travis file.

* Mon Aug 21 2017 Konstantina Chremmou <konstantina.chremmou@citrix.com> - 1.19.0-3.xapi.1.45.0
- Use jbuilder to build the SDK.

* Wed Aug 02 2017 Konstantina Chremmou <konstantina.chremmou@citrix.com> - 1.19.0-2.xapi.1.44.0
- Package the API reference in html, markdown, and docbook format.

* Wed Aug 02 2017 Rob Hoes <rob.hoes@citrix.com> - 1.19.0-1.xapi.1.44.0
- CA-249080: Do not throw an error when a Get-XenXXX cmdlet returns no results.
- Removed some unnecessary using directives.
- CA-109372, CP-4751: Connect-XenServer cmdlet enhancements.
- CA-260203: (Basic fix) The connection and reply timeout of the xmlrpc client configuration were not set properly.
- CA-260203: (Extended fix) Deprecated the _replyWait and _connWait fields.
- CA-260203: Use the latest version of the xmlrpc client.
- Removed constructors that have been deprecated since at least API v1.3.

* Wed Jul 12 2017 Rob Hoes <rob.hoes@citrix.com> - 1.18.0-1.xapi.1.42.0
- Do not generate relation bindings for all objects, but only for the filtered ones.
- CA-125488, CA-212616: Generate get-class cmdlets only for classes that have get_all_records.

* Fri Jul 07 2017 Konstantina Chremmou <konstantina.chremmou@citrix.com> - 1.17.0-1.xapi.1.41.0
- Build and include the API reference pdf in the SDK zip.

* Mon Jul 03 2017 Rob Hoes <rob.hoes@citrix.com> - 1.17.0-1.xapi.1.40.0
- Stop generating two almost identical versions of the C# SDK.
- Fix usage errors identified by Lexica
- CA-187179: Add AUTH_DISABLE_FAILED_INVALID_ACCOUNT error message
- CA-254480: XenCenter error message refine for CA-205515

* Tue Jun 20 2017 Konstantina Chremmou <konstantina.chremmou@citrix.com> - 1.16.0-1.xapi.1.37.0
- Included the xapi version in the release info.

* Fri Jun 16 2017 Jon Ludlam <jonathan.ludlam@citrix.com> - 1.16.0-1
- Removed compatibility patch. The unwanted obj_uuid can be filtered out by the C generation code.
- Refactoring and deliverable improvement.
- CA-242702: Corrected implementatation of event.from for the C SDK.

* Wed Jun 7 2017 Konstantina Chremmou <konstantina.chremmou@citrix.com> - 1.15.0-3
- Package the same files for XenCenter as for XenServer.NET.

* Fri Jun 2 2017 Konstantina Chremmou <konstantina.chremmou@citrix.com> - 1.15.0-2
- Removed groovy pipeline.

* Thu Jun 01 2017 Rob Hoes <rob.hoes@citrix.com> - 1.15.0-1
- Fixed build regression and refactored code generation.
- CA-254412: Stop generating XenCenter's object downloader.

* Tue May 23 2017 Rob Hoes <rob.hoes@citrix.com> - 1.14.0-1
- Use the same logic to parse arguments across languages.
- Minor refactoring: no need to define a new function to return the license string.
- CA-245333: Use mustache templates to populate the API versions for historical and current releases.
- Add opam file & Travis configuration (#96)
- Add .merlin file

* Fri May 12 2017 Rob Hoes <rob.hoes@citrix.com> - 1.13.0-1
- Pass the location of the FriendlyErrorNames.resx file as a parameter.
- Removed OMakefile. From now on the SDK will be built with Oasis.
- Moved files from top directory to more relevant locations.

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
