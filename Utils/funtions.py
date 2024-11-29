from gtts import gTTS
import PyPDF2
import pyperclip
import os
import subprocess
import whisper
import time
import datetime


def read_pdf(archivo):
    with open(archivo, 'rb') as f:
        pdf_reader = PyPDF2.PdfReader(f)
        texto= ""
        for pagina in pdf_reader.pages:
            texto+= pagina.extract_text()

        return  texto.encode("utf-8").decode("utf-8")

def sda(user_id, text):
  """- Esta función busca guardar las conversaciones individuales de cada usuario y utilizarla
  para generar de un contexto del chat y así volver más eficientes la interacción con la IA.

  - This feature seeks to save each user's individual conversations and use them
  to generate a chat context and thus make interaction with AI more efficient."""

  Nombre_de_carpeta = f"Usuario_{user_id}"
  nombre_del_archivo = f"./Historial_Chats/{Nombre_de_carpeta}/{user_id}.txt"

  # Crear la carpeta si no existe
  os.makedirs(f"./Historial_Chats/{Nombre_de_carpeta}", exist_ok=True)

  # Abrir el archivo en modo escritura, truncando el contenido previo
  with open(nombre_del_archivo, "w") as archivo_de_texto:
      archivo_de_texto.write(text)

  print("Archivo sobrescrito correctamente")

def stt_whisper(input_file = "NOta.wav", model = "base", idioma ="es"):
    input_file = ogg_to_wav(input_file)
    inicio = time.time()
    s ={
        "text": "",
    }
    # cargamos el modelo de Whisper
    modelo = whisper.load_model(model)
    try:
        res = modelo.transcribe(input_file, language = idioma, verbose=False, word_timestamps=False)
        s["text"] = res["text"]
        return (s["text"])
    except Exception as r:
        print("Excetion: ", r)
    finally:
        print(f' Tiempo de stt: {time.time()-inicio} segundos')

def texto_a_voz(texto, ruta_salida="voz.mp3"):
    inicio = time.time()
    gTTS.GOOGLE_TTS_MAX_CHARS = 200
    tts = gTTS(texto, lang="es", tld="es", lang_check=False)
    # guardamos el archivo resultante
    tts.save(ruta_salida)
    comando = f'ffmpeg -y -i "{ruta_salida}" -filter:a "atempo=1.30" -vn "voz.ogg"'
    subprocess.run(comando, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    print(f' Tiempo: {time.time()-inicio} segundos')    

def ogg_to_wav(input_file = "Nota.ogg", onput_file = "Nota.wav"):
    inicio = time.time()
    comando = f"ffmpeg -i {input_file} -vn {onput_file}"
    subprocess.run(comando, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    print(f' Tiempo de conversion: {time.time()-inicio} segundos')
    return onput_file

def day_of_the_week():
    """Devuelve el día de la semana actual como un string."""
    days = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
    today = datetime.date.today()
    day = today.weekday()
    return days[day]

def stt_whisper(input_file = "NOta.wav", model = "base", idioma ="es"):
    input_file = ogg_to_wav(input_file)
    inicio = time.time()
    s ={
        "text": "",
    }
    # cargamos el modelo de Whisper
    modelo = whisper.load_model(model)
    try:
        res = modelo.transcribe(input_file, language = idioma, verbose=False, word_timestamps=False)
        s["text"] = res["text"]
        return (s["text"])
    except Exception as r:
        print("Excetion: ", r)
    finally:
        print(f' Tiempo de stt: {time.time()-inicio} segundos')