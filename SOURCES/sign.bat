@echo off

rem This script applies to the SDK build on transformer. Do not simply copy it
rem over to other products or build environments - it may give you real grief

rem Script parameters:
rem 1 File to be signed
rem 2 Description
rem 3 Signing node name
rem 4 Self-signing certificate sha1 thumbprint
rem 5 Self-signing certificate sha256 thumbprint

set timestamp_sha1=http://timestamp.digicert.com
set timestamp_sha2=http://timestamp.digicert.com
set thumb_sha1=%4
set thumb_sha256=%5

set cross_sign=yes
set is_ps=no

if /I %~x1 == .ps1 (
    set is_ps=yes
    set cross_sign=no
)
if /I %~x1 == .ps1xml (
    set is_ps=yes
    set cross_sign=no
)

set descr=%~2
if "%descr%"=="" set "descr=XenServer SDK"

SETLOCAL ENABLEDELAYEDEXPANSION

set CTXSIGN=C:\ctxsign2\ctxsign.exe
set CTXSIGN2=C:\ctxsign2\ctxsign.exe

if exist %CTXSIGN% (
    echo %CTXSIGN% exists; signing in SBE

    %CTXSIGN%  --authorise --workerID %3 --orchID %3 --jobID XenServerWindowsLegacyPVTools_signing --task XenServerDotnetPackages-%BUILD_NUMBER% --debug > out.txt
    echo OUTPUT FROM %CTXSIGN% --AUTHORISE:
    type out.txt
    echo OUTPUT ENDS
    if errorlevel = 1 exit /b 1
    echo
    set /p CCSS_TICKET= < out.txt

    if exist %CTXSIGN2% (
        echo %CTXSIGN2% exists

        if "%is_ps%"=="yes" (
            %CTXSIGN2% --sign --key XenServerSHA256.NET_KEY --pagehashes yes --type Authenticode %1
        ) else (
            %CTXSIGN2% --sign --key XenServer.NET_KEY --cross-sign --pagehashes yes --type Authenticode %1
        )
        if %errorlevel% neq 0 exit /b %errorlevel%
        if "%cross_sign%"=="yes" (
            %CTXSIGN2% --sign --authenticode-append --authenticode-SHA256 --key XenServerSHA256.NET_KEY --cross-sign --pagehashes yes %1
            if %errorlevel% neq 0 exit /b %errorlevel%
        )
    ) else (
        echo %CTXSIGN2% does not exist
        %CTXSIGN% --sign --key XenServer.NET_KEY %1
    )
    %CTXSIGN% --end

) else (
    echo %CTXSIGN% does not exist; self-signing.

    if /I "%cross_sign%" == "no" (
        signtool sign -v -sm -sha1 %thumb_sha1% -d "%descr%" -tr %timestamp_sha2% -td sha256 %1
    ) else (
        signtool sign -v -sm -sha1 %thumb_sha1% -d "%descr%" -t %timestamp_sha1% %1
        signtool sign -v -sm -as -sha1 %thumb_sha256% -d "%descr%" -tr %timestamp_sha2% -td sha256 %1
    )
)
