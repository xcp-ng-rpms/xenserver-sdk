#!/bin/bash

set -xeu

rm -rf XenServer-SDK
rm -rf XenCenterBindings

# C

mkdir -p XenServer-SDK/libxenserver/bin
mkdir -p XenServer-SDK/libxenserver/src
mv  c/{COPYING,README} XenServer-SDK/libxenserver
cp -r c/* XenServer-SDK/libxenserver/src
make -C c
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
