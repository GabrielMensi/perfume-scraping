@echo off
echo ==========================================
echo    SCRAPER DE PERFUMES - VERSION SIMPLE
echo ==========================================
echo.

REM Mantener la ventana abierta sin importar que pase
echo Verificando Python...
python --version
if ERRORLEVEL 1 (
    echo.
    echo ERROR: Python no esta instalado o no esta en PATH
    echo.
    echo SOLUCION:
    echo 1. Instala Python desde: https://www.python.org/downloads/
    echo 2. Durante la instalacion, marca "Add Python to PATH"
    echo 3. Reinicia la computadora
    echo.
    goto :end
)

echo.
echo Verificando pip...
pip --version
if ERRORLEVEL 1 (
    echo.
    echo ERROR: pip no esta disponible
    echo Reinstala Python marcando "Add Python to PATH"
    echo.
    goto :end
)

echo.
echo Instalando dependencias...
pip install requests beautifulsoup4 selenium webdriver-manager

echo.
echo Ejecutando scraper...
python scrap_perfumes.py

echo.
echo Script terminado.

:end
echo.
echo Presiona cualquier tecla para cerrar...
pause >nul
