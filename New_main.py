from telegram import Update, InlineKeyboardButton,InlineKeyboardMarkup # Librería para manejar actualizaciones de Telegram
from telegram.ext import ApplicationBuilder,CommandHandler,ContextTypes,MessageHandler,filters, CallbackContext,CallbackQueryHandler
from dotenv import load_dotenv  # Librería para cargar variables de entorno
import os  # Librería para manejar variables de entorno
import google.generativeai as genai  # Importamos Gemini Pro
import datetime
from telegram.constants import ChatAction
import time
from config import JUSTICIA, technical_aspects
import random
from Utils.bdd import user_verification, message_registration, read_message, documents_registration, handle_state_functions, handle_documents
from Utils.funtions import sda, texto_a_voz, day_of_the_week, stt_whisper, read_pdf

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    - Función para manejar el comando /start que da inicio a la activación del chat Bot.
    - Function to handle the /start command that starts the activation of the Bot chat.
    """
    #------------------------------------------ Variables Principales ------------------------------------------#

    id_user = update.effective_user.id
    user_name = update.effective_user.name
    user_fullname = update.effective_user.full_name
    user_first_name = update.effective_user.first_name
    user_last_name = update.effective_user.last_name
    day = day_of_the_week()
    #------------------------------------------ Funciones de respuesta ------------------------------------------#

    validation = user_verification(id_user, user_name, user_fullname, user_first_name, user_last_name, day)
    response = main_process(update, context, 1)[0]
    await escribir_con_retraso(update, context, response)

def main_process(update: Update, context: ContextTypes.DEFAULT_TYPE, mode, callback_action=""):

    """
    - La función principal de respuesta es el centro principal que comunica las funciones de respuesta. 
    - The main response function is the main center that communicates the response functions.
    """
    #------------------------------------------ Variables Principales ------------------------------------------#
    user_id = update.effective_user.id
    user_name = update.effective_user.name
    user_full_name = update.effective_user.full_name
    chat_id = update.effective_chat.id
    day = day_of_the_week()
    try:
        state_funtions = handle_state_functions(user_id, "s")
    except Exception as r:
        print(f"Error: {r}")
        return "No estamos disponibles en este momento"

    print(f"Usuario: {user_name}\nNombre completo: {user_full_name}\n")
    #------------------------------------------ Funciones de respuesta ------------------------------------------#

    if state_funtions[0] == "normal":
        part = ""
        if mode == 1:
            content = "Hola"
            message_type = "text"
        elif mode == 2:
            content = update.message.text
            message_type = "text"
        elif mode == 3:
            content= download_and_read_audio(update,context)
            message_type = "audio"
        else:
            content = "Sistema: Enviando una nota de Voz..."
            message_type[0] = "Notification"""
    elif state_funtions == "chatpdf":
        part = chat_pdf(user_id)
        content = callback_action
        if callback_action == "":
            mode = 3
            content = update.message.text
            callback_action = content
            message_type = "text"
        elif mode == 4:
            content= download_and_read_audio(update,context)
            message_type = "audio"
        else:
            content = "Sistema: Enviando una nota de Voz..."
            message_type = "Notification"""
    while(True):
        try: 
            print(f"\n{user_full_name}: {content}\n")
            context_chat, new_context = chat_history_register_to_user(chat_id, user_id, content, message_type, 1, day)
            response_types = define_response_types(content, context_chat)
            if new_context == "":
                print("Opcion 1")
                response = ia_interaction(1, content, context_chat, JUSTICIA, response_types)
                chat_history_register_to_justicia(chat_id, 1, response, message_type, 1, day)
            else:
                print("Opcion 2")
                response = ia_interaction(mode, content, context_chat, JUSTICIA, response_types, callback_action, part)
                chat_history_register_to_justicia(chat_id, 1, response, message_type, 1, day)
            break
        except Exception as r:
            print(f"Hubo un problema al responder: \n\nProblema {r}")
            time.sleep(3) 
    return response, response_types

async def handle_message_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    response, response_types = main_process(update, context, 2)
    numero = random.randint(0,100)
    if response_types == "audio":
        await audio_con_retraso(update, context, response)
    else:
        await escribir_con_retraso(update, context, response)
    try:
        os.remove("voz.mp3")
        os.remove("voz.ogg")
    except:
        pass

