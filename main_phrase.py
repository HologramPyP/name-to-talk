import speech_recognition as sr
import time
import keyboard

# Inicializar el recognizer y la variable MicOpen
recognizer = sr.Recognizer()
MicOpen = False
silence_start = None

t_pressed = False

# Función para escuchar y detectar palabra clave "Valentina"
def listen_for_keyword():
    global MicOpen, silence_start, t_pressed
    with sr.Microphone() as source:
        print("Iniciandos")
        recognizer.adjust_for_ambient_noise(source, duration=4)  # Ajustar para el ruido ambiental
        print("Ruido ambiental ajustado")
        print("Esperando la palabra 'Valentina'...")
        while True:
            print("-"*50)
            try:
                print("Escuchando....:")
                # Limitar el tiempo de grabación de cada fragmento
                audio = recognizer.listen(source, 10, 2)
                print("Procesando texto...")
                text = recognizer.recognize_google(audio, language="es-ES")
                print("Escuchado:", text)

                # Verificar si se dijo "Valentina"
                if "valentina" in text.lower() and not t_pressed:
                    MicOpen = True
                    silence_start = None  # Restablecer el contador de silencio
                    print("¡Palabra clave detectada! MicOpen:", MicOpen)
                    t_pressed = True        # Actualizar el estado a "presionada"
                    keyboard.press('alt+e')
                    time.sleep(0.1)
                    keyboard.release('alt+e')
                    keyboard.press('t')

            except sr.UnknownValueError:
                print("UnknownValueError")
                # No se entendió, considerar como silencio
                if MicOpen and (silence_start is None):
                    silence_start = time.time()  # Iniciar el contador de silencio
                elif MicOpen and (time.time() - silence_start >= 2):
                    MicOpen = False  # Si han pasado 3 segundos en silencio, desactivar MicOpen
                    silence_start = None
                    print("Silencio detectado. MicOpen:", MicOpen)
                    if t_pressed:
                        t_pressed = False
                        keyboard.press('alt+q')
                        time.sleep(0.1)
                        keyboard.release('alt+q')
                        keyboard.release('t') 

            except sr.WaitTimeoutError:
                print("WaitTimeoutError")
                # Si hay un tiempo de espera prolongado, considerar como silencio
                if MicOpen and silence_start is None:
                    silence_start = time.time()
                elif MicOpen and (time.time() - silence_start >= 2):
                    MicOpen = False
                    silence_start = None
                    print("Silencio detectado. MicOpen:", MicOpen)

# Llamar a la función para comenzar a escuchar
listen_for_keyword()
