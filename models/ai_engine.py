import requests
import json
import os
from typing import List, Dict, Optional
from models.emotional_intelligence import EmotionalIntelligence
from models.memory_system import MemorySystem
from models.rag_engine import RAGEngine
from models.schemas import EmotionType
from models.vosk_wake_word_engine import VoskWakeWordEngine
from models.youtube_controller import YouTubeController
from models.media_controller import MediaController


class AIEngine:
    """Motor de IA que integra Mistral 7B con inteligencia emocional y memoria"""
    
    def __init__(self, ollama_url: str = "http://127.0.0.1:11434", enable_wake_word: bool = False):
        """
        Inicializa el motor de IA
        
        Args:
            ollama_url: URL del servidor Ollama
            enable_wake_word: Habilitar detección de wake word usando Vosk (offline)
        """
        self.ollama_url = ollama_url
        self.model = "mistral:7b"     # LLM empleado mistral:7b
        self.emotional_intelligence = EmotionalIntelligence()
        self.memory_system = MemorySystem()
        try:
            self.rag_engine = RAGEngine()
        except Exception as e:
            print(f"Advertencia: No se pudo iniciar RAG Engine: {e}")
            self.rag_engine = None

        # Inicializar controladores de YouTube y Media
        self.youtube_controller = YouTubeController()
        self.media_controller = MediaController()
        print("✅ Controladores de YouTube y Media inicializados")

        # Iniciar sistema de detección de palabra clave con Vosk (SOLO VOSK)
        self.wake_word_enabled = enable_wake_word
        self.wake_word_engine = None
        
        if self.wake_word_enabled:
            try:
                # Usar SOLO Vosk (100% offline)
                self.wake_word_engine = VoskWakeWordEngine(
                    wake_word_callback=self.on_wake_word_detected, 
                    wake_word="LILY"
                )
                if self.wake_word_engine.is_available():
                    print("✅ Sistema de wake word Vosk (OFFLINE) iniciado correctamente")
                else:
                    print("❌ Modelo Vosk no encontrado. Descarga el modelo desde:")
                    print("   https://alphacephei.com/vosk/models/vosk-model-small-es-0.42.zip")
                    print("   Extrae y coloca en: models/vosk-model-small-es-0.42/")
                    self.wake_word_engine = None
                    self.wake_word_enabled = False
                    
            except Exception as e:
                print(f"❌ Error iniciando sistema de palabra clave Vosk: {e}")
                self.wake_word_engine = None
                self.wake_word_enabled = False

        # Cargar system prompt desde archivo
        try:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            prompt_path = os.path.join(current_dir, "system_prompt.txt")
            with open(prompt_path, "r", encoding="utf-8") as f:
                self.base_system_prompt = f.read()
        except Exception as e:
            print(f"Error cargando system_prompt.txt: {e}")
            # Fallback en caso de error
            print(f"La IA no tiene system prompt")
            self.base_system_prompt = ""
    
    def check_ollama_connection(self) -> bool:
        """Verifica la conexión con Ollama"""
        try:
            response = requests.get(f"{self.ollama_url}/api/tags", timeout=5)
            return response.status_code == 200
        except:
            return False

    def enable_wake_word_detection(self):
        """Habilita la detección de palabra clave"""
        if self.wake_word_enabled and self.wake_word_engine:
            self.wake_word_engine.start_listening()
            print("Detección de palabra clave habilitada")

    def disable_wake_word_detection(self):
        """Deshabilita la detección de palabra clave"""
        if self.wake_word_enabled and self.wake_word_engine:
            self.wake_word_engine.stop_listening()
            print("Detección de palabra clave deshabilitada")

    def on_wake_word_detected(self):
        """Callback cuando se detecta la palabra clave"""
        print("¡Palabra clave 'LILY' detectada!")
        # Aquí puedes implementar la lógica que desees cuando se detecte la palabra clave
        # Por ejemplo, iniciar grabación de audio, mostrar una notificación, etc.
        # Por ejemplo, podrías generar una respuesta de activación
        try:
            response_text = "¡Hola! Como estas el dia de hoy?."
            # Aquí podrías generar un audio de respuesta de activación si lo deseas
            # Por ejemplo: audio_url = self.tts_engine.text_to_speech(response_text, emotion="neutral")
            print(f"Lily responde: {response_text}")
        except Exception as e:
            print(f"Error en la respuesta de activación: {e}")
    
    def process_media_command(self, user_message: str) -> tuple[bool, str]:
        """
        Detecta y ejecuta comandos de control de medios
        
        Returns:
            (comando_detectado, mensaje_respuesta)
        """
        message_lower = user_message.lower()
        
        # Detectar comandos de reproducción de música
        music_keywords = ["pon música", "reproduce", "ponme música", "play", "escuchar", "música de"]
        if any(keyword in message_lower for keyword in music_keywords):
            # Extraer qué música buscar
            query = self._extract_music_query(user_message)
            if query:
                result = self.youtube_controller.search_and_play(query)
                if result["status"] == "success":
                    return True, f"¡Claro Mijin! Buscando {query} en YouTube 🎵"
                else:
                    return True, f"Ay Mijin, hubo un error: {result['message']}"
        
        # Detectar comando de pausa
        if any(word in message_lower for word in ["pausa", "pause", "detén", "para"]):
            result = self.media_controller.pause_play()
            if result["status"] == "success":
                return True, "¡Listo Mijin! Pausado/Reproduciendo 🎵"
            else:
                return True, f"Ups, no pude pausar: {result['message']}"
        
        # Detectar comando de siguiente
        if any(word in message_lower for word in ["siguiente", "next", "skip", "salta"]):
            result = self.media_controller.next_video()
            if result["status"] == "success":
                return True, "¡Siguiente video Mijin! ⏭️"
            else:
                return True, f"No pude cambiar: {result['message']}"
        
        # Detectar comando de anterior
        if any(word in message_lower for word in ["anterior", "previous", "atrás", "regresa"]):
            result = self.media_controller.previous_video()
            if result["status"] == "success":
                return True, "¡Video anterior Mijin! ⏮️"
            else:
                return True, f"No pude regresar: {result['message']}"
        
        # Detectar comando de subir volumen
        if any(word in message_lower for word in ["sube volumen", "más volumen", "volumen arriba", "sube el volumen"]):
            result = self.media_controller.volume_up(steps=3)
            if result["status"] == "success":
                return True, "¡Volumen subido Mijin! 🔊"
            else:
                return True, f"No pude subir el volumen: {result['message']}"
        
        # Detectar comando de bajar volumen
        if any(word in message_lower for word in ["baja volumen", "menos volumen", "volumen abajo", "baja el volumen"]):
            result = self.media_controller.volume_down(steps=3)
            if result["status"] == "success":
                return True, "¡Volumen bajado Mijin! 🔉"
            else:
                return True, f"No pude bajar el volumen: {result['message']}"
        
        # Detectar comando de silencio
        if any(word in message_lower for word in ["silencio", "mute", "calla"]):
            result = self.media_controller.mute_unmute()
            if result["status"] == "success":
                return True, "¡Silencio activado/desactivado Mijin! 🔇"
            else:
                return True, f"No pude silenciar: {result['message']}"
        
        return False, ""
    
    def _extract_music_query(self, message: str) -> str:
        """
        Extrae la consulta de música del mensaje del usuario
        """
        message_lower = message.lower()
        
        # Remover palabras clave y obtener el query
        keywords = [
            "pon música de", "pon música", "ponme música de", "ponme música",
            "reproduce", "play", "escuchar", "música de", "pon", "ponme"
        ]
        
        for keyword in keywords:
            if keyword in message_lower:
                # Obtener todo lo que viene después del keyword
                parts = message_lower.split(keyword, 1)
                if len(parts) > 1:
                    query = parts[1].strip()
                    if query:
                        return query
        
        # Si no se encontró keyword, devolver el mensaje completo
        return message.strip()
    
    def build_prompt(self, user_message: str, user_id: str) -> List[Dict[str, str]]:
        """Construye el prompt con contexto emocional y memoria"""
        
        # Actualizar estado emocional
        emotional_state = self.emotional_intelligence.update_emotional_state(user_message)
        self.memory_system.add_emotional_state(user_id, emotional_state)
        
        # Obtener modificador emocional
        emotional_modifier = self.emotional_intelligence.get_emotional_modifier()
        
        # Obtener contexto de conversación
        conversation_context = self.memory_system.get_conversation_context(user_id, max_messages=6)
        emotional_summary = self.memory_system.get_emotional_summary(user_id)
        conversation_summary = self.memory_system.get_conversation_summary(user_id)
        
        # Obtener contexto RAG
        rag_context = ""
        if self.rag_engine:
            rag_docs = self.rag_engine.query(user_message, n_results=2)
            if rag_docs:
                rag_context = "INFORMACIÓN RELEVANTE RECUPERADA:\n" + "\n".join(rag_docs) + "\n"

        # Construir system prompt con contexto
        system_prompt = f"""{self.base_system_prompt}

CONTEXTO EMOCIONAL ACTUAL:
{emotional_modifier}
Tu emoción actual: {emotional_state.emotion.value} (intensidad: {emotional_state.intensity:.2f})
Razón: {emotional_state.reason}

MEMORIA DE CONVERSACIÓN:
{conversation_summary}
{emotional_summary}
{rag_context}"""
        
        # Construir mensajes
        messages = [{"role": "system", "content": system_prompt}]
        
        # Agregar contexto de conversación previa
        for msg in conversation_context:
            messages.append({
                "role": msg["role"],
                "content": msg["content"]
            })
        
        # Agregar mensaje actual del usuario
        messages.append({"role": "user", "content": user_message})
        
        return messages
    
    def generate_response(self, user_message: str, user_id: str = "default_user") -> tuple[str, EmotionType]:
        """Genera una respuesta usando Mistral 7B con contexto emocional"""
        
        try:
            # PRIMERO: Verificar si es un comando de medios (música, volumen, etc.)
            is_media_command, media_response = self.process_media_command(user_message)
            if is_media_command:
                # Es un comando de medios, retornar respuesta directa
                return media_response, EmotionType.EMOCIONADA
            
            # SI NO es comando de medios, procesar normalmente con el LLM
            # Construir prompt con contexto
            messages = self.build_prompt(user_message, user_id)
            
            # Llamar a Ollama
            response = requests.post(
                f"{self.ollama_url}/api/chat",
                json={
                    "model": self.model,
                    "messages": messages,
                    "stream": False,
                    "options": {
                        "temperature": 0.8,
                        "top_p": 0.9,
                        "top_k": 40
                    }
                },
                timeout=60
            )
            
            if response.status_code == 200:
                result = response.json()
                assistant_response = result["message"]["content"]
                
                # Eliminar bloques de pensamiento <think>...</think>
                import re
                assistant_response = re.sub(r'<think>.*?</think>', '', assistant_response, flags=re.DOTALL)
                assistant_response = assistant_response.strip()
                
                # Guardar en memoria
                self.memory_system.add_message(user_id, "user", user_message)
                self.memory_system.add_message(
                    user_id, 
                    "assistant", 
                    assistant_response, 
                    self.emotional_intelligence.current_state.emotion.value
                )
                
                # Guardar en RAG
                if self.rag_engine:
                    self.rag_engine.add_conversation_turn(user_message, assistant_response)
                
                return assistant_response, self.emotional_intelligence.current_state.emotion
            else:
                return f"Error al conectar con el modelo: {response.status_code}", EmotionType.NEUTRAL
                
        except requests.exceptions.Timeout:
            return "Lo siento Mijin, estoy tardando mucho en pensar... ¿Podrías repetir eso?", EmotionType.PREOCUPADA
        except Exception as e:
            return f"Ay Mijin, algo salió mal: {str(e)}", EmotionType.PREOCUPADA
    
    def get_current_emotion(self) -> EmotionType:
        """Obtiene la emoción actual"""
        return self.emotional_intelligence.current_state.emotion
    
    def get_emotional_state(self):
        """Obtiene el estado emocional completo"""
        return self.emotional_intelligence.current_state


