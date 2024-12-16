import sounddevice as sd
import queue
import json
import time
import keyboard
from vosk import Model, KaldiRecognizer

# Ruta al modelo de idioma en español descargado y descomprimido
MODEL_PATH = "vosk-model-small-es-0.42"

# Inicializar el modelo y variables de control
model = Model(MODEL_PATH)
recognizer = KaldiRecognizer(model, 16000)
audio_queue = queue.Queue()
MicOpen = False
silence_start = None
t_pressed = False

keyword = "carlos"

# Callback para capturar audio en tiempo real
def audio_callback(indata, frames, time, status):
    if status:
        print(status)
    audio_queue.put(bytes(indata))

# Función para escuchar y detectar palabra clave "Valentina"
def listen_for_keyword():
    global MicOpen, silence_start, t_pressed

    print("Calibrando para el ruido ambiental... Un momento")
    with sd.RawInputStream(samplerate=16000, blocksize=8000, dtype="int16",
                           channels=1, callback=audio_callback):
        print("Esperando la palabra ...")

        while True:
            data = audio_queue.get()

            if recognizer.AcceptWaveform(data):
                result = recognizer.Result()
                text = json.loads(result).get("text", "")
            else:
                partial_result = recognizer.PartialResult()
                text = json.loads(partial_result).get("partial", "")

            print("Texto reconocido:", text)

            # Verificar si se dijo el nombre
            if keyword in text.lower() and not t_pressed:
                MicOpen = True
                silence_start = None  # Restablecer el contador de silencio
                print("¡Palabra clave detectada! MicOpen:", MicOpen)
                t_pressed = True  # Actualizar el estado a "presionada"
                keyboard.press('alt+e')
                time.sleep(0.1)
                keyboard.release('alt+e')
                keyboard.press('t')

            # Control de silencio para desactivar MicOpen
            elif text == "":  # Si no hay texto en el resultado parcial
                if MicOpen and (silence_start is None):
                    silence_start = time.time()  # Iniciar el contador de silencio
                elif MicOpen and (time.time() - silence_start >= 2):
                    MicOpen = False
                    silence_start = None
                    print("Silencio detectado. MicOpen:", MicOpen)
                    if t_pressed:
                        t_pressed = False
                        keyboard.press('alt+q')
                        time.sleep(0.1)
                        keyboard.release('alt+q')
                        keyboard.release('t')

# Llamar a la función para comenzar a escuchar
listen_for_keyword()
