import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'backend')))

from models.usuarioModel import UsuarioModel, hashPassword  # 👈 importante

def crear_admin():
    usuarioModel = UsuarioModel()

    nombre = "soporte Inicial"
    correo = "y@gmail.com"
    cui = "1234567890002"
    telefono = "1234-5678"
    contrasena = "12345"
    tipo = "Soporte"

    # Hashear explícitamente
    hashed = hashPassword(contrasena)

    query = """
        INSERT INTO usuarios (nombre, correo, cui, telefono, contrasena, tipo)
        VALUES (%s, %s, %s, %s, %s, %s)
    """
    usuarioModel.cursor.execute(query, (nombre, correo, cui, telefono, hashed, tipo))
    usuarioModel.db.commit()
    usuarioModel.cerrarConexion()

    print("Administrador creado con éxito.")

if __name__ == "__main__":
    crear_admin()
