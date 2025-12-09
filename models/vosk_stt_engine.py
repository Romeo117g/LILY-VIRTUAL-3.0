import os
import json
import wave
from vosk import Model, KaldiRecognizer
import pyaudio


class VoskSTTEngine:
    """Motor de reconocimiento de voz usando Vosk para transcripción en tiempo real (offline)"""
    
    def __init__(self, model_path: str = "models/vosk-model-small-es-0.42", sample_rate: int = 16000):
        """
        Inicializa el motor Vosk
        
        Args:
            model_path: Ruta al modelo Vosk descargado
            sample_rate: Frecuencia de muestreo del audio (16000 Hz recomendado)
        """
        self.model_path = model_path
        self.sample_rate = sample_rate
        self.model = None
        self.recognizer = None
        
        # Verificar si el modelo existe
        if not os.path.exists(model_path):
            print(f"⚠️  Modelo Vosk no encontrado en: {model_path}")
            print(f"📥 Descarga el modelo desde: https://alphacephei.com/vosk/models")
            print(f"   Busca: vosk-model-small-es-0.42.zip (~50MB)")
            print(f"   Extrae y coloca en: {model_path}")
            return
        
        try:
            print(f"Cargando modelo Vosk desde {model_path}...")
            self.model = Model(model_path)
            self.recognizer = KaldiRecognizer(self.model, sample_rate)
            self.recognizer.SetWords(True)  # Habilitar timestamps de palabras
            print("✅ Modelo Vosk cargado correctamente")
        except Exception as e:
            print(f"❌ Error cargando modelo Vosk: {e}")
            self.model = None
    
    def transcribe_file(self, audio_file_path: str) -> str:
        """
        Transcribe un archivo de audio completo
        
        Args:
            audio_file_path: Ruta al archivo WAV
            
        Returns:
            Texto transcrito
        """
        if not self.model:
            return "Error: Modelo Vosk no cargado. Descarga el modelo primero."
        
        if not os.path.exists(audio_file_path):
            return "Error: Archivo de audio no encontrado."
        
        try:
            with wave.open(audio_file_path, "rb") as wf:
                # Verificar formato de audio
                if wf.getnchannels() != 1 or wf.getsampwidth() != 2:
                    return "Error: El audio debe ser mono (1 canal) con 16-bit samples"
                
                if wf.getframerate() != self.sample_rate:
                    print(f"⚠️  Advertencia: Sample rate {wf.getframerate()} Hz diferente del esperado {self.sample_rate} Hz")
                
                # Crear reconocedor para esta sesión
                rec = KaldiRecognizer(self.model, wf.getframerate())
                rec.SetWords(True)
                
                # Procesar audio en chunks
                results = []
                while True:
                    data = wf.readframes(4000)
                    if len(data) == 0:
                        break
                    
                    if rec.AcceptWaveform(data):
                        result = json.loads(rec.Result())
                        if "text" in result and result["text"]:
                            results.append(result["text"])
                
                # Obtener resultado final
                final_result = json.loads(rec.FinalResult())
                if "text" in final_result and final_result["text"]:
                    results.append(final_result["text"])
                
                return " ".join(results).strip()
                
        except Exception as e:
            return f"Error transcribiendo: {str(e)}"
    
    def start_stream(self):
        """Inicia una sesión de reconocimiento en streaming"""
        if not self.model:
            return False
        
        # Crear nuevo reconocedor para streaming
        self.recognizer = KaldiRecognizer(self.model, self.sample_rate)
        self.recognizer.SetWords(True)
        return True
    
    def process_audio_chunk(self, audio_data: bytes) -> dict:
        """
        Procesa un chunk de audio en streaming
        
        Args:
            audio_data: Bytes de audio raw (16-bit PCM)
            
        Returns:
            Dict con 'partial' (texto parcial) o 'final' (texto final del chunk)
        """
        if not self.recognizer:
            return {"error": "Reconocedor no inicializado"}
        
        try:
            if self.recognizer.AcceptWaveform(audio_data):
                # Resultado final de este chunk
                result = json.loads(self.recognizer.Result())
                return {
                    "final": result.get("text", ""),
                    "confidence": result.get("confidence", 0.0)
                }
            else:
                # Resultado parcial (en progreso)
                partial_result = json.loads(self.recognizer.PartialResult())
                return {
                    "partial": partial_result.get("partial", "")
                }
        except Exception as e:
            return {"error": str(e)}
    
    def finish_stream(self) -> str:
        """
        Finaliza la sesión de streaming y obtiene el resultado final
        
        Returns:
            Texto transcrito final
        """
        if not self.recognizer:
            return ""
        
        try:
            final_result = json.loads(self.recognizer.FinalResult())
            return final_result.get("text", "")
        except Exception as e:
            print(f"Error obteniendo resultado final: {e}")
            return ""
    
    def is_available(self) -> bool:
        """Verifica si el motor está disponible y listo para usar"""
        return self.model is not None
    
    def get_supported_sample_rates(self) -> list:
        """Retorna las frecuencias de muestreo soportadas"""
        return [8000, 16000, 32000, 48000]


# Función de utilidad para capturar audio desde el micrófono
def record_audio_stream(duration_seconds: int = 5, sample_rate: int = 16000):
    """
    Graba audio desde el micrófono para testing
    
    Args:
        duration_seconds: Duración de la grabación
        sample_rate: Frecuencia de muestreo
        
    Returns:
        Bytes de audio grabado
    """
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    
    audio = pyaudio.PyAudio()
    
    try:
        stream = audio.open(
            format=FORMAT,
            channels=CHANNELS,
            rate=sample_rate,
            input=True,
            frames_per_buffer=CHUNK
        )
        
        print(f"🎤 Grabando {duration_seconds} segundos...")
        frames = []
        
        for _ in range(0, int(sample_rate / CHUNK * duration_seconds)):
            data = stream.read(CHUNK)
            frames.append(data)
        
        print("✅ Grabación completada")
        
        stream.stop_stream()
        stream.close()
        
        return b''.join(frames)
        
    finally:
        audio.terminate()
