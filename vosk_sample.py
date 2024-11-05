import sounddevice as sd
import queue
import json
from vosk_sample import Model, KaldiRecognizer

# Ruta al modelo de idioma en español descargado y descomprimido
MODEL_PATH = "vosk-model-small-es-0.42"

# Cargar el modelo de idioma
model = Model(MODEL_PATH)
recognizer = KaldiRecognizer(model, 16000)
audio_queue = queue.Queue()

# Función para procesar el audio y convertirlo a texto en tiempo real
def audio_callback(indata, frames, time, status):
    if status:
        print(status)
    # Agregar el audio recibido a la cola
    audio_queue.put(bytes(indata))

# Configuración y apertura del flujo de audio
def realtime_speech_to_text():
    with sd.RawInputStream(samplerate=16000, blocksize=8000, dtype="int16",
                           channels=1, callback=audio_callback):
        print("Comienza a hablar...")

        while True:
            # Procesar el audio en la cola
            data = audio_queue.get()
            if recognizer.AcceptWaveform(data):
                result = recognizer.Result()
                text = json.loads(result).get("text", "")
                print("Texto reconocido:", text)
            else:
                partial_result = recognizer.PartialResult()
                partial_text = json.loads(partial_result).get("partial", "")
                print("Reconociendo (parcial):", partial_text)

# Llamada a la función
realtime_speech_to_text()
