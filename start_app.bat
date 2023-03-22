echo off
chcp 65001
cls

set "get_parent_dir=cd /d %~dp0"
set "venv=.venv\Scripts\activate"
set "pip-compile=pip-compile --upgrade --resolver=backtracking"
set "pip-tools=python -m pip install pip-tools"
set "virtualenv=python -m pip install virtualenv"
set "click=python -m pip install --upgrade click"


:Menu
echo Opções:
echo [1] - Atualizar dependencias
echo [2] - Setup do ambiente
echo [3] - Ativar ambiente virtual
echo [4] - Desativar ambiente virtual
echo  -
echo [X] - Sair
echo.
choice /c 1234x /m "Selecione a opção:"
echo.

goto Option%ERRORLEVEL%

:Option0
goto Menu


:: [1] - Atualizar dependencias
:Option1
cls
echo Atualizando requirements.txt
cmd /k "%get_parent_dir% & %venv% & %click% & %pip-compile% & pip-sync"

:: [2] - Setup do ambiente
:Option2
cls
echo Efetuando o setup do ambiente
%pip-tools%
%virtualenv%
virtualenv .venv
cmd /k "%get_parent_dir% & %venv% & %pip-tools% & %click% & %pip-compile% & pip-sync"

:: [3] - Ativar ambiente virtual
:Option3
echo Ativando ambiente virtual
%venv%
goto Menu

:: [4] - Desativar ambiente virtual
:Option4
echo Desativando ambiente virtual
deactivate
goto Menu


:: [X] - Sair
:Option5
exit /B
