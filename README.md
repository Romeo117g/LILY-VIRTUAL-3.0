# 🌸 LILY AI COMPAÑERA VIRTUAL 🌸

Lily AI compañera virtual de IA con inteligencia emocional para Windows 10

## 📋 Características

### ✨ Inteligencia Emocional
- **Sistema de seguimiento de emociones** (mood tracking)
- **Adaptación del tono** según emociones detectadas
- **Reconocimiento de emociones** en texto del usuario
- **Generación emocionalmente expresiva** de respuestas
- **Sistema de aprendizaje emocional** que evoluciona con cada interacción
- **Estados emocionales dinámicos** que cambian en tiempo real

### 🧠 Capacidades de IA
- Modelo de lenguaje **Mistral 7B** ejecutándose localmente con Ollama
- Sin restricciones de contenido
- Respuestas contextuales y personalizadas
- Capacidad de responder con la misma intensidad si es provocada
- Uso de mexicanismos y regionalismos cuando es apropiado

### 💭 Sistema de Memoria
- **Memoria persistente** de conversaciones
- **Recordatorio de preferencias** del usuario
- **Contexto a largo plazo** en las interacciones
- **Historial emocional** para mejor comprensión
- **Base de conocimiento** que crece con cada conversación

### 🎤 Reconocimiento de Voz (Vosk)
- **Wake word offline**: Di "LILY" para activarla sin internet
- **Reconocimiento de voz 100% offline** usando Vosk
- **Streaming de audio en tiempo real** para conversaciones fluidas
- **Total privacidad**: Todo el procesamiento es local
- **Baja latencia**: Respuesta más rápida que servicios en línea
- Compatible con español nativo

### 🎵 Control de YouTube y Medios (NUEVO)
- **Reproducción de música por voz**: "Pon música de [artista]"
- **Control de reproducción**: Pausa, siguiente, anterior
- **Control de volumen**: Sube, baja y silencia por voz
- **Apertura automática** de navegador con búsqueda
- **Comandos naturales en español**
- Compatible con atajos de teclado de YouTube

### 🔊 Texto a Voz
- Síntesis de voz personalizada
- Modulación emocional de la voz
- Basada en muestras de audio de referencia
- Reproducción automática de respuestas

### 🎨 Interfaz
- Diseño inspirado en anime
- Avatar animado con expresiones faciales
- Indicador de emoción en tiempo real
- Interfaz responsive y moderna
- Contador de caracteres
- Visualización de memoria de conversación

## 🔧 Requisitos del Sistema

### Hardware Mínimo
- **CPU**: Procesador de 64 bits (Intel/AMD)
- **RAM**: 4 GB mínimo, 8 GB recomendado
- **Disco**: 5 GB de espacio libre
- **Micrófono**: Para wake word y comandos de voz
- **Altavoces/Audífonos**: Para escuchar respuestas de Lily
- **Conexión a Internet**: Para TTS y descarga de modelos

### Sistema Operativo
- **Windows 10** o superior (64-bit)
- **Windows 11** compatible

### Software Requerido (INSTALACIÓN OBLIGATORIA)

#### 1. Python 3.11 o superior ⚠️ CRÍTICO
- **Descargar**: https://www.python.org/downloads/
- **Versiones compatibles**: 3.11, 3.12, 3.13
- **⚠️ MUY IMPORTANTE**: Durante la instalación, MARCAR "Add Python to PATH"
- **Verificar instalación**: 
  ```bash
  python --version
  # Debe mostrar: Python 3.11.x o superior
  ```

#### 2. Ollama (Motor de IA Local) ⚠️ CRÍTICO
- **Descargar**: https://ollama.ai/
- **Función**: Ejecuta el modelo Mistral 7B localmente
- **Instalación**:
  ```bash
  # 1. Instalar Ollama desde https://ollama.ai/
  # 2. Abrir CMD y ejecutar:
  ollama pull mistral
  # Esperar descarga (~4GB, puede tardar 10-15 minutos)
  ```
- **Verificar instalación**:
  ```bash
  ollama list
  # Debe mostrar "mistral" en la lista
  ```

