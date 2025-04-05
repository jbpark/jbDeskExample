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

:: Vagrant VM 상태 확인
for %%i in (%VM_NAME1% %VM_NAME2% %VM_NAME3%) do (
    vagrant status %%i >nul 2>&1
    if %errorlevel% equ 0 (
        echo VM %%i 가 존재합니다. 삭제를 시작합니다.
        vagrant destroy %%i -f
    ) else (
        echo VM %%i 는 존재하지 않습니다.
    )
)

for %%i in (%VM_PATH1% %VM_PATH2% %VM_PATH3%) do (
    if exist "%%i" (
        echo Deleting "%%i"...
        rmdir /s /q %%i
        echo Deleted successfully. : %%i
    ) else (
        echo Directory does not exist: %%i
    )
)

endlocal