async def handle_message_document(update: Update, context: ContextTypes.DEFAULT_TYPE):

    #------------------------------------------ Variables Principales ------------------------------------------#
    user_id = update.effective_user.id
    user_name = update.effective_user.name
    day = day_of_the_week()
    if update.message.document:
            if update.message.document.mime_type == "application/pdf":
                document_name = update.message.document.file_name
                new_file = await update.message.effective_attachment.get_file()
                path_doc =  f"./documents/{document_name}"
                await new_file.download_to_drive(path_doc)
                documents_registration(user_id, document_name, day, path_doc)
                handle_state_functions(user_id, "u",1)
                await chatpdf_primarykey(update, context, document_name)           
            else:
                await update.message.reply_text("Formato no compatible, únicamente se acepta PDF")
    pass

def define_response_types(content, context: None):
    """- Esta funcion busca definir la forma en como te puede responder
    el asistente, ya sea mediante texto o audio (tipo nota de voz).

    - This function seeks to define the way in which the assistant 
    can respond to you, either through text or audio in the form of a voice note.
    """

    modelo = genai.GenerativeModel("gemini-pro")
    genai.configure(api_key=load_variables()[1])
    opciones = ["text", "audio"]
    pront = f"Compórtate como una analizadora de contexto cuya función es devolver una palabra de una lista, cabe destacar que es muy importante que tus decisiones siempre deben estar orientadas a la petición del usuario  y a su contexto, este es el contexto en tiempo real de este chat, son las conversaciones que hemos tenido: '{context}', según este mensaje importante*{content}* responde únicamente un elemento de esta lista '{opciones}',  es muy importante que tu respuesta solo y únicamente sea un elemento de esa lista sin comillas ya que de lo contrario romperás el programa, por favor solo devuelve un elemento, sin explicaciones ni resúmenes ni nada distinto a lo especifico que te estoy pidiendo."
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
                print("Error al definifir el tipo de respuestas")
                print(f"Exeption: {e}")

def ia_interaction(mode=2 , content="", context_chat="", personalidad="", response_types="", callback_action="", part = ""):

    # Usamos el modelo generativo de la IA
    read_code = code_read()
    modelo = genai.GenerativeModel("gemini-pro")
    genai.configure(api_key=load_variables()[1])

    if mode == 1:
        respuesta = modelo.generate_content(f"Asumiendo esta personalidad '{personalidad}', asumiendo que este es tu codigo fuente '{read_code}', asumiendo estos aspectos tecnicos '{technical_aspects}' has una pequeña y corta presentacion sobre ti, no reveles mucho de ti, algo corto y superficial")
        respuesta = respuesta.text
        return respuesta
    elif mode == 2:
        pront = f"Siendo este el codigo en la cual estas programada '{read_code}', este es el contexto de este chat, son las conversaciones que has tenido con este usario: '{context_chat}', asumiendo esta personalidad '{personalidad}', asumiendo estos aspectos tecnicos '{technical_aspects}',  responde a este mensaje '{content}' por favor bajo ninguna circustancia repitas las mismas respuestas, se creativa, ademas la respuestas que des será mostrada en forma de: '{response_types}' cosa que es muy importante tener en cuenta."
    elif mode == 3:      
        pront = f"Este es el contexto de este chat, son las conversaciones que has tenido con este usario: '{context_chat}', este es el contenido del pdf {part} que usaras unicamente para responder a esta pregunta {callback_action}"
        print(pront)
        sda(1, pront)
    while(True):
        try:
            respuesta = modelo.generate_content(pront)
            respuesta = respuesta.text
            return respuesta
        except Exception as e:
            print(f"Exeption: {e}")

#-------------------- Funciones de Registro --- Logging Functions --------------------#

def chat_history_register_to_justicia(chat_id, user_id: None, content: None, message_type, importance: None, day):
    """
    - Esta función busca guardar las respuestas individuales a cada usuario y utilizarla para generar de un contexto 
    del chat y así volver más eficientes la interacción con la IA.
    - This function seeks to save individual responses to each user and use them to 
    generate a chat context context and thus make interaction with AI more efficient.
    """

    date = datetime.datetime.now()
    message_registration(chat_id, user_id, content, day, message_type, importance)
    print(f"\nJustic-ia: {content} {date}\n")

def chat_history_register_to_user(chat_id, user_id: None, content: None, message_type, importance: None, day):
    """- Esta función busca guardar las conversaciones individuales de cada usuario y utilizarla
    para generar de un contexto del chat y así volver más eficientes la interacción con la IA.

    - This feature seeks to save each user's individual conversations and use them
    to generate a chat context and thus make interaction with AI more efficient."""
    new_context = read_message(user_id)

    message_registration(chat_id, user_id, content, day, message_type, importance)
    context_chat = read_message(user_id)
    sda(user_id,context_chat)

    return context_chat, new_context

