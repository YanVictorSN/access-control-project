@echo off

:menu
echo 4Safety - Helper
echo ----------------
echo [1] - Atualizar dependencias
echo [2] - Setup inicial do ambiente [Rodar somente uma vez!]
echo [3] - Instalar Pyenv
echo [4] - Rodar a aplicacao
echo [5] - Abrir PyQt Designer
echo [6] - Sair
echo ----------------
set /p choice="Entre com a opcao [1-6]: "

if %choice%==1 (
    .venv\Scripts\activate
    pip-compile --upgrade --resolver=backtracking
    pip-sync
    goto menu
) else if %choice%==2 (
  python -m pip install virtualenv
  virtualenv .venv
  .venv\Scripts\activate
  python -m pip install pip-tools
  pip-compile --upgrade --resolver=backtracking
  pip-sync
  goto menu
) else  if %choice%==3 (
  set "SCRIPT_PATH=./install-pyenv-win.ps1"
  powershell.exe -Command "& {Invoke-WebRequest -UseBasicParsing -Uri 'https://raw.githubusercontent.com/pyenv-win/pyenv-win/master/pyenv-win/install-pyenv-win.ps1' -OutFile %SCRIPT_PATH%; &'%SCRIPT_PATH%'}"
  del "install-pyenv-win.ps1"
  goto menu
) else if %choice%==4 (
  .venv\Scripts\activate
  python -V
  python app.py
  goto menu
) else if %choice%==5 (
  @start "" ".venv\Lib\site-packages\qt5_applications\Qt\bin\designer.exe"
)else if %choice%==6 (
  exit
) else (
  echo Opcao invalida.
  goto menu
)
