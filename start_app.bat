@echo off

:menu
echo Which command sequence do you want to run?
echo [1] - Atualizar dependencias [No Windows]
echo [2] - Setup inicial do ambiente [Rodar somente uma vez!]
echo [3] - Instalar pyenv [No Windows]
set /p choice=Enter choice number:

if %choice%==1 (
  .venv\Scripts\activate
  pip-compile --upgrade --resolver=backtracking
  pip-sync
) else if %choice%==2 (
  python -m pip install virtualenv
  virtualenv .venv
  .venv\Scripts\activate
  python -m pip install pip-tools
  pip-compile --upgrade --resolver=backtracking
  pip-sync
) else  if %choice%==3 (
    set "SCRIPT_PATH=./install-pyenv-win.ps1"
    powershell.exe -Command "& {Invoke-WebRequest -UseBasicParsing -Uri 'https://raw.githubusercontent.com/pyenv-win/pyenv-win/master/pyenv-win/install-pyenv-win.ps1' -OutFile %SCRIPT_PATH%; &'%SCRIPT_PATH%'}"
    del "install-pyenv-win.ps1"
) else (
  echo Invalid choice, please enter either 1, 2 or 3.
  goto menu
)
