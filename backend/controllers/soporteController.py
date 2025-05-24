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
