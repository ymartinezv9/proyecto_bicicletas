from models.usuarioModel import UsuarioModel
from models.usuarioModel import verifyPassword

class UsuarioController:
    def __init__(self):
        self.usuarioModel = UsuarioModel()

    def registrarUsuario(self, datosUsuario):
    
        # Validar campos obligatorios
        campos_obligatorios = ['nombre', 'correo', 'cui', 'telefono', 'contrasena']
        for campo in campos_obligatorios:
            if campo not in datosUsuario or not datosUsuario[campo]:
                return {"success": False, "message": f"El campo '{campo}' es obligatorio."}

        resultado = self.usuarioModel.registrarUsuario(
            datosUsuario['nombre'],
            datosUsuario['correo'],
            datosUsuario['cui'],
            datosUsuario['telefono'],
            datosUsuario['contrasena'],
            datosUsuario.get('tipo', 'Usuario')
        )
        
        self.usuarioModel.cerrarConexion()
        return resultado
    
    def iniciarSesion(self, datosUsuario):
        correo = datosUsuario.get('correo')
        contrasena = datosUsuario.get('contrasena')

        usuario = self.usuarioModel.obtenerUsuarioPorCorreo(correo)
        if not usuario:
            return {"success": False, "message": "Usuario no encontrado."}
        
        if usuario['estado'] == 'Bloqueado':
            return {"success": False, "message": "Cuenta bloqueada. Contacta al administrador."}

        # Verificar contraseña con hash
        if verifyPassword(usuario['contrasena'], contrasena):
            self.usuarioModel.actualizarIntentos(correo, 0)
            self.usuarioModel.cerrarConexion()            
            return {
                "success": True,
                "message": f"¡Bienvenido {usuario['nombre']}!",
                "usuario": {
                    "id": usuario["id"],
                    "nombre": usuario["nombre"],
                    "correo": usuario["correo"],
                    "tipo": usuario["tipo"]
                }
            }
            

        else:
            intentos = usuario['intentos_fallidos'] + 1
            self.usuarioModel.actualizarIntentos(correo, intentos)

            if intentos >= 3:
                self.usuarioModel.bloquearUsuario(correo)
                self.usuarioModel.cerrarConexion()
                return {"success": False, "message": "Cuenta bloqueada por 3 intentos fallidos."}
            else:
                self.usuarioModel.cerrarConexion()
                return {"success": False, "message": f"Contraseña incorrecta. Intentos: {intentos}/3"}
