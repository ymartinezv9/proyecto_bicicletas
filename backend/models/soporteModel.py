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

    def obtenerMensajesPendientes(self):
        query = """
        SELECT ms.id, u.nombre AS remitente, ms.asunto, ms.mensaje, ms.fecha, ms.estado
        FROM mensajes_soporte ms
        JOIN usuarios u ON ms.usuario_id = u.id
        WHERE ms.estado = 'Pendiente'
        ORDER BY ms.fecha DESC
        """
        self.cursor.execute(query)
        return self.cursor.fetchall()
    
    def marcarMensajeComoAtendido(self, mensaje_id):
        query = "UPDATE mensajes_soporte SET estado = 'Atendido' WHERE id = %s"
        self.cursor.execute(query, (mensaje_id,))
        self.db.commit()

    def obtenerMensajesPorUsuario(self, usuario_id):
        query = """
        SELECT id, asunto, mensaje, fecha, estado
        FROM mensajes_soporte
        WHERE usuario_id = %s
        ORDER BY fecha DESC
        """
        self.cursor.execute(query, (usuario_id,))
        return self.cursor.fetchall()



    def cerrarConexion(self):
        self.cursor.close()
        self.db.close()