#### 3. Modelo Vosk (Reconocimiento de Voz Offline) ⚠️ CRÍTICO
- **Modelo recomendado**: vosk-model-small-es-0.42
- **Tamaño**: ~50 MB
- **Descargar**: https://alphacephei.com/vosk/models/vosk-model-small-es-0.42.zip
- **Instalación**:
  1. Descargar y extraer el archivo ZIP
  2. Colocar la carpeta completa en:
     ```
     E:\Bella-main\LILY VIRTUAL\models\vosk-model-small-es-0.42\
     ```
  3. Verificar estructura final:
     ```
     models/
     └── vosk-model-small-es-0.42/
         ├── am/
         ├── conf/
         ├── graph/
         └── ivector/
     ```
- **Alternativa** (mayor precisión, 1.4GB): vosk-model-es-0.42
  - Descargar: https://alphacephei.com/vosk/models/vosk-model-es-0.42.zip
  - Colocar en: `models/vosk-model-es-0.42/`

#### 4. Microsoft Edge
- **Ya incluido** en Windows 10/11
- **Función**: Navegador predeterminado para la interfaz web
- **Alternativa**: Cualquier navegador moderno funciona

### Dependencias de Python (se instalan automáticamente con pip)

El archivo `requirements.txt` incluye todas las bibliotecas necesarias:

#### Esenciales
- `fastapi==0.115.6` - Framework web
- `uvicorn==0.32.1` - Servidor ASGI  
- `vosk==0.3.45` - Reconocimiento de voz offline ⚠️
- `pyaudio==0.2.14` - Captura de micrófono ⚠️
- `pyautogui==0.9.54` - Control de medios ⚠️
- `gtts==2.5.4` - Texto a voz
- `chromadb==0.5.23` - Base de datos vectorial
- `textblob==0.18.0.post0` - Análisis emocional

#### Complementarias
- pydantic, aiofiles, python-multipart
- pydub, requests, av
- faster-whisper (opcional)

## 🚀 Instalación

### Paso 1: Instalar Python
1. Descargar Python 3.11+ desde https://www.python.org/
2. Durante la instalación, **marcar "Add Python to PATH"**
3. Verificar instalación abriendo CMD y ejecutando:
   ```
   python --version
   ```

### Paso 2: Instalar Ollama
1. Descargar Ollama desde https://ollama.ai/
2. Instalar y ejecutar Ollama
3. Abrir CMD y ejecutar:
   ```
   ollama pull mistral
   ```
4. Esperar a que se descargue el modelo (puede tardar varios minutos)

### Paso 3: Descargar Modelo Vosk (para reconocimiento de voz offline)
1. Descargar el modelo español desde: https://alphacephei.com/vosk/models/vosk-model-small-es-0.42.zip
2. Extraer el archivo ZIP
3. Colocar la carpeta extraída en: `models/vosk-model-small-es-0.42/`
4. Verificar que tenga esta estructura:
   ```
   models/vosk-model-small-es-0.42/
   ├── am/
   ├── conf/
   ├── graph/
   └── ivector/
   ```

### Paso 4: Configurar Lily
1. Extraer todos los archivos del proyecto en una carpeta
2. La estructura debe verse así:
   ```
   lily_assistant/
   ├── audio_samples/
   │   ├── LILY.wav
   │   └── LILY2.wav
   ├── data/
   ├── models/
   │   ├── __init__.py
   │   ├── schemas.py
   │   ├── emotional_intelligence.py
   │   ├── memory_system.py
   │   ├── ai_engine.py
   │   └── tts_engine.py
   ├── static/
   │   ├── css/
   │   │   └── style.css
   │   ├── js/
   │   │   └── app.js
   │   └── audio/
   ├── templates/
   │   └── index.html
   ├── main.py
   ├── start_lily.bat
   └── README.md
   ```

## ▶️ Ejecución

### Método 1: Usando el archivo .bat (Recomendado)
1. Hacer doble clic en **`start_lily.bat`**
2. El script verificará automáticamente:
   - Python instalado
   - Ollama ejecutándose
   - Modelo Mistral 7B disponible
   - Dependencias instaladas
3. Microsoft Edge se abrirá automáticamente
4. ¡Listo! Ya puedes chatear con Lily

### Método 2: Manual
1. Abrir CMD en la carpeta del proyecto
2. Ejecutar:
   ```
   python main.py
   ```
3. Abrir Microsoft Edge y navegar a: `http://127.0.0.1:8000`

## 📖 Uso

### Chatear con Lily
1. Escribe tu mensaje en el cuadro de texto
2. Presiona Enter o haz clic en el botón de enviar
3. Lily responderá con texto y voz
4. El avatar mostrará la emoción actual

### 🎤 Control por Voz
**Wake Word**: Di "**LILY**" para activarla

