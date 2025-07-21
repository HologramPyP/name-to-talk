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
No_words= True #Indica que el usuario no a iniciado la pregunta#
last_keyword_time = time.time()

keyword  = input("Por favor, ingresa la palabra clave: ")

# Callback para capturar audio en tiempo real
def audio_callback(indata, frames, time, status):
    if status:
        print(status)
    audio_queue.put(bytes(indata))

# Función para escuchar y detectar palabra clave "Valentina"
def listen_for_keyword():
    global MicOpen, silence_start, t_pressed, last_keyword_time, No_words

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
                last_keyword_time = time.time()  # Actualizar el tiempo de la última detección
                print("¡Palabra clave detectada! MicOpen:", MicOpen)
                t_pressed = True  # Actualizar el estado a "presionada"
                keyboard.press('alt+e')
                time.sleep(0.1)
                keyboard.release('alt+e')
                keyboard.press('t')           


            # Control de silencio para desactivar MicOpen
            elif text == "" and No_words == False:  # Si no hay texto en el resultado parcial
                if MicOpen and (silence_start is None):
                    silence_start = time.time()  # Iniciar el contador de silencio
                elif MicOpen and (time.time() - silence_start >= 1):
                    MicOpen = False
                    silence_start = None
                    print("Silencio detectado. MicOpen:", MicOpen)
                    if t_pressed:
                        
                        keyboard.press('alt+q')
                        time.sleep(0.1)
                        keyboard.release('alt+q')
                        keyboard.release('t')
                        t_pressed = False
                        No_words = True


            if MicOpen and No_words:
                #print("Microfono abierto y no words")
                if time.time() -last_keyword_time >= 10:
                    MicOpen = False
                    silence_start = None
                    print("Silencio de arranque detectado. MicOpen:", MicOpen)
                    if t_pressed:
                        
                        keyboard.press('alt+q')
                        time.sleep(0.1)
                        keyboard.release('alt+q')
                        keyboard.release('t')
                        t_pressed = False
                        No_words = True
                
                # Crear lista con las palabras reconocidas
                palabras = text.split()
                # Eliminar las palabras de la lista antes de camilo
                if keyword in palabras:
                    index = palabras.index(keyword)
                    palabras = palabras[index:]
                else:
                    pass
                    #print("La palabra clave no está en la lista.")
                
                # Si en la lista esta la palabra clave y hay otras palabras, No_words = False
                if (keyword in palabras) and len(palabras)>1:
                    No_words = False
                
                # Si no es la palabra clave pero estan otras palabras entonces No_words = False
                if not (keyword in palabras) and len(palabras)>0:
                    No_words = False

  

                

            # Verificar si han pasado 60 segundos sin detectar la palabra clave
            if time.time() - last_keyword_time >= 60:
                print("60 segundos sin detectar la palabra clave. Presionando alt+1")
                keyboard.press('alt+l')
                time.sleep(0.1)
                keyboard.release('alt+l')
                last_keyword_time = time.time()  # Reiniciar el contador

# Llamar a la función para comenzar a escuchar
listen_for_keyword()
