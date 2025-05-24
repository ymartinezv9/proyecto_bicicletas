from config.dbConnection import DBConnection

class SoporteModel:
    def __init__(self):
        self.db = DBConnection().conectar()
        self.cursor = self.db.cursor(dictionary=True)

    def enviarMensaje(self, usuario_id, asunto, mensaje):
        self.db = DBConnection().conectar()
        self.cursor = self.db.cursor(dictionary=True)
        
        query = """
        INSERT INTO mensajes_soporte (usuario_id, asunto, mensaje)
        VALUES (%s, %s, %s)
        """
        try:
            self.cursor.execute(query, (usuario_id, asunto, mensaje))
            self.db.commit()
            return {"success": True, "message": "Mensaje enviado al equipo de soporte."}
        except Exception as e:
            return {"success": False, "message": f"Error al enviar mensaje: {str(e)}"}

    def cerrarConexion(self):
        self.cursor.close()
        self.db.close()
