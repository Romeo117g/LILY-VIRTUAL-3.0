# 🚀 INSTALADOR AUTOMÁTICO - Guía de Uso

## 📋 ¿Qué hace INSTALAR_TODO.bat?

Este script automatiza completamente la instalación de Lily AI, instalando:

1. ✅ **Dependencias de Python** (vosk, pyaudio, pyautogui, etc.)
2. ✅ **Modelo Ollama Mistral 7B** (~4GB)
3. ✅ **Modelo Vosk español** (~50MB)

---

## ⚠️ REQUISITOS PREVIOS

Antes de ejecutar el instalador, debes tener instalado:

### 1. Python 3.11 o superior
- **Descargar**: https://www.python.org/downloads/
- **CRÍTICO**: Durante la instalación, marcar "Add Python to PATH"
- **Verificar**: Abrir CMD y ejecutar `python --version`

### 2. Ollama
- **Descargar**: https://ollama.ai/
- **Instalar** Ollama siguiendo las instrucciones
- **Verificar**: Abrir CMD y ejecutar `ollama --version`

### 3. Conexión a Internet
- Necesaria para descargar modelos (~4.5GB total)

---

## 🎯 CÓMO USAR

### Paso 1: Preparación
1. Asegúrate de tener Python y Ollama instalados
2. Cierra cualquier otra aplicación que use mucha red
3. Ten paciencia: la descarga puede tardar 15-30 minutos

### Paso 2: Ejecutar Instalador
1. **Haz doble clic** en `INSTALAR_TODO.bat`
2. Lee la información inicial
3. Presiona cualquier tecla para continuar

### Paso 3: Proceso Automático
El script ejecutará automáticamente:

```
[PASO 1/5] Verificando Python...
[PASO 2/5] Instalando dependencias de Python...
[PASO 3/5] Verificando Ollama...
[PASO 4/5] Descargando modelo Mistral 7B... (~4GB)
[PASO 5/5] Descargando modelo Vosk... (~50MB)
```

### Paso 4: Verificación
Al finalizar, verás un resumen:
```
✅ Python instalado
✅ Vosk instalado
✅ PyAudio instalado
✅ PyAutoGUI instalado
✅ Modelo Mistral instalado
✅ Modelo Vosk instalado
```

---

## ⏱️ TIEMPOS ESTIMADOS

| Componente | Tamaño | Tiempo (100 Mbps) | Tiempo (10 Mbps) |
|------------|--------|-------------------|------------------|
| Dependencias Python | ~200 MB | 1-2 min | 3-5 min |
| Modelo Mistral | ~4 GB | 5-7 min | 50-60 min |
| Modelo Vosk | ~50 MB | 10-20 seg | 1-2 min |
| **TOTAL** | **~4.25 GB** | **7-10 min** | **55-70 min** |

---

## 🐛 SOLUCIÓN DE PROBLEMAS

### ❌ "Python no está instalado o no está en PATH"
**Solución**:
1. Reinstalar Python desde https://www.python.org/
2. Durante instalación, **MARCAR** "Add Python to PATH"
3. Reiniciar computadora
4. Ejecutar instalador nuevamente

### ❌ "Ollama no está instalado"
**Solución**:
1. Descargar Ollama desde https://ollama.ai/
2. Instalar Ollama
3. Ejecutar instalador nuevamente

### ❌ "No se pudo descargar el modelo Mistral"
**Solución**:
1. Verificar conexión a internet
2. Abrir CMD y ejecutar manualmente:
   ```
   ollama pull mistral
   ```
3. Esperar a que termine
4. Continuar con el resto de la instalación

### ❌ "No se pudo descargar el modelo Vosk"
**Solución**:
1. Descargar manualmente desde:
   https://alphacephei.com/vosk/models/vosk-model-small-es-0.42.zip
2. Extraer el archivo ZIP
3. Colocar la carpeta en:
   ```
   E:\Bella-main\LILY VIRTUAL\models\vosk-model-small-es-0.42\
   ```

### ❌ Error al instalar dependencias de Python
**Solución**:
1. Abrir CMD como **Administrador**
2. Navegar a la carpeta del proyecto:
   ```
   cd "E:\Bella-main\LILY VIRTUAL"
   ```
3. Ejecutar manualmente:
   ```
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

---

## ✅ DESPUÉS DE LA INSTALACIÓN

Una vez completada la instalación:

1. **Ejecuta** `INICIAR_LILY.bat`
2. **Espera** a que se abra Microsoft Edge
3. **Di "LILY"** para probar el wake word
4. **¡Disfruta** de tu asistente virtual!

---

## 📝 NOTAS IMPORTANTES

### Descargas Grandes
- **Modelo Mistral**: ~4GB (puede tardar mucho en conexiones lentas)
- **Modelo Vosk**: ~50MB (descarga rápida)

### Espacio en Disco
- Asegúrate de tener al menos **5GB libres**

### Primera Ejecución
- La primera vez que uses Lily, puede tardar unos segundos en cargar los modelos

### Actualizaciones
- Si actualizas Lily, puedes ejecutar este instalador nuevamente
- Solo descargará lo que falte

---

## 🔄 REINSTALACIÓN

Si algo salió mal y quieres reinstalar:

1. **Eliminar modelos**:
   - Borrar carpeta: `models\vosk-model-small-es-0.42\`
   - Ejecutar: `ollama rm mistral`

2. **Desinstalar dependencias**:
   ```
   pip uninstall -r requirements.txt -y
   ```

3. **Ejecutar instalador nuevamente**:
   - Doble clic en `INSTALAR_TODO.bat`

---

## 📊 RESUMEN

| Característica | Estado |
|----------------|--------|
| Instalación automática | ✅ |
| Descarga de modelos | ✅ |
| Verificación de componentes | ✅ |
| Manejo de errores | ✅ |
| Resumen final | ✅ |

---

## 🎉 ¡Listo!

Después de ejecutar `INSTALAR_TODO.bat` exitosamente, tu sistema estará completamente configurado para ejecutar Lily AI con todas sus funcionalidades:

- 🎤 Reconocimiento de voz offline (Vosk)
- 🎵 Control de YouTube y medios
- 💬 Chat con IA (Mistral 7B)
- ❤️ Inteligencia emocional
- 🧠 Memoria persistente

**¡Disfruta de Lily!** 💕

