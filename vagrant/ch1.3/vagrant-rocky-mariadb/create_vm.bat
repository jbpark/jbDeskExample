@echo off
chcp 65001 > nul
setlocal

:: VM 이름 정의
set VM_NAME1=mariadb20
set VM_NAME2=mariadb21
set VM_NAME3=mariadb22

:: VM PATH 정의
set VM_PATH1="%USERPROFILE%\VirtualBox VMs\%VM_NAME1%"
set VM_PATH2="%USERPROFILE%\VirtualBox VMs\%VM_NAME2%"
set VM_PATH3="%USERPROFILE%\VirtualBox VMs\%VM_NAME3%"

:: VirtualBox의 전체 경로로 VBoxManage 실행
set VBOXMANAGE="C:\Program Files\Oracle\VirtualBox\VBoxManage.exe"

:: VirtualBox에 등록된 VM인지 확인하고 생성
for %%i in (%VM_NAME1% %VM_NAME2% %VM_NAME3%) do (
    %VBOXMANAGE% list vms | findstr /i "%%i" >nul
    if !errorlevel! == 0 (
        echo VM %%i 가 VirtualBox에 존재합니다.
    ) else (
        echo VM %%i 를 생성합니다.
        vagrant up %%i
    )
)

endlocal
