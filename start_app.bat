echo off
chcp 65001
cls

set "get_parent_dir=cd /d %~dp0"
set "venv=.venv\Scripts\activate"
set "pip-compile=python -m piptools compile --upgrade --resolver=backtracking"
set "pip-sync=python -m piptools sync"

set "install_piptools=python -m pip install pip-tools"
set "install_virtualenv=python -m pip install virtualenv"
set "install_click=python -m pip install --upgrade click"


:Menu
echo Opções:
echo [1] - Atualizar dependencias
echo [2] - Setup inicial do ambiente [Rodar somente uma vez!]
echo [3] - Instalar pyenv [No Windows]
echo  -
echo [X] - Sair
echo.
choice /c 123x /m "Selecione a opção:"
echo.

goto Option%ERRORLEVEL%

:Option0
goto Menu


:: [1] - Atualizar dependencias
:Option1
cls
echo Atualizando requirements.txt
cmd /k "%get_parent_dir% & %venv% & %install_click% & %pip-compile% & %pip-sync%"

:: [2] - Setup inicial do ambiente
:Option2
cls
echo Efetuando o setup inicial do ambiente
%install_piptools%
%install_virtualenv%
python -m venv .venv
cmd /k "%get_parent_dir% & %venv% & %install_piptools% & %install_click% & %pip-compile% & %pip-sync%"

:: [3] - Instalar pyenv
:Option3
cls
echo Instalando pyenv
set "SCRIPT_PATH=./install-pyenv-win.ps1"
powershell.exe -Command "& {Invoke-WebRequest -UseBasicParsing -Uri 'https://raw.githubusercontent.com/pyenv-win/pyenv-win/master/pyenv-win/install-pyenv-win.ps1' -OutFile %SCRIPT_PATH%; &'%SCRIPT_PATH%'}"
del "install-pyenv-win.ps1"
goto Menu


:: [X] - Sair
:Option4
exit /B
