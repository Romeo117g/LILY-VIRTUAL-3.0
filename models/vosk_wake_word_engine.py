import os
import json
import threading
import time
import pyaudio
from typing import Callable, Optional
from vosk import Model, KaldiRecognizer


class VoskWakeWordEngine:
    """Motor de detección de wake word usando Vosk (100% offline)"""
    
    def __init__(
        self, 
        wake_word_callback: Optional[Callable] = None, 
        wake_word: str = "LILY",
        model_path: str = "models/vosk-model-small-es-0.42",
        sample_rate: int = 16000
    ):
        """
        Inicializa el motor de detección de wake word con Vosk
        
        Args:
            wake_word_callback: Función a llamar cuando se detecta la palabra clave
            wake_word: Palabra clave a detectar
            model_path: Ruta al modelo Vosk
            sample_rate: Frecuencia de muestreo
        """
        self.wake_word_callback = wake_word_callback
        self.wake_word = wake_word.lower()  # Normalizar a minúsculas
        self.model_path = model_path
        self.sample_rate = sample_rate
        
        self.is_listening = False
        self.listening_thread = None
        self.model = None
        self.recognizer = None
        
        # Configuración de audio
        self.CHUNK = 4000  # Tamaño de chunk para procesamiento
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = 1
        
        # Verificar si el modelo existe
        if not os.path.exists(model_path):
            print(f"⚠️  Modelo Vosk no encontrado en: {model_path}")
            print(f"📥 Descarga el modelo desde: https://alphacephei.com/vosk/models")
            print(f"   Busca: vosk-model-small-es-0.42.zip (~50MB)")
            print(f"   Extrae y coloca en: {model_path}")
            return
        
        # Cargar modelo
        try:
            print(f"Cargando modelo Vosk para wake word...")
            self.model = Model(model_path)
            print("✅ Modelo Vosk cargado para wake word detection")
        except Exception as e:
            print(f"❌ Error cargando modelo Vosk: {e}")
            self.model = None
    
    def start_listening(self):
        """Comienza a escuchar la palabra clave"""
        if not self.model:
            print("❌ Modelo no disponible. Descarga el modelo Vosk primero.")
            return
        
        if self.is_listening:
            print("⚠️  La escucha de wake word ya está activa")
            return
        
        self.is_listening = True
        self.listening_thread = threading.Thread(target=self._listen_loop)
        self.listening_thread.daemon = True
        self.listening_thread.start()
        print(f"👂 Escuchando palabra clave '{self.wake_word.upper()}' (Vosk - OFFLINE)...")
    
    def stop_listening(self):
        """Detiene la escucha de la palabra clave"""
        self.is_listening = False
        if self.listening_thread:
            self.listening_thread.join(timeout=2)
        print("🛑 Escucha de wake word detenida")
    
    def _listen_loop(self):
        """Bucle principal de escucha usando Vosk"""
        audio = pyaudio.PyAudio()
        stream = None
        
        try:
            # Abrir stream de audio
            stream = audio.open(
                format=self.FORMAT,
                channels=self.CHANNELS,
                rate=self.sample_rate,
                input=True,
                frames_per_buffer=self.CHUNK
            )
            
            # Crear reconocedor
            rec = KaldiRecognizer(self.model, self.sample_rate)
            rec.SetWords(False)  # No necesitamos timestamps para wake word
            
            print(f"🎤 Micrófono activo. Di '{self.wake_word.upper()}' para activar a Lily...")
            
            while self.is_listening:
                try:
                    # Leer datos del micrófono
                    data = stream.read(self.CHUNK, exception_on_overflow=False)
                    
                    # Procesar con Vosk
                    if rec.AcceptWaveform(data):
                        # Resultado completo
                        result = json.loads(rec.Result())
                        text = result.get("text", "").lower()
                        
                        if text:
                            print(f"🔊 Detectado: '{text}'")
                            
                            # Verificar si contiene la palabra clave
                            if self.wake_word in text:
                                print(f"✨ ¡Wake word '{self.wake_word.upper()}' detectada!")
                                if self.wake_word_callback:
                                    self.wake_word_callback()
                                
                                # Pequeño delay para evitar detecciones múltiples
                                time.sleep(2)
                                
                                # Reiniciar reconocedor
                                rec = KaldiRecognizer(self.model, self.sample_rate)
                                rec.SetWords(False)
                    else:
                        # Resultado parcial (opcional: para debugging)
                        partial = json.loads(rec.PartialResult())
                        partial_text = partial.get("partial", "").lower()
                        
                        # Verificar en resultado parcial también
                        if partial_text and self.wake_word in partial_text:
                            print(f"✨ ¡Wake word '{self.wake_word.upper()}' detectada (parcial)!")
                            if self.wake_word_callback:
                                self.wake_word_callback()
                            
                            time.sleep(2)
                            rec = KaldiRecognizer(self.model, self.sample_rate)
                            rec.SetWords(False)
                
                except OSError as e:
                    # Error de audio (buffer overflow, etc)
                    if self.is_listening:
                        print(f"⚠️  Error de audio: {e}")
                        time.sleep(0.1)
                    continue
                except Exception as e:
                    if self.is_listening:
                        print(f"❌ Error en detección: {e}")
                        time.sleep(0.5)
                    continue
        
        except Exception as e:
            print(f"❌ Error crítico en wake word loop: {e}")
        
        finally:
            # Limpiar recursos
            if stream:
                stream.stop_stream()
                stream.close()
            audio.terminate()
            print("🔇 Stream de audio cerrado")
    
    def set_callback(self, callback: Callable):
        """Establece la función de callback para cuando se detecta la palabra clave"""
        self.wake_word_callback = callback
    
    def is_available(self) -> bool:
        """Verifica si el motor está disponible"""
        return self.model is not None
    
    def __del__(self):
        """Limpieza de recursos"""
        self.stop_listening()


# Test simple
if __name__ == "__main__":
    def on_wake_word_detected():
        print("🎉 ¡LILY detectada!Callback ejecutado.")
    
    print("=== Test de Vosk Wake Word Engine ===")
    print("Di 'LILY' para probar la detección")
    print("Presiona Ctrl+C para salir\n")
    
    engine = VoskWakeWordEngine(wake_word_callback=on_wake_word_detected)
    
    if engine.is_available():
        engine.start_listening()
        
        try:
            # Mantener el programa corriendo
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n\n👋 Deteniendo...")
            engine.stop_listening()
    else:
        print("❌ Motor no disponible. Descarga el modelo Vosk.")
