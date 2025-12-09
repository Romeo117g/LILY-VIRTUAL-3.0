from fastapi import FastAPI, HTTPException, Request, UploadFile, File
from fastapi.responses import HTMLResponse, FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import os
from datetime import datetime

from models.ai_engine import AIEngine
from models.schemas import ChatRequest, ChatResponse, EmotionType
from models.tts_engine import TTSEngine
from models.vosk_stt_engine import VoskSTTEngine
import shutil

# Crear aplicación FastAPI
app = FastAPI(
    title="Lily virtual companion AI",
    description="Compañera virtual con inteligencia emocional",
    version="1.0.0"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Montar directorio estático
app.mount("/static", StaticFiles(directory="static"), name="static")

# Inicializar motor de IA con detección de palabra clave
ai_engine = AIEngine(enable_wake_word=True)

# Iniciar sistema de detección de palabra clave si está disponible
try:
    ai_engine.enable_wake_word_detection()
except Exception as e:
    print(f"Error iniciando detección de palabra clave: {e}")

# Inicializar motor de TTS
tts_engine = TTSEngine()

# Inicializar motor Vosk STT (offline, streaming)
vosk_stt_engine = VoskSTTEngine()

# Variable global para almacenar el último audio generado
last_audio_path = None

# Diccionario para almacenar sesiones de streaming de Vosk
vosk_sessions = {}


@app.get("/", response_class=HTMLResponse)
async def read_root():
    """Servir la página principal"""
    try:
        with open("templates/index.html", "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read())
    except FileNotFoundError:
        return HTMLResponse(content="<h1>Error: Template no encontrado</h1>", status_code=500)


@app.get("/health")
async def health_check():
    """Verificar el estado del sistema"""
    ollama_status = ai_engine.check_ollama_connection()
    
    return {
        "status": "healthy" if ollama_status else "degraded",
        "ollama_connected": ollama_status,
        "timestamp": datetime.now().isoformat()
    }


@app.post("/api/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Endpoint principal de chat"""
    try:
        # Generar respuesta
        response_text, emotion = ai_engine.generate_response(
            request.message, 
            request.user_id
        )
        
        # Generar audio con TTS
        audio_url = None
        try:
            audio_url = tts_engine.text_to_speech(response_text, emotion.value)
        except Exception as e:
            print(f"Error generando audio: {e}")
        
        # Preparar respuesta
        return ChatResponse(
            response=response_text,
            emotion=emotion.value,
            audio_url=audio_url,
            timestamp=datetime.now().isoformat()
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generando respuesta: {str(e)}")


@app.get("/api/emotion")
async def get_current_emotion():
    """Obtener la emoción actual de Lily"""
    emotional_state = ai_engine.get_emotional_state()
    
    return {
        "emotion": emotional_state.emotion.value,
        "intensity": emotional_state.intensity,
        "reason": emotional_state.reason,
        "timestamp": emotional_state.timestamp.isoformat()
    }


@app.get("/api/memory/{user_id}")
async def get_user_memory(user_id: str):
    """Obtener memoria de conversación del usuario"""
    try:
        context = ai_engine.memory_system.get_conversation_context(user_id, max_messages=10)
        summary = ai_engine.memory_system.get_conversation_summary(user_id)
        emotional_summary = ai_engine.memory_system.get_emotional_summary(user_id)
        
        return {
            "user_id": user_id,
            "conversation_summary": summary,
            "emotional_summary": emotional_summary,
            "recent_messages": context
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error obteniendo memoria: {str(e)}")


@app.post("/api/tts")
async def text_to_speech(request: Request):
    """Endpoint para texto a voz con personalización emocional"""
    data = await request.json()
    text = data.get("text", "")
    emotion = data.get("emotion", "neutral")
    
    try:
        audio_url = tts_engine.text_to_speech(text, emotion)
        return {
            "status": "success",
            "audio_url": audio_url,
            "text": text,
            "emotion": emotion
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generando audio: {str(e)}")


@app.post("/api/transcribe")
async def transcribe_audio(file: UploadFile = File(...)):
    """Endpoint para transcribir audio (Speech-to-Text) usando Vosk"""
    try:
        # Guardar archivo temporalmente
        temp_filename = f"temp_audio_{datetime.now().timestamp()}.wav"
        with open(temp_filename, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        # Transcribir con Vosk (offline)
        if vosk_stt_engine.is_available():
            text = vosk_stt_engine.transcribe_file(temp_filename)
        else:
            # Si Vosk no está disponible, informar al usuario
            os.remove(temp_filename)
            return {
                "text": "Error: Modelo Vosk no disponible. Descarga el modelo desde: https://alphacephei.com/vosk/models",
                "engine": "none"
            }
        
        # Eliminar archivo temporal
        os.remove(temp_filename)
        
        return {"text": text, "engine": "vosk"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error transcribiendo audio: {str(e)}")


@app.get("/api/audio/{filename}")
async def get_audio(filename: str):
    """Servir archivos de audio generados"""
    audio_path = os.path.join("static", "audio", filename)
    
    if os.path.exists(audio_path):
        return FileResponse(audio_path, media_type="audio/mpeg")
    else:
        raise HTTPException(status_code=404, detail="Audio no encontrado")


@app.delete("/api/audio/{filename}")
async def delete_audio(filename: str):
    """Eliminar archivo de audio después de reproducción"""
    try:
        audio_url = f"/static/audio/{filename}"
        deleted = tts_engine.delete_audio_file(audio_url)

        if deleted:
            return {"status": "success", "message": "Audio eliminado correctamente"}
        else:
            return {"status": "error", "message": "Audio no encontrado"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error eliminando audio: {str(e)}")


@app.post("/api/wake_word/enable")
async def enable_wake_word():
    """Habilitar detección de palabra clave"""
    try:
        ai_engine.enable_wake_word_detection()
        return {"status": "success", "message": "Detección de palabra clave habilitada"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error habilitando detección de palabra clave: {str(e)}")


@app.post("/api/wake_word/disable")
async def disable_wake_word():
    """Deshabilitar detección de palabra clave"""
    try:
        ai_engine.disable_wake_word_detection()
        return {"status": "success", "message": "Detección de palabra clave deshabilitada"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deshabilitando detección de palabra clave: {str(e)}")


# ====================================
# ENDPOINTS DE VOSK (RECONOCIMIENTO DE VOZ STREAMING)
# ====================================

@app.post("/api/vosk/start-stream")
async def vosk_start_stream():
    """Iniciar sesión de reconocimiento de voz en streaming con Vosk"""
    if not vosk_stt_engine.is_available():
        raise HTTPException(
            status_code=503, 
            detail="Motor Vosk no disponible. Descarga el modelo desde: https://alphacephei.com/vosk/models"
        )
    
    # Generar ID de sesión único
    import uuid
    session_id = str(uuid.uuid4())
    
    # Iniciar streaming
    if vosk_stt_engine.start_stream():
        vosk_sessions[session_id] = {
            "started": datetime.now(),
            "active": True
        }
        return {
            "status": "success",
            "session_id": session_id,
            "message": "Sesión de streaming iniciada"
        }
    else:
        raise HTTPException(status_code=500, detail="Error iniciando sesión de streaming")


@app.post("/api/vosk/process-chunk")
async def vosk_process_chunk(request: Request):
    """Procesar un chunk de audio en streaming"""
    data = await request.json()
    session_id = data.get("session_id")
    audio_data = data.get("audio_data")  # Base64 encoded audio
    
    if not session_id or session_id not in vosk_sessions:
        raise HTTPException(status_code=400, detail="Sesión inválida o expirada")
    
    if not vosk_sessions[session_id]["active"]:
        raise HTTPException(status_code=400, detail="Sesión no activa")
    
    try:
        # Decodificar audio de base64
        import base64
        audio_bytes = base64.b64decode(audio_data)
        
        # Procesar con Vosk
        result = vosk_stt_engine.process_audio_chunk(audio_bytes)
        
        return {
            "status": "success",
            "session_id": session_id,
            "result": result
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error procesando audio: {str(e)}")


@app.post("/api/vosk/stop-stream")
async def vosk_stop_stream(request: Request):
    """Finalizar sesión de streaming y obtener resultado final"""
    data = await request.json()
    session_id = data.get("session_id")
    
    if not session_id or session_id not in vosk_sessions:
        raise HTTPException(status_code=400, detail="Sesión inválida")
    
    try:
        # Obtener resultado final
        final_text = vosk_stt_engine.finish_stream()
        
        # Marcar sesión como inactiva
        vosk_sessions[session_id]["active"] = False
        
        return {
            "status": "success",
            "session_id": session_id,
            "final_text": final_text
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error finalizando sesión: {str(e)}")


@app.post("/api/vosk/transcribe-file")
async def vosk_transcribe_file(file: UploadFile = File(...)):
    """Transcribir un archivo de audio usando Vosk (offline)"""
    if not vosk_stt_engine.is_available():
        raise HTTPException(
            status_code=503,
            detail="Motor Vosk no disponible. Descarga el modelo primero."
        )
    
    try:
        # Guardar archivo temporalmente
        temp_filename = f"temp_vosk_{datetime.now().timestamp()}.wav"
        with open(temp_filename, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Transcribir con Vosk
        text = vosk_stt_engine.transcribe_file(temp_filename)
        
        # Eliminar archivo temporal
        os.remove(temp_filename)
        
        return {
            "status": "success",
            "text": text,
            "engine": "vosk"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error transcribiendo: {str(e)}")


@app.get("/api/vosk/status")
async def vosk_status():
    """Obtener estado del motor Vosk"""
    return {
        "available": vosk_stt_engine.is_available(),
        "active_sessions": len([s for s in vosk_sessions.values() if s["active"]]),
        "supported_sample_rates": vosk_stt_engine.get_supported_sample_rates(),
        "engine": "vosk"
    }


@app.get("/api/wake_word/status")
async def get_wake_word_status():
    """Obtener estado de la detección de palabra clave"""
    try:
        return {
            "enabled": ai_engine.wake_word_enabled,
            "is_listening": ai_engine.wake_word_engine.is_listening if ai_engine.wake_word_engine else False
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error obteniendo estado: {str(e)}")


if __name__ == "__main__":
    print("=" * 60)
    print("Lily virtual companion AI")
    print("=" * 60)
    print(f"Servidor iniciando en: http://127.0.0.1:8000")
    print(f"Documentación API: http://127.0.0.1:8000/docs")
    print("=" * 60)
    
    # Limpiar archivos de audio antiguos al iniciar
    print("Limpiando archivos de audio antiguos...")
    tts_engine.clean_old_audio_files(max_age_seconds=300)
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=False,
        log_level="info"
    )

