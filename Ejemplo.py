
import google.generativeai as genai  # Importamos Gemini Pro
from dotenv import load_dotenv  # Librería para cargar variables de entorno
import time, os 
def load_variables():
    load_dotenv() 
    telegram_token = os.getenv( "telegram_token")  
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

    return telegram_token, GOOGLE_API_KEY




