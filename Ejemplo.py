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


def handle_state_functions(user_id, mode, state_functions = 0):
    """ 
        - Esta función verifica el rol del usuario si existe, si no, registra al usuario.
        - This function checks the user's role if it exists, if not, it logs the user.
    """
    conection = conectar_bd()
    try:
        cursor = conection.cursor()
        if mode == "s":
            x = "read"
            consult = f"SELECT state_functions FROM users WHERE id = 2147483647"
            cursor.execute(consult)
            data = cursor.fetchall()
            return data[0]
        elif mode == "u":
            x = "update"
            if state_functions == 0:
                state_functions = "normal"
            elif state_functions == 1:
                state_functions = "chatpdf"            
            consult = f"UPDATE users SET state_functions = '{state_functions}' WHERE id = {user_id}"
            cursor.execute(consult)
            conection.commit()
            return True
    except Exception as e:
        print(f"Error al -{x}- el estado de la funsion")
        print(f"Error: {e}")
    finally:
        conection.close() 
