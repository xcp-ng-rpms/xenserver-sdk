#!/bin/bash

set -xeu

# Csharp

mv csharp/src/bin/Release/{XenServer.dll,CookComputing.XmlRpcV2.dll,Newtonsoft.Json.dll} XenServer-SDK/XenServer.NET/bin
cp csharp/src/FriendlyErrorNames.Designer.cs XenServer-SDK/XenServer.NET/src

# PS

mv powershell/src/bin/Release/{XenServer.dll,CookComputing.XmlRpcV2.dll,Newtonsoft.Json.dll,XenServerPowerShell.dll} XenServer-SDK/XenServerPowerShell/XenServerPSModule
mv powershell/samples/* XenServer-SDK/XenServerPowerShell/samples
mv powershell/{Initialize-Environment.ps1,*.ps1xml} XenServer-SDK/XenServerPowerShell/XenServerPSModule

# rename and zip up
mv XenServer-SDK CitrixHypervisor-SDK
zip -q -r9 CitrixHypervisor-SDK.zip CitrixHypervisor-SDK

# XenCenter bindings
zip -q -r9 XenCenterBindings.zip XenCenterBindings

# API reference
zip -q -r9 management-api.zip management-api
