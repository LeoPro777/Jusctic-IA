import os # Librería para manejar variables de entorno
from dotenv import load_dotenv # Librería para cargar variables de entorno
import mysql.connector

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

# Conectar a la base de datos
def conectar_bd():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )

def database(self):
        conexion = conectar_bd()
        try:
            cursor = conexion.cursor()
            user = self.user.get()
            password = self.password.get()

            consulta = "SELECT * FROM usuarios WHERE usuario = %s AND password = %s"
            cursor.execute(consulta, (user,password))
            resultado = cursor.fetchone()
        finally:
            conexion.close()