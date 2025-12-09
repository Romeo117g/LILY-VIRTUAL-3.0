@echo off
REM ════════════════════════════════════════════════════════════════════
REM    LILY AI - INSTALADOR AUTOMÁTICO COMPLETO
REM ════════════════════════════════════════════════════════════════════
REM Este script instala automáticamente todos los requisitos para Lily
REM ════════════════════════════════════════════════════════════════════

title Lily AI - Instalador Automático
color 0A

echo.
echo ════════════════════════════════════════════════════════════════════
echo    LILY AI - INSTALADOR AUTOMÁTICO
echo ════════════════════════════════════════════════════════════════════
echo.
echo Este script instalará automáticamente:
echo   [1] Dependencias de Python (pip install)
echo   [2] Modelo Ollama Mistral 7B
echo   [3] Modelo Vosk para reconocimiento de voz
echo.
echo ⚠️  IMPORTANTE:
echo   - Python 3.11+ debe estar instalado
echo   - Ollama debe estar instalado
echo   - Se requiere conexión a internet
echo.
echo ════════════════════════════════════════════════════════════════════
echo.

pause

REM ════════════════════════════════════════════════════════════════════
REM PASO 1: VERIFICAR PYTHON
REM ════════════════════════════════════════════════════════════════════

echo.
echo [PASO 1/5] Verificando Python...
echo ────────────────────────────────────────────────────────────────────

python --version >nul 2>&1
if errorlevel 1 (
    echo.
    echo ❌ ERROR: Python no está instalado o no está en PATH
    echo.
    echo Por favor:
    echo 1. Descarga Python 3.11+ desde: https://www.python.org/downloads/
    echo 2. Durante la instalación, marca "Add Python to PATH"
    echo 3. Reinicia esta instalación
    echo.
    pause
    exit /b 1
)

python --version
echo ✅ Python detectado correctamente
echo.

REM ════════════════════════════════════════════════════════════════════
REM PASO 2: INSTALAR DEPENDENCIAS DE PYTHON
REM ════════════════════════════════════════════════════════════════════

echo.
echo [PASO 2/5] Instalando dependencias de Python...
echo ────────────────────────────────────────────────────────────────────
echo.
echo Esto puede tardar varios minutos...
echo.

pip install --upgrade pip
if errorlevel 1 (
    echo ❌ Error actualizando pip
    pause
    exit /b 1
)

pip install -r requirements.txt
if errorlevel 1 (
    echo.
    echo ❌ ERROR: No se pudieron instalar las dependencias
    echo.
    echo Intenta ejecutar manualmente:
    echo   pip install -r requirements.txt
    echo.
    pause
    exit /b 1
)

echo.
echo ✅ Dependencias de Python instaladas correctamente
echo.

REM ════════════════════════════════════════════════════════════════════
REM PASO 3: VERIFICAR OLLAMA
REM ════════════════════════════════════════════════════════════════════

echo.
echo [PASO 3/5] Verificando Ollama...
echo ────────────────────────────────────────────────────────────────────

ollama --version >nul 2>&1
if errorlevel 1 (
    echo.
    echo ❌ ADVERTENCIA: Ollama no está instalado
    echo.
    echo Por favor:
    echo 1. Descarga Ollama desde: https://ollama.ai/
    echo 2. Instala Ollama
    echo 3. Ejecuta este instalador nuevamente
    echo.
    echo ¿Deseas continuar sin Ollama? (No recomendado)
    pause
    goto SKIP_OLLAMA
)

echo ✅ Ollama detectado
echo.

REM ════════════════════════════════════════════════════════════════════
REM PASO 4: DESCARGAR MODELO MISTRAL
REM ════════════════════════════════════════════════════════════════════

echo.
echo [PASO 4/5] Descargando modelo Mistral 7B...
echo ────────────────────────────────────────────────────────────────────
echo.
echo ⚠️  ADVERTENCIA: Esta descarga es de ~4GB
echo    Puede tardar 10-20 minutos dependiendo de tu conexión
echo.

REM Verificar si Mistral ya está instalado
ollama list | findstr "mistral" >nul 2>&1
if not errorlevel 1 (
    echo ✅ Modelo Mistral ya está instalado
    echo.
    goto SKIP_MISTRAL
)

