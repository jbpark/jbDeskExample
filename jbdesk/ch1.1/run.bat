@echo off
set CONDA_ENV_NAME=jbdesk38_64

:: Conda 활성화
call conda activate base

:: Conda 환경 목록 확인 후 존재하지 않으면 생성
conda info --envs | findstr /C:"%CONDA_ENV_NAME%" >nul
if %errorlevel% neq 0 (
    echo Creating conda environment: %CONDA_ENV_NAME%
    conda create -y -n %CONDA_ENV_NAME% python=3.8
)

:: Conda 환경 활성화
call conda activate %CONDA_ENV_NAME%

:: PyQt5 설치
pip show PyQt5 >nul 2>nul
if %errorlevel% neq 0 (
    echo Installing PyQt5...
    pip install PyQt5
)

:: jbdesk.py 실행
python jbdesk.py