set MSBUILD=%SYSTEMROOT%\Microsoft.NET\Framework\v4.0.30319\MSBuild.exe
set RESGEN="%SYSTEMDRIVE%\Program Files (x86)\Microsoft SDKs\Windows\v8.1A\bin\NETFX 4.5.1 Tools\ResGen.exe"

cd csharp\src
%RESGEN% FriendlyErrorNames.resx /str:cs,XenAPI,FriendlyErrorNames,FriendlyErrorNames.Designer.cs /publicClass
%MSBUILD% XenServer.csproj /t:Build /p:Configuration=Release /p:SignAssembly=true /p:AssemblyOriginatorKeyFile=%1

cd ..\..
call sign.bat csharp\src\bin\Release\XenServer.dll "XenServer.NET" || goto :error
call sign.bat csharp\src\bin\Release\CookComputing.XmlRpcV2.dll "XML-RPC.NET by Charles Cook, signed by Citrix" || goto :error

copy csharp\src\bin\Release\XenServer.dll powershell\src
copy csharp\src\bin\Release\CookComputing.XmlRpcV2.dll powershell\src

set CSC=%SYSTEMROOT%\Microsoft.NET\Framework\v4.0.30319\csc.exe

cd powershell\src
%CSC% /target:library /out:XenServerPowerShell.dll /r:System.Management.Automation.dll /R:XenServer.dll /R:CookComputing.XmlRpcV2.dll *.cs"

cd ..\..
call sign.bat powershell\src\XenServerPowerShell.dll "XenServer PowerShell Module" || goto :error
for /R %%g in (*.ps1xml *.ps1) do (
    call sign.bat %%g  || goto :error
)

:error
exit /b %errorlevel%
