@echo off
REM Cambia al directorio donde está ubicado el .bat
cd /d "%~dp0"

REM Verifica si el entorno virtual existe
if not exist ".venv\Scripts\activate" (
    echo El entorno virtual no se encontro. Asegurate de que el entorno virtual este en la carpeta correcta.
    pause
    exit /b
)

REM Activa el entorno virtual
call .venv\Scripts\activate

REM Verifica si el archivo main.py existe
if not exist "main.py" (
    echo El archivo main.py no se encontro en la carpeta actual.
    pause
    exit /b
)

REM Ejecuta el archivo main.py
python main.py

REM Mantiene la ventana abierta para ver la salida
pause
