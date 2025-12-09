# 🎵 Control de YouTube y Medios - Guía de Uso

## 🎯 Funcionalidades Implementadas

Lily ahora puede controlar YouTube y los medios de tu sistema usando comandos de voz.

---

## 🎤 Comandos Disponibles

### Reproducir Música en YouTube

**Comandos**:
- "Pon música de [artista/canción]"
- "Reproduce [artista/canción]"
- "Play [artista/canción]"
- "Ponme música de [artista/canción]"
- "Escuchar [artista/canción]"

**Ejemplos**:
```
Usuario: "LILY, pon música de Juan Gabriel"
Lily: "¡Claro Mijin! Buscando Juan Gabriel en YouTube 🎵"
→ Se abre Microsoft Edge con la búsqueda en YouTube

Usuario: "Reproduce Bohemian Rhapsody"
Lily: "¡Claro Mijin! Buscando Bohemian Rhapsody en YouTube 🎵"
```

---

### Control de Reproducción

#### Pausar/Reanudar
**Comandos**: `pausa`, `pause`, `detén`, `para`

```
Usuario: "pausa"
Lily: "¡Listo Mijin! Pausado/Reproduciendo 🎵"
→ Presiona la tecla Espacio
```

#### Siguiente Video
**Comandos**: `siguiente`, `next`, `skip`, `salta`

```
Usuario: "siguiente"
Lily: "¡Siguiente video Mijin! ⏭️"
→ Presiona Shift+N (atajo de YouTube)
```

#### Video Anterior
**Comandos**: `anterior`, `previous`, `atrás`, `regresa`

```
Usuario: "anterior"
Lily: "¡Video anterior Mijin! ⏮️"
→ Presiona Shift+P (atajo de YouTube)
```

---

### Control de Volumen

#### Subir Volumen
**Comandos**: `sube volumen`, `más volumen`, `volumen arriba`, `sube el volumen`

```
Usuario: "sube volumen"
Lily: "¡Volumen subido Mijin! 🔊"
→ Aumenta 3 pasos el volumen del sistema
```

#### Bajar Volumen
**Comandos**: `baja volumen`, `menos volumen`, `volumen abajo`, `baja el volumen`

```
Usuario: "baja volumen"  
Lily: "¡Volumen bajado Mijin! 🔉"
→ Reduce 3 pasos el volumen del sistema
```

#### Silenciar
**Comandos**: `silencio`, `mute`, `calla`

```
Usuario: "silencio"
Lily: "¡Silencio activado/desactivado Mijin! 🔇"
→ Activa/Desactiva el silencio del sistema
```

---

## 🏗️ Cómo Funciona

### Flujo Completo

```
1. Usuario: "LILY" (wake word)
   ↓
2. Lily activa reconocimiento de voz
   ↓
3. Usuario: "pon música de Juan Gabriel"
   ↓
4. ai_engine.py detecta comando de música
   ↓
5. youtube_controller.py abre YouTube con búsqueda
   ↓
6. Lily responde: "¡Claro Mijin! Buscando Bad Bunny en YouTube 🎵"
```

### Para Comandos de Control

```
Video reproduciendo en YouTube
   ↓
Usuario: "pausa"
   ↓
media_controller.py presiona tecla Espacio
   ↓
Video se pausa
```

---

## 📋 Archivos Creados

### 1. `youtube_controller.py`
Control de YouTube:
- `search_and_play(query)` - Busca y abre YouTube
- `play_direct_video(video_id)` - Reproduce video específico
- `search_music(artist, song)` - Búsqueda con artista/canción

### 2. `media_controller.py`
Control de medios:
- `pause_play()` - Pausar/Reanudar (Espacio)
- `next_video()` - Siguiente (Shift+N)
- `previous_video()` - Anterior (Shift+P)
- `volume_up(steps)` - Subir volumen
- `volume_down(steps)` - Bajar volumen
- `mute_unmute()` - Silenciar
- `fullscreen()` - Pantalla completa (F)

### 3. Modificaciones en `ai_engine.py`
- `process_media_command()` - Detecta comandos
- `_extract_music_query()` - Extrae búsqueda de música
- Integración en `generate_response()`

---

## 🎮 Atajos de Teclado Usados

### YouTube
- **Espacio**: Pausar/Reproducir
- **Shift+N**: Siguiente video
- **Shift+P**: Video anterior
- **F**: Pantalla completa

### Sistema
- **VolumeUp**: Subir volumen
- **VolumeDown**: Bajar volumen
- **VolumeMute**: Silenciar

---

## 🔧 Requisitos Técnicos

### Dependencias
```txt
pyautogui==0.9.54  # Control de teclado y mouse
```

### Instalación
```bash
pip install pyautogui
```

Ya instalado automáticamente en:
- ✅ Python 3.13 (para INICIAR_LILY.bat)
- ✅ Miniconda environment

---

## ⚡ Ejemplos de Uso Completos

### Ejemplo 1: Sesión de Música
```
Usuario: "LILY"
Lily: "¡Hola! ¿Cómo estás?"

Usuario: "pon música de Shakira"
Lily: "¡Claro Mijin! Buscando Shakira en YouTube 🎵"
[Se abre YouTube con Shakira]

Usuario: "siguiente"
Lily: "¡Siguiente video Mijin! ⏭️"
[Cambia al siguiente video]

Usuario: "sube volumen"
Lily: "¡Volumen subido Mijin! 🔊"
[Aumenta el volumen]
```

### Ejemplo 2: Control Rápido
```
Usuario: "pausa" (mientras algo está reproduciéndose)
Lily: "¡Listo Mijin! Pausado/Reproduciendo 🎵"

Usuario: "baja volumen"
Lily: "¡Volumen bajado Mijin! 🔉"
```

---

## 🐛 Troubleshooting

### "No se abre YouTube"
- Verifica que tengas conexión a internet
- Asegúrate de que Microsoft Edge esté instalado
- El navegador predeterminado se abrirá automáticamente

### "Los atajos de teclado no funcionan"
- Asegúrate de que la ventana de YouTube esté en foco (activa)
- Verifica que pyautogui esté instalado correctamente
- En Windows, puede requerir permisos de accesibilidad

### "El volumen no cambia"
- pyautogui usa las teclas del sistema
- Funciona en Windows, Mac y Linux
- Verifica que tu teclado tenga teclas de volumen funcionales

---

## 🚀 Mejoras Futuras Posibles

1. **YouTube API Integration**
   - Buscar videos específicos más precisos
   - Control directo de reproducción

2. **Playlists**
   - "Crea una playlist de..."
   - "Reproduce mi playlist de..."

3. **Spotify/Apple Music**
   - Integración con otros servicios
   - Control de Spotify local

4. **Comandos Adicionales**
   - "Adelanta 10 segundos"
   - "Retrocede 10 segundos"
   - "Activa subtítulos"

---

## ✅ Resumen

- ✅ Reproducción de música en YouTube
- ✅ Control de pausa/reproducción
- ✅ Navegación entre videos (siguiente/anterior)
- ✅ Control de volumen del sistema (subir/bajar/silenciar)
- ✅ Respuestas naturales de Lily
- ✅ 100% integrado con wake word

**¡Lily ahora es tu DJ personal!** 🎵🎉
