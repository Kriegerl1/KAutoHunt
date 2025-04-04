@echo off
:: Eleva para administrador, se necessário
openfiles >nul 2>nul
if %errorlevel% NEQ 0 (
    powershell -Command "Start-Process '%~f0' -Verb runAs"
    exit
)

:: Vai para a pasta onde o script .bat está localizado
cd /d "%~dp0"

:: Ativa a virtualenv
call "Py310\Scripts\activate"

:: Executa o script principal
python -m src.main

:: Pausa para exibir a saída
pause