#-------------------- Funciones de Envio --- Shipping Functions --------------------#

async def escribir_con_retraso(update: Update, context: ContextTypes.DEFAULT_TYPE, respuesta):
    """Simula que el bot está escribiendo antes de enviar la respuesta."""
    try:
        await update.message.chat.send_action(ChatAction.TYPING)
        time.sleep(3)  # Ajusta el tiempo de espera según la longitud de la respuesta
        await update.message.reply_text(respuesta)
    except:
        await update.callback_query.message.chat.send_action(ChatAction.TYPING)
        time.sleep(3)  # Ajusta el tiempo de espera según la longitud de la respuesta
        await update.callback_query.message.reply_text(respuesta)

async def audio_con_retraso(update: Update, context: ContextTypes.DEFAULT_TYPE, respuesta):
    """Simula que el bot está escribiendo antes de enviar la respuesta."""
    texto_a_voz(respuesta)
    await update.message.chat.send_action(ChatAction.UPLOAD_VOICE)
    time.sleep(5)  # Ajusta el tiempo de espera según la longitud de la respuesta
    await update.message.reply_voice("voz.ogg")

#-------------------- Funciones Especiales --- Special Functions --------------------#

async def chatpdf_primarykey(update: Update, context: ContextTypes.DEFAULT_TYPE, document_name): 
    keyboard =InlineKeyboardMarkup([
                [InlineKeyboardButton(text=f"Elaborar una Introducción", callback_data="intro")], #callback_data es el valor que se envia al bot 
                [InlineKeyboardButton(text="Elaborar una Conclusión", callback_data='conclu')],
                [InlineKeyboardButton(text="Ayuda 🆘", callback_data='help')],
                [InlineKeyboardButton(text="Salir de ChatPDF", callback_data='close')],
            ])
    
    await update.message.reply_text(
            f"Bienvenido a ChatPDF.\n\nPDF: {document_name} 📁\n\nPregunta lo que quieras." 
            ,reply_markup=keyboard)

async def chatpdf_callback(update: Update, context: CallbackContext): 
    """
    Obedece al Callback de la fusion de respchatpdf_primarykey
    """
    user_id = update.effective_user.id
    data = update.callback_query.data
    if data == "intro":
        callback_action = "Elabora una introducción para un trabajo academico, debe ser clara, redactada con máxima calidad discursiva. Y la estuctura de texto tiene que tener es tipo parrafo, ninguna mas"
    elif data == "conclu":
        callback_action = "Elabora una Conclusión para un trabajo academico, debe ser clara, redactada con máxima calidad discursiva. Y la estuctura de texto tiene que tener es tipo parrafo, ninguna mas"
    elif data == "close":
        handle_state_functions(user_id, "u")
        callback_action = ""
        #------------------------------------------ Funciones de respuesta ------------------------------------------#
    response = main_process(update, ContextTypes.DEFAULT_TYPE, 2, callback_action)[0]
    await escribir_con_retraso(update, context, response)

def chat_pdf(user_id):
    path_doc = handle_documents(user_id, "s")
    content_doc = read_pdf(path_doc[0])
    part = f"El documento tiene este contenido: '{content_doc}'"
    return part

async def download_and_read_audio(update: Update, context: ContextTypes.DEFAULT_TYPE):
    new_file = await update.message.effective_attachment.get_file()
    file_name = f"Nota.ogg"
    await new_file.download_to_drive(file_name)
    text = stt_whisper(file_name)
    return text

def code_read():
    try:
        with open("New_main.py", 'r', encoding='latin-1') as archivo:
            read_code = archivo.read()
            archivo.close()
            return read_code
    except FileNotFoundError:
        print(f"El archivo main.py no se encontró.")
    except Exception as e:
        print(f"Ocurrió un error al leer el archivo: {e}")

def load_variables():
    load_dotenv() 
    telegram_token = os.getenv( "telegram_token")  
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

    return telegram_token, GOOGLE_API_KEY

def main():

    inicio = time.time()
    print("Iniciando bot...")
    application = (
        ApplicationBuilder().token(load_variables()[0]).build()
    ) 
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT, handle_message_text))
    application.add_handler(MessageHandler(filters.ATTACHMENT, handle_message_document))
    application.add_handler(CallbackQueryHandler(chatpdf_callback))

    print("Bot iniciado")
    application.run_polling(poll_interval=5, timeout=5)
    print(f' Tiempo: {time.time()-inicio} segundos')

if __name__ == "__main__":  
    main()
