rem Script parameters:
rem 1 SNK key location
rem 2 Signing node name
rem 3 Self-signing certificate thumbprint1
rem 4 Self-signing certificate thumbprint2

set MSBUILD=%SYSTEMROOT%\Microsoft.NET\Framework\v4.0.30319\MSBuild.exe
set RESGEN="%SYSTEMDRIVE%\Program Files (x86)\Microsoft SDKs\Windows\v8.1A\bin\NETFX 4.5.1 Tools\ResGen.exe"
set NUGET=nuget.exe

rem Csharp

mkdir XenCenterBindings
copy csharp\src\*.cs XenCenterBindings
copy csharp\src\*.resx XenCenterBindings

mkdir XenServer-SDK\XenServer.NET\bin
mkdir XenServer-SDK\XenServer.NET\samples
mkdir XenServer-SDK\XenServer.NET\src

for %%D in (bin,samples,src) do (
  copy csharp\LICENSE.txt XenServer-SDK\XenServer.NET\%%D\LICENSE.txt
  copy LICENSE.CookComputing.XmlRpcV2.txt XenServer-SDK\XenServer.NET\%%D
  copy LICENSE.Newtonsoft.Json.txt XenServer-SDK\XenServer.NET\%%D
)

move /y csharp\README.txt XenServer-SDK\XenServer.NET

xcopy /s csharp\samples\* XenServer-SDK\XenServer.NET\samples
copy CookComputing.XmlRpcV2.dll csharp\samples
copy Newtonsoft.Json.CH.dll csharp\samples

xcopy /s csharp\src\* XenServer-SDK\XenServer.NET\src
copy CookComputing.XmlRpcV2.dll csharp\src
copy Newtonsoft.Json.CH.dll csharp\src
copy LICENSE.CookComputing.XmlRpcV2.txt csharp
copy LICENSE.Newtonsoft.Json.txt csharp

cd csharp\src
%RESGEN% FriendlyErrorNames.resx /str:cs,XenAPI,FriendlyErrorNames,FriendlyErrorNames.Designer.cs /publicClass XenAPI.FriendlyErrorNames.resources
%MSBUILD% XenServer.csproj /t:Build /p:Configuration=Release /p:SignAssembly=true /p:AssemblyOriginatorKeyFile=%1
cd ..\..

copy csharp\src\bin\Release\XenServer.dll csharp\samples
cd csharp\samples
%MSBUILD% XenSdkSample.csproj /t:Build /p:Configuration=Release

cd ..\..
call sign.bat csharp\src\bin\Release\XenServer.dll "XenServer.NET" %2 %3 %4 || goto :error
call sign.bat csharp\src\bin\Release\CookComputing.XmlRpcV2.dll "XML-RPC.NET by Charles Cook, signed by Citrix" %2 %3 %4 || goto :error
call sign.bat csharp\src\bin\Release\Newtonsoft.Json.CH.dll "JSON.NET by James Newton-King, signed by Citrix" %2 %3 %4 || goto :error

for /R csharp\src\bin\Release %%g in (XenServer.dll,CookComputing.XmlRpcV2.dll,Newtonsoft.Json.CH.dll) do copy /y %%g XenServer-SDK\XenServer.NET\bin
copy csharp\src\FriendlyErrorNames.Designer.cs XenServer-SDK\XenServer.NET\src

cd csharp
%NUGET% pack Citrix.Hypervisor.SDK.nuspec
move /y Citrix.Hypervisor.SDK.*.nupkg .\
cd ..

rem PS

mkdir XenServer-SDK\XenServerPowerShell\samples
mkdir XenServer-SDK\XenServerPowerShell\src
mkdir XenServer-SDK\XenServerPowerShell\XenServerPSModule

for %%D in (src,samples,XenServerPSModule) do (
  copy powershell\LICENSE.txt XenServer-SDK\XenServerPowerShell\%%D
  copy LICENSE.CookComputing.XmlRpcV2.txt XenServer-SDK\XenServerPowerShell\%%D
  copy LICENSE.Newtonsoft.Json.txt XenServer-SDK\XenServerPowerShell\%%D
)

move /y powershell\README.txt XenServer-SDK\XenServerPowerShell
move /y powershell\about_XenServer.help.txt XenServer-SDK\XenServerPowerShell\XenServerPSModule
move /y powershell\XenServerPSModule.psd1 XenServer-SDK\XenServerPowerShell\XenServerPSModule
xcopy /s powershell\src\* XenServer-SDK\XenServerPowerShell\src
move /y System.Management.Automation.dll powershell\src


copy csharp\src\bin\Release\XenServer.dll powershell\src
copy csharp\src\bin\Release\CookComputing.XmlRpcV2.dll powershell\src
copy csharp\src\bin\Release\Newtonsoft.Json.CH.dll powershell\src

cd powershell\src
%MSBUILD% XenServerPowerShell.csproj /t:Build /p:Configuration=Release /p:SignAssembly=true /p:AssemblyOriginatorKeyFile=%1

cd ..\..
call sign.bat powershell\src\bin\Release\XenServerPowerShell.dll "XenServer PowerShell Module" %2 %3 %4 || goto :error
for /R %%g in (*.ps1xml *.ps1) do (
  call sign.bat %%g "XenServer SDK" %2 %3 %4 || goto :error
)

for /R powershell\src\bin\Release\ %%g in (XenServer.dll,CookComputing.XmlRpcV2.dll,Newtonsoft.Json.CH.dll,XenServerPowerShell.dll) do (
  move /y %%g XenServer-SDK\XenServerPowerShell\XenServerPSModule
)
for /R powershell\samples %%g in (*) do move /y %%g XenServer-SDK\XenServerPowerShell\samples
for /R powershell %%g in (*.ps1xml) do move /y %%g XenServer-SDK\XenServerPowerShell\XenServerPSModule
move /y powershell\Initialize-Environment.ps1 XenServer-SDK\XenServerPowerShell\XenServerPSModule

:error
exit /b %errorlevel%

