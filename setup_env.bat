@echo off
:: Nombre del entorno virtual
set VENV_NAME=.venv

echo Creando el entorno virtual...
python -m venv %VENV_NAME%
if errorlevel 1 (
    echo Error al crear el entorno virtual.
    exit /b 1
)

echo Activando el entorno virtual...
call %VENV_NAME%\Scripts\activate
if errorlevel 1 (
    echo Error al activar el entorno virtual.
    exit /b 1
)

echo Instalando dependencias desde requirements.txt...
pip install -r requirements.txt
if errorlevel 1 (
    echo Error al instalar dependencias.
    exit /b 1
)

echo Todo listo. El entorno virtual esta configurado y las dependencias instaladas.
pause
