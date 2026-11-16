@echo off
setlocal
cd /d "%~dp0"
py -3 -m venv build\venv-windows
if errorlevel 1 goto erro
build\venv-windows\Scripts\python.exe -m pip install -r requirements-build.txt
if errorlevel 1 goto erro
build\venv-windows\Scripts\python.exe gerar.py
if errorlevel 1 goto erro
echo Executavel pronto em windows\BlockLab.exe
pause
exit /b 0
:erro
echo Falha ao gerar. Verifique se o Python com Tkinter esta instalado e se ha acesso a internet.
pause
exit /b 1
