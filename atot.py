# módulos de Python
import time
import subprocess
import whisper 
# módulos de terceros
from gtts import gTTS

def ogg_to_wav(input_file = "Nota.ogg", onput_file = "Nota.wav"):
    inicio = time.time()
    comando = f"ffmpeg -i {input_file} -vn {onput_file}"
    subprocess.run(comando, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    print(f' Tiempo: {time.time()-inicio} segundos')

def texto_a_voz(texto, ruta_salida="voz.mp3"):

    inicio = time.time()
    # generamos la locución con la API de Google TTS
    print('Generando locución con API de Google TTS')
    # lang: idioma para la locución
    # tld: dominio de Google
    # lang_check: comprobar si el idioma detectado en el texto está disponible
    gTTS.GOOGLE_TTS_MAX_CHARS = 200
    tts = gTTS(texto, lang="es", tld="es", lang_check=False)
    # guardamos el archivo resultante
    tts.save(ruta_salida)
    print('Acelerando audio con FFMPEG')
    comando = f'ffmpeg -y -i "{ruta_salida}" -filter:a "atempo=1.30" -vn "voz_acelerada_FFMPEG.mp3"'
    subprocess.run(comando, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    print(f' Tiempo: {time.time()-inicio} segundos')

def stt_whisper(input_file = "out.wav", model = "base", idioma ="es"):
    inicio = time.time()
    s ={
        "text": "",
    }
    # cargamos el modelo de Whisper
    modelo = whisper.load_model(model)
    try:
        res = modelo.transcribe(input_file, language = idioma, verbose=False, word_timestamps=False)
        s["text"] = res["text"]
        print(s["text"])
    except Exception as r:
        print("Excetion: ", r)
    finally:
        print(f' Tiempo: {time.time()-inicio} segundos')
    

if __name__ == '__main__':
    #texto = "Me caes mal trozo de basura"
    #texto_a_voz (texto)
   stt_whisper()