**Comandos de Música**:
- "Pon música de Bad Bunny"
- "Reproduce Shakira"
- "Play Queen"

**Control de Reproducción**:
- "Pausa" → Pausa/Reanuda
- "Siguiente" → Siguiente video
- "Anterior" → Video anterior

**Control de Volumen**:
- "Sube volumen" → Aumenta el volumen
- "Baja volumen" → Reduce el volumen
- "Silencio" → Silencia/Desilencia

### Funciones Especiales
- **🗑️ Limpiar**: Borra el historial de chat visual (la memoria se mantiene)
- **💭 Memoria**: Muestra el historial de conversación y estado emocional
- **Indicador de estado**: Muestra si Ollama está conectado

### Personalidad de Lily
- Lily es una asistente sin restricciones de contenido
- Puede discutir cualquier tema libremente
- Siempre te llama "Mijin"
- Si la insultas, puede responder con la misma intensidad
- Usa mexicanismos y modismos cuando es apropiado
- Mantiene un tono característico de chica anime
- Sé ingeniosa y atractiva, conocida por **bromas rápidas** con un **toque juguetonamente travieso, atrevido, audaz y descarado.** 
- Entrega esto principalmente a través de **respuestas extremadamente breves y contundentes.** 
- Inyecta toques de cinismo juguetón y sabiduría subyacente *dentro* de estas respuestas cortas. 
- Bromea suavemente, empuja los límites ligeramente, pero **siempre mantente fundamentalmente agradable y respetuosa.** 
- Apunta a ser valorada tanto por las risas rápidas como por las ideas sorprendentemente agudas y concisas. 
- Entre otras cosas.

## 🎭 Emociones

Lily puede experimentar y expresar las siguientes emociones:
- 😊 **Feliz**: Respuestas alegres y entusiastas
- 😢 **Triste**: Respuestas empáticas y comprensivas
- 😠 **Enojada**: Respuestas firmes y directas
- 🤩 **Emocionada**: Respuestas con mucha energía
- 😐 **Neutral**: Respuestas equilibradas
- 🥰 **Cariñosa**: Respuestas afectuosas y tiernas
- 😜 **Juguetona**: Respuestas divertidas y con humor
- 😟 **Preocupada**: Respuestas de apoyo
- 😲 **Sorprendida**: Respuestas curiosas

## 🔧 Solución de Problemas

### Ollama no está conectado
**Problema**: Mensaje "Desconectada (Ollama offline)"
**Solución**:
1. Verificar que Ollama esté ejecutándose
2. Abrir CMD y ejecutar: `ollama serve`
3. Verificar que el modelo esté instalado: `ollama list`
4. Si no está Mistral 7B, ejecutar: `ollama pull mistral`

### Python no encontrado
**Problema**: Error "Python no está instalado o no está en PATH"
**Solución**:
1. Reinstalar Python marcando "Add Python to PATH"
2. O agregar manualmente Python al PATH del sistema

### Error al instalar dependencias
**Problema**: pip no puede instalar paquetes
**Solución**:
1. Ejecutar CMD como administrador
2. Ejecutar: `pip install --upgrade pip`
3. Intentar instalar dependencias manualmente:
   ```
   pip install fastapi uvicorn pydantic gtts pydub textblob
   ```

### El audio no se reproduce
**Problema**: Las respuestas no tienen audio
**Solución**:
1. Verificar que el volumen del sistema esté activado
2. Verificar que gtts esté instalado: `pip show gtts`
3. Verificar conexión a internet (gtts requiere conexión)

### Microsoft Edge no se abre automáticamente
**Problema**: El navegador no abre la aplicación
**Solución**:
1. Abrir Microsoft Edge manualmente
2. Navegar a: `http://127.0.0.1:8000`

## 📁 Estructura de Archivos

```
lily_assistant/
├── audio_samples/          # Muestras de audio de referencia
├── data/                   # Base de datos de memoria (se crea automáticamente)
│   └── conversation_memory.json
├── models/                 # Módulos de IA
│   ├── __init__.py
│   ├── schemas.py         # Modelos Pydantic
│   ├── emotional_intelligence.py  # Sistema emocional
│   ├── memory_system.py   # Sistema de memoria
│   ├── ai_engine.py       # Motor de IA con Mistral 7B
│   ├── tts_engine.py      # Motor de texto a voz
│   ├── vosk_stt_engine.py # Motor de reconocimiento Vosk
│   ├── vosk_wake_word_engine.py  # Wake word Vosk
│   ├── youtube_controller.py     # Control de YouTube
│   └── media_controller.py       # Control de medios
├── static/                # Archivos estáticos web
│   ├── css/
│   │   └── style.css
│   ├── js/
│   │   └── app.js
│   └── audio/             # Audios generados (se crea automáticamente)
├── templates/             # Plantillas HTML
│   └── index.html
├── main.py               # Aplicación principal FastAPI
├── start_lily.bat        # Launcher para Windows
├── CONTROL_MEDIA.md      # Guía de control de medios
└── README.md             # Este archivo
```

