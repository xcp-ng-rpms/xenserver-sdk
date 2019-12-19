#!/bin/bash

set -xeu

# rename and zip up
mv XenServer-SDK CitrixHypervisor-SDK
zip -q -r9 CitrixHypervisor-SDK.zip CitrixHypervisor-SDK

# XenCenter bindings
zip -q -r9 XenCenterBindings.zip XenCenterBindings

# API reference
zip -q -r9 management-api.zip management-api
