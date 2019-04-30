#!/bin/bash

set -xeu

rm -rf XenServer-SDK
rm -rf XenCenterBindings

# C

mkdir -p XenServer-SDK/libxenserver/bin
mkdir -p XenServer-SDK/libxenserver/src
mv  c/{COPYING,README} XenServer-SDK/libxenserver
cp -r c/* XenServer-SDK/libxenserver/src
make -C c all
mv c/libxenserver.so* XenServer-SDK/libxenserver/bin

# Java

mkdir -p XenServer-SDK/XenServerJava/bin
mkdir -p XenServer-SDK/XenServerJava/javadoc
mkdir -p XenServer-SDK/XenServerJava/samples
mkdir -p XenServer-SDK/XenServerJava/src
mv java/{LICENSE.txt,README.txt,LICENSE.Apache-2.0.txt} XenServer-SDK/XenServerJava
cp java/samples/* XenServer-SDK/XenServerJava/samples
cp java/Makefile XenServer-SDK/XenServerJava/src
cp -r java/com XenServer-SDK/XenServerJava/src

mv *.jar java
mv java/samples/* java
make -C java all docs
mv java/*.jar XenServer-SDK/XenServerJava/bin
cp -r java/doc/* XenServer-SDK/XenServerJava/javadoc

# Python

mkdir -p XenServer-SDK/XenServerPython
cp -r python/* XenServer-SDK/XenServerPython

# API reference

mkdir doctemp
cp -r /usr/share/xapi/doc/* doctemp
cd doctemp && sh doc-convert.sh
cd ..

mkdir -p XenServer-SDK/API-reference
cp -r doctemp/html XenServer-SDK/API-reference

mkdir management-api
cp -r doctemp/html management-api

mkdir -p management-api/markdown
cp doctemp/markdown/*.md doctemp/markdown/*.png management-api/markdown

# Csharp

mkdir XenCenterBindings
cp csharp/src/*.cs csharp/src/*.resx XenCenterBindings/

mkdir -p XenServer-SDK/XenServer.NET/bin
mkdir -p XenServer-SDK/XenServer.NET/samples
mkdir -p XenServer-SDK/XenServer.NET/src
for dest in bin samples src; do
  cp csharp/LICENSE.txt XenServer-SDK/XenServer.NET/${dest}/LICENSE.txt
  cp LICENSE.CookComputing.XmlRpcV2.txt XenServer-SDK/XenServer.NET/${dest}
  cp LICENSE.Newtonsoft.Json.txt XenServer-SDK/XenServer.NET/${dest}
done

mv csharp/README.txt XenServer-SDK/XenServer.NET

cp -r csharp/samples/* XenServer-SDK/XenServer.NET/samples
cp CookComputing.XmlRpcV2.dll csharp/samples
cp Newtonsoft.Json.dll csharp/samples

cp -r csharp/src/* XenServer-SDK/XenServer.NET/src
cp CookComputing.XmlRpcV2.dll csharp/src
cp Newtonsoft.Json.dll csharp/src

# PS

mkdir -p XenServer-SDK/XenServerPowerShell/samples
mkdir -p XenServer-SDK/XenServerPowerShell/src
mkdir -p XenServer-SDK/XenServerPowerShell/XenServerPSModule

for dest in src samples XenServerPSModule; do
  cp powershell/LICENSE.txt XenServer-SDK/XenServerPowerShell/${dest}
  cp LICENSE.CookComputing.XmlRpcV2.txt XenServer-SDK/XenServerPowerShell/${dest}
  cp LICENSE.Newtonsoft.Json.txt XenServer-SDK/XenServerPowerShell/${dest}
done

mv powershell/README.txt XenServer-SDK/XenServerPowerShell
mv powershell/{about_XenServer.help.txt,*.psd1} XenServer-SDK/XenServerPowerShell/XenServerPSModule
cp -r powershell/src/* XenServer-SDK/XenServerPowerShell/src
mv System.Management.Automation.dll powershell/src
