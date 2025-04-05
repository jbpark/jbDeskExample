@echo off
setlocal

:: VM 이름 정의
set VM_NAME1=mariadb20
set VM_NAME2=mariadb21
set VM_NAME3=mariadb22

:: VM PATH 정의
set VM_PATH1=%USERPROFILE%\VirtualBox VMs\%VM_NAME1%
set VM_PATH2=%USERPROFILE%\VirtualBox VMs\%VM_NAME2%
set VM_PATH3=%USERPROFILE%\VirtualBox VMs\%VM_NAME3%

:: Vagrant VM 상태 확인
for %%i in (%VM_NAME1% %VM_NAME2% %VM_NAME3%) do (
    vagrant status %%i >nul 2>&1
    if %errorlevel% equ 0 (
        echo VM %%i가 존재합니다. 삭제를 시작합니다.
        vagrant destroy %%i -f
    ) else (
        echo VM %%i는 존재하지 않습니다.
    )
)

endlocal



set VM_NAME=oracle21c
set VM_PATH=%USERPROFILE%\VirtualBox VMs\%VM_NAME%
set VDI_FILE=%VM_NAME%.vdi

:: VirtualBox의 전체 경로로 VBoxManage 실행
set VBOXMANAGE="C:\Program Files\Oracle\VirtualBox\VBoxManage.exe"

:: VM이 실행 중인지 확인하고 종료
echo Checking if VM is running...
%VBOXMANAGE% showvminfo %VM_NAME% --machinereadable | findstr "VMState=" | findstr /i "running"
if %errorlevel%==0 (
    echo VM is running. Stopping the VM...
    vagrant halt %VM_NAME% --force

    :: 잠시 기다린 후 삭제 작업
    timeout /t 5 /nobreak
) else (
    echo VM is not running.
)

if exist "%VM_PATH%" (
    echo Deleting "%VM_PATH%"...
    vagrant destroy -f %VM_NAME%
    rmdir /s /q "%VM_PATH%"
    echo Deleted successfully. : "%VM_NAME%"
) else (
    echo Directory does not exist: "%VM_PATH%"
)

if exist "%VDI_FILE%" (
    %VBOXMANAGE% closemedium disk "%VDI_FILE%"
    del /f /q "%VDI_FILE%"
    echo %VDI_FILE% has been deleted.
) else (
    echo %VDI_FILE% does not exist.
)