from config.dbConnection import DBConnection
import hashlib  # Para hashear contraseñas
import os


class UsuarioModel:
    def __init__(self):
        self.db = DBConnection().conectar()
        self.cursor = self.db.cursor(dictionary=True)

    def verificarExistente(self, correo, cui):
        self.db = DBConnection().conectar()
        self.cursor = self.db.cursor(dictionary=True)

        query = "SELECT correo, cui FROM usuarios WHERE correo = %s OR cui = %s"
        self.cursor.execute(query, (correo, cui))
        return self.cursor.fetchone()


    def registrarUsuario(self, nombre, correo, cui, telefono, contrasena, tipo='Usuario'):
        self.db = DBConnection().conectar()
        self.cursor = self.db.cursor(dictionary=True)

        if self.verificarExistente(correo, cui):
            return {"success": False, "message": "El correo o CUI ya está registrado."}
        
        hashed_pass = hashPassword(contrasena)  # ahora guardamos hash (bytes)
        
        query = """
            INSERT INTO usuarios (nombre, correo, cui, telefono, contrasena, tipo)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        try:
            self.cursor.execute(query, (nombre, correo, cui, telefono, hashed_pass, tipo))
            self.db.commit()
            return {"success": True, "message": "Usuario registrado exitosamente."}
        except Exception as e:
            return {"success": False, "message": f"Error al registrar: {str(e)}"}

    
    def obtenerUsuarioPorCorreo(self, correo):
        self.db = DBConnection().conectar()
        self.cursor = self.db.cursor(dictionary=True)

        query = "SELECT * FROM usuarios WHERE correo = %s"
        self.cursor.execute(query, (correo,))
        return self.cursor.fetchone()

    def actualizarIntentos(self, correo, intentos):
        self.db = DBConnection().conectar()
        self.cursor = self.db.cursor(dictionary=True)

        query = "UPDATE usuarios SET intentos_fallidos = %s WHERE correo = %s"
        self.cursor.execute(query, (intentos, correo))
        self.db.commit()

    def bloquearUsuario(self, correo):
        self.db = DBConnection().conectar()
        self.cursor = self.db.cursor(dictionary=True)
        
        query = "UPDATE usuarios SET estado = 'Bloqueado' WHERE correo = %s"
        self.cursor.execute(query, (correo,))
        self.db.commit()

    def cerrarConexion(self):
        self.cursor.close()
        self.db.close()

def hashPassword(password, salt=None):
    if not salt:
        salt = os.urandom(16)  # 16 bytes de sal aleatoria
    hashed = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
    return salt + hashed  # concatenamos sal + hash

def verifyPassword(stored_password, provided_password):
    salt = stored_password[:16]          # los primeros 16 bytes son la sal
    stored_hash = stored_password[16:]   # el resto es el hash
    new_hash = hashlib.pbkdf2_hmac('sha256', provided_password.encode('utf-8'), salt, 100000)
    return new_hash == stored_hash