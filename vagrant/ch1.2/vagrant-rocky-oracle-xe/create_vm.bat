@echo off
set VM_NAME=oracle21c
set VM_PATH=%USERPROFILE%\VirtualBox VMs\%VM_NAME%
set VDI_FILE=%VM_NAME%.vdi

:: VirtualBox의 전체 경로로 VBoxManage 실행
set VBOXMANAGE="C:\Program Files\Oracle\VirtualBox\VBoxManage.exe"

if exist "%VDI_FILE%" (
    %VBOXMANAGE% closemedium disk "%VDI_FILE%"
    del /f /q "%VDI_FILE%"
    echo %VDI_FILE% has been deleted.
) else (
    echo %VDI_FILE% does not exist.
)

if exist "%VM_PATH%" (
    echo %VM_NAME% already exists.
) else (
    echo %VM_NAME% does not exist. Starting Vagrant VM...
    vagrant halt
    vagrant up
)