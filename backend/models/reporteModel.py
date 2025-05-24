from config.dbConnection import DBConnection

class ReporteModel:
    def __init__(self):
        self.db = DBConnection().conectar()
        self.cursor = self.db.cursor(dictionary=True)

    def crearReporte(self, usuario_id, bicicleta_id, tipo, descripcion):
        self.db = DBConnection().conectar()
        self.cursor = self.db.cursor(dictionary=True)

        query = """
        INSERT INTO reportes_problemas (usuario_id, bicicleta_id, tipo_problema, descripcion)
        VALUES (%s, %s, %s, %s)
        """
        try:
            self.cursor.execute(query, (usuario_id, bicicleta_id, tipo, descripcion))
            self.db.commit()
            return {"success": True, "message": "Reporte enviado correctamente."}
        except Exception as e:
            return {"success": False, "message": f"Error al guardar reporte: {str(e)}"}

    def cerrarConexion(self):
        self.cursor.close()
        self.db.close()

    def obtenerReportes(self, estado_filtro=None):
        self.db = DBConnection().conectar()
        self.cursor = self.db.cursor(dictionary=True)

        query = """
        SELECT r.id, u.nombre AS usuario, b.codigo AS bicicleta,
            r.tipo_problema, r.descripcion, r.estado, r.fecha_reporte
        FROM reportes_problemas r
        JOIN usuarios u ON r.usuario_id = u.id
        JOIN bicicletas b ON r.bicicleta_id = b.id
        """

        if estado_filtro:
            query += " WHERE r.estado = %s ORDER BY r.fecha_reporte DESC"
            self.cursor.execute(query, (estado_filtro,))
        else:
            query += " ORDER BY r.fecha_reporte DESC"
            self.cursor.execute(query)

        return self.cursor.fetchall()

    def actualizarEstadoReporte(self, reporte_id, nuevo_estado):
        self.db = DBConnection().conectar()
        self.cursor = self.db.cursor(dictionary=True)

        query = "UPDATE reportes_problemas SET estado = %s WHERE id = %s"
        self.cursor.execute(query, (nuevo_estado, reporte_id))
        self.db.commit()

    def actualizarEstadoBicicleta(self, bicicleta_id, nuevo_estado):
        self.db = DBConnection().conectar()
        self.cursor = self.db.cursor(dictionary=True)
        
        query = "UPDATE bicicletas SET estado = %s WHERE id = %s"
        self.cursor.execute(query, (nuevo_estado, bicicleta_id))
        self.db.commit()

