from models.soporteModel import SoporteModel

class SoporteController:
    def __init__(self):
        self.soporteModel = SoporteModel()

    def enviarMensajeSoporte(self, usuario_id, asunto, mensaje):
        if not asunto or not mensaje:
            return {"success": False, "message": "El asunto y mensaje son obligatorios."}

        resultado = self.soporteModel.enviarMensaje(usuario_id, asunto, mensaje)
        self.soporteModel.cerrarConexion()
        return resultado
    
    def verMensajesPendientes(self):
        mensajes = self.soporteModel.obtenerMensajesPendientes()
        self.soporteModel.cerrarConexion()
        return {"success": True, "mensajes": mensajes}
    
    def atenderMensaje(self, mensaje_id):
        self.soporteModel.marcarMensajeComoAtendido(mensaje_id)
        self.soporteModel.cerrarConexion()
        return {"success": True, "message": "Mensaje marcado como atendido."}

    def verMensajesUsuario(self, usuario_id):
        mensajes = self.soporteModel.obtenerMensajesPorUsuario(usuario_id)
        self.soporteModel.cerrarConexion()
        return {"success": True, "mensajes": mensajes}
    
