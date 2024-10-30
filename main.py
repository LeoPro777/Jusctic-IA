from telegram import Update# Librería para manejar actualizaciones de Telegram
from telegram.ext import ApplicationBuilder,CommandHandler,ContextTypes,MessageHandler,filters
from dotenv import load_dotenv  # Librería para cargar variables de entorno
import os  # Librería para manejar variables de entorno
import google.generativeai as genai  # Importamos Gemini Pro
import datetime
from telegram.constants import ChatAction
import time
from config import JUSTICIA, technical_aspects
import subprocess
import whisper
import random
from gtts import gTTS

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    - Función para manejar el comando /start que da inicio a la activación del chat Bot.
    - Function to handle the /start command that starts the activation of the Bot chat.
    """
    #------------------------------------------ Funciones de respuesta ------------------------------------------#
    response = main_process(update, context, 1)[0]
    await escribir_con_retraso(update, context, response)

def main_process(update: Update, context: ContextTypes.DEFAULT_TYPE, mode):
    """
    - La función principal de respuesta es el centro principal que comunica las funciones de respuesta. 
    - The main response function is the main center that communicates the response functions.
    """
    #------------------------------------------ Variables Principales ------------------------------------------#
    user = update.effective_user.name
    user_id = update.effective_user.id
    user_full_name = update.effective_user.full_name
    date = datetime.datetime.now()
    print(f"Usuario: {user}\nNombre completo: {user_full_name}\n")
    #------------------------------------------ Funciones de respuesta ------------------------------------------#
    if mode == 1:  
        text = "Hola"
        user_message_type = "text"
    elif mode == 2:
        text = update.message.text
        user_message_type = "text"
    elif mode == 3:
        text = download_and_read_audio(update,context)
        user_message_type = "audio"
    else:
        text = "Sistema: Enviando una nota de Voz..."
        user_message_type = "Notification"
    while(True):
        try: 
            context_chat, new_context = chat_history_register_to_user(user, user_full_name, user_id, text, date, user_message_type)
            response_types = define_response_types(text, context_chat)
            print(f"New_context = {new_context}\nText = {text}")
            if new_context:
                context_chat = chat_history_register_to_user(user, user_full_name, user_id, text, date, user_message_type)[0]
                response = ia_interaction(1, text, context_chat, JUSTICIA, response_types)
            else:
                response = ia_interaction(2, text, context_chat, JUSTICIA, response_types)
            chat_history_register_to_towa(user,user_id, response, date, response_types)
            break
        except:
            time.sleep(3) 
    return response, response_types

# Funcion para manejar el mensaje del usuario y la respuesta del bot al mismo tiempo
async def handle_message_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    response, response_types = main_process(update, context, 2)
    numero = random.randint(0,100)
    if response_types == "audio":
        await audio_con_retraso(update, context, response)
    else:
        if numero < 5:
            await audio_con_retraso(update, context, response)
        else:
            await escribir_con_retraso(update, context, response)
    try:
        os.remove("voz.mp3")
        os.remove("voz.ogg")
    except:
        pass

async def handle_message_voice(update: Update, context: ContextTypes.DEFAULT_TYPE):

    numero = random.randint(0,100)
    if numero < 20:
        while (True):
            try:
                response, response_types = main_process(update, context, 4)
                break
            except:
                time.sleep(3)
        numero = random.randint(0,100)
        if numero < 50:
            await audio_con_retraso(update, context, response)
        else:
            await escribir_con_retraso(update, context, response)
    try:
        os.remove("voz.mp3")
        os.remove("voz.ogg")
    except:
        pass
    response, response_types = main_process(update, context, 3)
    numero = random.randint(0,100)
    if response_types == "audio":
        await audio_con_retraso(update, context, response)
    else:
        if numero < 5:
            await audio_con_retraso(update, context, response)
        else:
            await escribir_con_retraso(update, context, response)
        try:
            os.remove("Nota.ogg")
            os.remove("Nota.wav")
        except:
            pass
        try:
            os.remove("voz.mp3")
            os.remove("voz.ogg")
        except:
            pass

async def handle_message_document(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """if update.message.document:
            if update.message.document.mime_type == "application/pdf":
                file_name = update.message.document.file_name
                new_file = await update.message.effective_attachment.get_file()
                await new_file.download_to_drive(file_name)
            else:
                await update.message.reply_text("Formato no compatible, únicamente se acepta PDF")"""
    pass

def define_response_types(text, context):
    """- Esta funcion busca definir la forma en como te puede responder
    el asistente, ya sea mediante texto o audio (tipo nota de voz).

    - This function seeks to define the way in which the assistant 
    can respond to you, either through text or audio in the form of a voice note."""
    modelo = genai.GenerativeModel("gemini-pro")
    genai.configure(api_key=load_variables()[1])
    opciones = ["text", "audio"]
    pront = f"Compórtate como una analizadora de contexto cuya función es devolver una palabra de una lista, cabe destacar que es muy importante que tus decisiones siempre deben estar orientadas a la petición del usuario  y a su contexto, este es el contexto en tiempo real de este chat, son las conversaciones que hemos tenido: '{context}', según este mensaje importante*{text}* responde únicamente un elemento de esta lista '{opciones}',  es muy importante que tu respuesta solo y únicamente sea un elemento de esa lista sin comillas ya que de lo contrario romperás el programa, por favor solo devuelve un elemento, sin explicaciones ni resúmenes ni nada distinto a lo especifico que te estoy pidiendo."
    while(True):
            try:
                respuesta = modelo.generate_content(pront)
                respuesta = respuesta.text
                print(f"\nForma de respuesta: {respuesta}\n")
                if respuesta in opciones:
                    return respuesta
                else:
                    time.sleep(2)
            except Exception as e:
                print(f"Exeption: {e}")

def ia_interaction(mode, text, context_chat, personalidad, response_types):

    # Usamos el modelo generativo de la IA
    read_code = code_read()
    modelo = genai.GenerativeModel("gemini-pro")

    genai.configure(api_key=load_variables()[1])
    if mode == 1:
        respuesta = modelo.generate_content(f"Asumiendo esta personalidad '{personalidad}', asumiendo que este es tu codigo fuente '{read_code}', asumiendo estos aspectos tecnicos '{technical_aspects}' has una pequeña y corta presentacion sobre ti, no reveles mucho de ti, algo corto y superficial")
        respuesta = respuesta.text
        return respuesta
    elif mode == 2:
        pront = f"Siendo este el codigo en la cual estas programada '{read_code}', este es el contexto de este chat, son las conversaciones que hemos tenido: '{context_chat}', asumiendo esta personalidad '{personalidad}', asumiendo estos aspectos tecnicos '{technical_aspects}',  responde a este mensaje '{text}' por favor bajo ninguna circustancia repitas las mismas respuestas, se creativa, ademas la respuestas que des será mostrada en forma de: '{response_types}' cosa que esm uy importante tener en cuenta."
        while(True):
            try:
                respuesta = modelo.generate_content(pront)
                respuesta = respuesta.text
                return respuesta
            except Exception as e:
                print(f"Exeption: {e}")

# funcion de error
""" async def error(update: Update, context: ContextTypes):
    print(context.error)
    await update.callback_query.message.reply_text("Ocurrio un error") """

def chat_history_register_to_user(user,user_full_name, user_id, text, date, user_message_type):
    """- Esta función busca guardar las conversaciones individuales de cada usuario y utilizarla
    para generar de un contexto del chat y así volver más eficientes la interacción con la IA.

    - This feature seeks to save each user's individual conversations and use them
    to generate a chat context and thus make interaction with AI more efficient."""

    Nombre_de_carpeta = f"Usuario_{user_id}"
    nombre_del_archivo = f"./Historial_Chats/{Nombre_de_carpeta}/{user}.txt"
    if os.path.exists(nombre_del_archivo)==True:
        archivo_de_texto = open(nombre_del_archivo,"a")
        new_context = False
    else:
        os.mkdir(f"./Historial_Chats/{Nombre_de_carpeta}")
        archivo_de_texto = open(nombre_del_archivo,"a")
        archivo_de_texto.write(f"Este historial pertence a: {user_full_name}: abierto en la fecha: {date}\n")
        new_context = True
    archivo_de_texto.write(f"{user}: {text} ||| {date} El usuario envio este mensaje en formato: {user_message_type}\n")
    archivo_de_texto.close()
    archivo_de_texto = open(nombre_del_archivo,"r")
    context_chat = archivo_de_texto.read()
    archivo_de_texto.close()
    return context_chat, new_context


def chat_history_register_to_towa(user, user_id, response, date, response_type):
    Nombre_de_carpeta = f"Usuario_{user_id}"
    nombre_del_archivo = f"./Historial_Chats/{Nombre_de_carpeta}/{user}.txt"
    archivo_de_texto = open(nombre_del_archivo,"a")
    archivo_de_texto.write(f"Towa: {response} ||| {date} Enviaste en formato: {response_type}\n")
    print(f"Towa: {response} {date}\n")
    archivo_de_texto.close()


async def escribir_con_retraso(update: Update, context: ContextTypes.DEFAULT_TYPE, respuesta):
    """Simula que el bot está escribiendo antes de enviar la respuesta."""
    await update.message.chat.send_action(ChatAction.TYPING)
    time.sleep(3)  # Ajusta el tiempo de espera según la longitud de la respuesta
    await update.message.reply_text(respuesta)


async def audio_con_retraso(update: Update, context: ContextTypes.DEFAULT_TYPE, respuesta):
    """Simula que el bot está escribiendo antes de enviar la respuesta."""
    texto_a_voz(respuesta)
    await update.message.chat.send_action(ChatAction.UPLOAD_VOICE)
    time.sleep(5)  # Ajusta el tiempo de espera según la longitud de la respuesta
    await update.message.reply_voice("voz.ogg")

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


def ogg_to_wav(input_file = "Nota.ogg", onput_file = "Nota.wav"):
    inicio = time.time()
    comando = f"ffmpeg -i {input_file} -vn {onput_file}"
    subprocess.run(comando, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    print(f' Tiempo de conversion: {time.time()-inicio} segundos')
    return onput_file

def texto_a_voz(texto, ruta_salida="voz.mp3"):
    inicio = time.time()
    gTTS.GOOGLE_TTS_MAX_CHARS = 200
    tts = gTTS(texto, lang="es", tld="es", lang_check=False)
    # guardamos el archivo resultante
    tts.save(ruta_salida)
    comando = f'ffmpeg -y -i "{ruta_salida}" -filter:a "atempo=1.30" -vn "voz.ogg"'
    subprocess.run(comando, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    print(f' Tiempo: {time.time()-inicio} segundos')    

def load_variables():
    load_dotenv() 
    telegram_token = os.getenv( "telegram_token")  
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

    return telegram_token, GOOGLE_API_KEY

async def download_and_read_audio(update: Update, context: ContextTypes.DEFAULT_TYPE):
    new_file = await update.message.effective_attachment.get_file()
    file_name = f"Nota.ogg"
    await new_file.download_to_drive(file_name)
    text = stt_whisper(file_name)
    return text

def main():
    inicio = time.time()
    print("Iniciando bot...")
    application = (
        ApplicationBuilder().token(load_variables()[0]).build()
    )  # inicializar el bot
    # agregar comandos
    application.add_handler(CommandHandler("start", start))
    # agregar funciones
    application.add_handler(MessageHandler(filters.TEXT, handle_message_text))
    application.add_handler(MessageHandler(filters.VOICE, handle_message_voice))   # funcion de respuestas
    # agregar error
    # application.add_error_handler(error)
    # iniciar
    print("Bot iniciado")
    # poll_interval=1,timeout=10 #tiempo de espera para la respuesta del bot en segundos
    application.run_polling(poll_interval=5, timeout=5)
    print(f' Tiempo: {time.time()-inicio} segundos')

def code_read():
    try:
        with open("main.py", 'r') as archivo:
            read_code = archivo.read()
            archivo.close()
            return read_code
    except FileNotFoundError:
        print(f"El archivo main.py no se encontró.")
    except Exception as e:
        print(f"Ocurrió un error al leer el archivo: {e}")


if __name__ == "__main__":  # Iniciar el bot
    main()