echo Descargando Mistral 7B...
ollama pull mistral
if errorlevel 1 (
    echo.
    echo ❌ ERROR: No se pudo descargar el modelo Mistral
    echo.
    echo Intenta ejecutar manualmente:
    echo   ollama pull mistral
    echo.
    pause
    exit /b 1
)

echo.
echo ✅ Modelo Mistral descargado correctamente
echo.

:SKIP_MISTRAL
:SKIP_OLLAMA

REM ════════════════════════════════════════════════════════════════════
REM PASO 5: DESCARGAR MODELO VOSK
REM ════════════════════════════════════════════════════════════════════

echo.
echo [PASO 5/5] Descargando modelo Vosk para reconocimiento de voz...
echo ────────────────────────────────────────────────────────────────────
echo.

REM Verificar si el modelo Vosk ya existe
if exist "models\vosk-model-small-es-0.42" (
    echo ✅ Modelo Vosk ya está instalado
    echo.
    goto SKIP_VOSK
)

echo Descargando modelo Vosk español (~50 MB)...
echo.

REM Crear carpeta models si no existe
if not exist "models" mkdir models

REM Descargar modelo Vosk usando PowerShell
powershell -Command "& {Invoke-WebRequest -Uri 'https://alphacephei.com/vosk/models/vosk-model-small-es-0.42.zip' -OutFile 'models\vosk-model-small-es-0.42.zip'}"

if errorlevel 1 (
    echo.
    echo ❌ ERROR: No se pudo descargar el modelo Vosk
    echo.
    echo Por favor descarga manualmente desde:
    echo https://alphacephei.com/vosk/models/vosk-model-small-es-0.42.zip
    echo.
    echo Y extrae en: models\vosk-model-small-es-0.42\
    echo.
    pause
    goto SKIP_VOSK
)

echo Extrayendo modelo Vosk...
powershell -Command "& {Expand-Archive -Path 'models\vosk-model-small-es-0.42.zip' -DestinationPath 'models\' -Force}"

if errorlevel 1 (
    echo.
    echo ❌ ERROR: No se pudo extraer el modelo Vosk
    echo.
    pause
    goto SKIP_VOSK
)

REM Eliminar archivo ZIP
del "models\vosk-model-small-es-0.42.zip"

echo.
echo ✅ Modelo Vosk instalado correctamente
echo.

:SKIP_VOSK

REM ════════════════════════════════════════════════════════════════════
REM RESUMEN DE INSTALACIÓN
REM ════════════════════════════════════════════════════════════════════

echo.
echo ════════════════════════════════════════════════════════════════════
echo    INSTALACIÓN COMPLETADA
echo ════════════════════════════════════════════════════════════════════
echo.

REM Verificar componentes instalados
echo Verificando componentes instalados:
echo.

python --version >nul 2>&1
if not errorlevel 1 (
    echo ✅ Python instalado
) else (
    echo ❌ Python NO instalado
)

pip show vosk >nul 2>&1
if not errorlevel 1 (
    echo ✅ Vosk instalado
) else (
    echo ❌ Vosk NO instalado
)

pip show pyaudio >nul 2>&1
if not errorlevel 1 (
    echo ✅ PyAudio instalado
) else (
    echo ❌ PyAudio NO instalado
)

pip show pyautogui >nul 2>&1
if not errorlevel 1 (
    echo ✅ PyAutoGUI instalado
) else (
    echo ❌ PyAutoGUI NO instalado
)

ollama list | findstr "mistral" >nul 2>&1
if not errorlevel 1 (
    echo ✅ Modelo Mistral instalado
) else (
    echo ❌ Modelo Mistral NO instalado
)

if exist "models\vosk-model-small-es-0.42" (
    echo ✅ Modelo Vosk instalado
) else (
    echo ❌ Modelo Vosk NO instalado
)

echo.
echo ════════════════════════════════════════════════════════════════════
echo.
echo 🎉 ¡Instalación completada!
echo.
echo PRÓXIMOS PASOS:
echo   1. Ejecuta INICIAR_LILY.bat para iniciar Lily
echo   2. Di "LILY" para activar el wake word
echo   3. ¡Disfruta de tu asistente virtual!
echo.
echo ════════════════════════════════════════════════════════════════════
echo.

pause
