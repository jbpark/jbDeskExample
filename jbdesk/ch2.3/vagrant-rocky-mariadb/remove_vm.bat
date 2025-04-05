@echo off
chcp 65001 > nul
setlocal

:: VM 이름 정의
set VM_NAME1=dev-first
set VM_NAME2=dev-second
set VM_NAME3=stage-first
set VM_NAME4=stage-second
set VM_NAME5=live-first
set VM_NAME6=live-second

:: VM PATH 정의
set VM_PATH1="%USERPROFILE%\VirtualBox VMs\%VM_NAME1%"
set VM_PATH2="%USERPROFILE%\VirtualBox VMs\%VM_NAME2%"
set VM_PATH3="%USERPROFILE%\VirtualBox VMs\%VM_NAME3%"
set VM_PATH4="%USERPROFILE%\VirtualBox VMs\%VM_NAME4%"
set VM_PATH5="%USERPROFILE%\VirtualBox VMs\%VM_NAME5%"
set VM_PATH6="%USERPROFILE%\VirtualBox VMs\%VM_NAME6%"

:: VirtualBox의 전체 경로로 VBoxManage 실행
set VBOXMANAGE="C:\Program Files\Oracle\VirtualBox\VBoxManage.exe"

:: VirtualBox에 등록된 VM인지 확인하고 삭제
for %%i in (%VM_NAME1% %VM_NAME2% %VM_NAME3% %VM_NAME4% %VM_NAME5% %VM_NAME6%) do (
    %VBOXMANAGE% list vms | findstr /i "%%i" >nul
    if !errorlevel! == 0 (
        echo VM %%i 가 VirtualBox에 존재합니다. 삭제를 시작합니다.
        vagrant destroy %%i -f
    ) else (
        echo VM %%i 는 VirtualBox에 존재하지 않습니다.
    )
)

for %%i in (%VM_PATH1% %VM_PATH2% %VM_PATH3% %VM_PATH4% %VM_PATH5% %VM_PATH6%) do (
    if exist "%%i" (
        echo Deleting "%%i"...
        rmdir /s /q %%i
        echo Deleted successfully. : %%i
    ) else (
        echo Directory does not exist: %%i
    )
)

endlocal