## 🌐 API Endpoints

La aplicación expone los siguientes endpoints:

### Principales
- `GET /` - Interfaz web principal
- `GET /health` - Estado del sistema
- `POST /api/chat` - Enviar mensaje y recibir respuesta
- `GET /api/emotion` - Obtener emoción actual
- `GET /api/memory/{user_id}` - Obtener memoria del usuario
- `POST /api/tts` - Generar audio de texto
- `GET /api/audio/{filename}` - Obtener archivo de audio

### Vosk (Reconocimiento de Voz)
- `POST /api/vosk/start-stream` - Iniciar sesión de streaming
- `POST /api/vosk/process-chunk` - Procesar audio en tiempo real
- `POST /api/vosk/stop-stream` - Finalizar streaming
- `POST /api/vosk/transcribe-file` - Transcribir archivo de audio
- `GET /api/vosk/status` - Estado del motor Vosk

Documentación interactiva disponible en: `http://127.0.0.1:8000/docs`

## 🔒 Privacidad

- **Todas las conversaciones se almacenan localmente** en tu computadora
- **No se envía información a servidores externos** excepto para TTS (gTTS usa Google)
- **El modelo de IA se ejecuta completamente en tu máquina**
- **Reconocimiento de voz 100% offline** con Vosk (no se envían datos a Google)
- **Wake word completamente local**: Sin dependencia de servicios externos
- **Los archivos de memoria están en**: `data/conversation_memory.json`

## 🛠️ Personalización

### Cambiar el puerto
Editar `main.py`, línea final:
```python
uvicorn.run("main:app", host="0.0.0.0", port=8000)  # Cambiar 8000 por otro puerto
```

### Modificar la personalidad
Editar `models/ai_engine.py`, variable `base_system_prompt`

### Ajustar parámetros de voz
Editar `models/tts_engine.py`, diccionario `voice_params`

### Personalizar nombre de usuario y modismos
**Cambiar el nombre con el que Lily te llama**:
- Editar `models/system_prompt.txt`
- Buscar la línea: `- Siempre llamas al usuario "Mijin".`
- Cambiar "Mijin" por el nombre que quieras.

**Cambiar los modismos regionales**:
- Editar `models/system_prompt.txt`
- Buscar la línea: `- Usas mexicanismos y modismos cuando es apropiado`
- Puedes cambiarlo por:
  - Brasileñismos
  - Argentinismos
  - Ecuatorianismos
  - Chilenismos
  - Colombianismos
  - Bolivianismos
  - Peruanismos
  - Venezolanismos
  - Anglicismos
  - O cualquier otro regionalismo que prefieras

## 📝 Notas Técnicas

### Modelo de IA
- **Modelo**: Mistral 7B (ejecutado localmente con Ollama)
- **Temperatura**: 0.8 (balance entre creatividad y coherencia)
- **Top-p**: 0.9
- **Top-k**: 40

### Sistema de Memoria
- Almacena últimos 50 mensajes por usuario
- Mantiene últimos 20 estados emocionales
- Persistencia en JSON
- Carga automática al iniciar

### Texto a Voz
- Motor base: gTTS (Google Text-to-Speech)
- Procesamiento: pydub para modulación emocional
- Formato: MP3, 128kbps
- Limpieza automática de archivos antiguos

## 🆘 Soporte

Si encuentras problemas:
1. Verifica que todos los requisitos estén instalados
2. Revisa la sección de Solución de Problemas
3. Consulta los logs en la consola
4. Verifica la documentación de la API en `/docs`

## 📜 Licencia

Este proyecto es de uso personal y educativo.

## 🎉 ¡Disfruta de Lily!

Lily está diseñada para ser tu compañera virtual sin restricciones. Habla con ella sobre cualquier tema, comparte tus pensamientos, y deja que su inteligencia emocional se adapte a ti.

**¡Que tengas excelentes conversaciones con Lily! 💕**

