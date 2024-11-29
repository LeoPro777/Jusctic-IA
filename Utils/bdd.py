from conector.conector import conectar_bd

def user_verification(user_id, user_name: None, user_fullname: None, user_first_name: None, user_last_name: None, day):
    """ 
        - Esta función verifica el rol del usuario si existe, si no, registra al usuario.
        - This function checks the user's role if it exists, if not, it logs the user.
    """
    conection = conectar_bd()
    try:
        cursor = conection.cursor()
        consult = f"SELECT id FROM users WHERE id ={user_id}"
        cursor.execute(consult)
        data = cursor.fetchall()
        if data:
            return True
        else:
            rol = "invitado"
            user_registration(user_id, user_name, user_fullname, user_first_name, user_last_name, rol, day)
            return False
    except Exception as e:
        print("Error al verificar el usuario")
        print(f"Error: {e}")
    finally:
        conection.close()

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
            consult = f"SELECT state_functions FROM user_properties WHERE {user_id}"
            print(consult)
            cursor.execute(consult)
            data = cursor.fetchall()
            print(data)
            return data[0]
        elif mode == "u":
            x = "update"
            if state_functions == 0:
                state_functions = "normal"
            elif state_functions == 1:
                state_functions = "chatpdf"            
            consult = f"UPDATE user_properties SET state_functions = '{state_functions}' WHERE id = {user_id}"
            cursor.execute(consult)
            conection.commit()
            return True
    except Exception as e:
        print(f"Error al -{x}- el estado de la funsion")
        print(f"Error: {e}")
    finally:
        conection.close() 

def handle_documents(user_id, mode):
    #-mejorar
    """ 
        - Esta función verifica el rol del usuario si existe, si no, registra al usuario.
        - This function checks the user's role if it exists, if not, it logs the user.
    """
    conection = conectar_bd()
    try:
        cursor = conection.cursor()
        if mode == 's':
            consult = f"SELECT path_doc FROM documents WHERE user_id = {user_id} ORDER BY id DESC;"
            cursor.execute(consult)
            data = cursor.fetchall()
            return data[0]
    except Exception as e:
        print(f"Error al manipular documentos")
        print(f"Error: {e}")
    finally:
        conection.close()      

def user_registration(user_id, user_name: None, user_fullname: None, user_first_name: None, user_last_name: None, rol, day):
    """ 
    - Esta función registra al usuario en la base de datos.
    - This function logs the user in the database.
    """
    conection = conectar_bd()
    try:
        cursor = conection.cursor()
        consult = f"INSERT INTO users (id,telegram_name,full_name,names,last_names,day_week,rol) VALUES({user_id},'{user_name}','{user_fullname}','{user_first_name}','{user_last_name}','{day}','{rol}');"
        cursor.execute(consult)
        consult = f"INSERT INTO user_properties (user_id) VALUES ({user_id});"
        cursor.execute(consult)
        consult = f"INSERT INTO social_networks (user_id) VALUES ({user_id});"
        cursor.execute(consult)
        conection.commit()
    except Exception as e:
        print("Error al registrar los usuarios")
        print(f"Error: {e}")
    finally:
        conection.close()

def documents_registration(user_id, document_name, day_week, path_doc):
    """ 
    - Esta función registra el mensaje en la base de datos.
    - This function logs the message in the database.
    """
    conection = conectar_bd()
    try:
        cursor = conection.cursor()
        consult = f"INSERT INTO documents (user_id,document_name,day_week,path_doc) VALUES({user_id},'{document_name}','{day_week}','{path_doc}')"
        cursor.execute(consult)
        conection.commit()
    except Exception as e:
        print("Error al registrar documentos")
        print(f"Error: {e}")
    finally:
        conection.close()

def message_registration(chat_id, user_id, content, day, message_type,importance):
    """
        - Esta función registra los documentos en la base de datos.
        - This function logs the documents in the database.
    """
    conection = conectar_bd()
    try:
        cursor = conection.cursor()
        consult = f"INSERT INTO messages (chat_id,user_id,content,day_week,message_type,importance) VALUES({chat_id},{user_id},'{content}','{day}','{message_type}',{importance})"
        cursor.execute(consult)
        conection.commit()
    except Exception as e:
        print("Error al registrar mensajes")
        print(f"Error: {e}")
    finally:
        conection.close()

def read_message(user_id):
    """ 
        - Esta función lee los mensajes del usuario en la base de datos.
        - This function reads the user's messages in the database.
    """
    conection = conectar_bd()
    try:
        cursor = conection.cursor()
        consult = f"SELECT m.content, m.sent_date, m.sent_time, m.message_type, m.day_week, u.full_name FROM messages m INNER JOIN users u ON m.user_id = u.id WHERE m.user_id in(1,{user_id}) ORDER BY m.sent_date ASC, m.sent_time ASC;"
        cursor.execute(consult)
        data = cursor.fetchall()
        context = ""

        for (content, sent_date, sent_time, message_type, day_week,full_name,) in data:
            message_format = f"{full_name}: {content} ||| {day_week} {sent_date} {sent_time} El usuario envió este mensaje en formato: {message_type}\n"
            context += message_format

        return context
        
    except Exception as e:
        print("Error al leer mensajes")
        print(f"Error: {e}")
    finally:
        conection.close()