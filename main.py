import sounddevice as sd
import queue
import json
import time
import keyboard
from vosk import Model, KaldiRecognizer
import socket
import threading

is_talking = False

# Ruta al modelo de idioma en español descargado y descomprimido
MODEL_PATH = "vosk-model-small-es-0.42"

# Inicializar el modelo y variables de control
model = Model(MODEL_PATH)
recognizer = KaldiRecognizer(model, 16000)
audio_queue = queue.Queue()
MicOpen = False
silence_start = None
t_pressed = False

# Inicializa para saber cuando el avatar está hablando
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', 5000))
server_socket.listen(1)

# Callback para capturar audio en tiempo real
def audio_callback(indata, frames, time, status):
    if status:
        print(status)
    audio_queue.put(bytes(indata))

def isAvatarTalking():
    global is_talking
    while True:
        client_socket, addr = server_socket.accept()
        with client_socket:
            data = client_socket.recv(1024)
            if data:
                is_talking = data.decode('utf-8') == 'True'
                print(f'El personaje está hablando: {is_talking}')
            else:
                is_talking = is_talking  # Se mantiene

# Función para escuchar y detectar palabra clave "Valentina"
def listen_for_keyword():
    global MicOpen, silence_start, t_pressed, is_talking

    print("Calibrando para el ruido ambiental... Un momento")
    with sd.RawInputStream(samplerate=16000, blocksize=8000, dtype="int16",
                           channels=1, callback=audio_callback):
        print("Esperando la palabra 'Euro'...")

        while True:
            if is_talking:
                # Limpiar la cola de audio para evitar procesamiento de fragmentos antiguos
                while not audio_queue.empty():
                    audio_queue.get()
                continue

            data = audio_queue.get()

            if recognizer.AcceptWaveform(data):
                result = recognizer.Result()
                text = json.loads(result).get("text", "")
            else:
                partial_result = recognizer.PartialResult()
                text = json.loads(partial_result).get("partial", "")

            print("Texto reconocido:", text)

            # Verificar si se dijo el nombre
            if "euro" in text.lower() and not t_pressed:
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

# Iniciar el hilo para el servidor
server_thread = threading.Thread(target=isAvatarTalking)
server_thread.daemon = True  # Termina al cerrar el programa
server_thread.start()

# Llamar a la función para comenzar a escuchar
listen_for_keyword()
