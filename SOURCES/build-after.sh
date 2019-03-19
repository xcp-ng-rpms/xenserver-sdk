#!/bin/bash

set -x

# Csharp

mv csharp/src/bin/Release/{XenServer.dll,CookComputing.XmlRpcV2.dll} XenServer-SDK/XenServer.NET/bin
cp csharp/src/FriendlyErrorNames.Designer.cs XenServer-SDK/XenServer.NET/src

# PS

mv powershell/src/{XenServer.dll,CookComputing.XmlRpcV2.dll,XenServerPowerShell.dll} XenServer-SDK/XenServerPowerShell/XenServerPSModule
mv powershell/samples/* XenServer-SDK/XenServerPowerShell/samples
mv powershell/{Initialize-Environment.ps1,*.ps1xml} XenServer-SDK/XenServerPowerShell/XenServerPSModule

#  zip up
zip -q -r9 XenServer-SDK.zip XenServer-SDK

# XenCenter bindings
mkdir XenCenterBindings
cp -r csharp/gui/* XenCenterBindings/
zip -q -r9 XenCenterBindings.zip XenCenterBindings
