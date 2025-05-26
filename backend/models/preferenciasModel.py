from config.dbConnection import DBConnection

class PreferenciasModel:
    def __init__(self):
        self.db = DBConnection().conectar()
        self.cursor = self.db.cursor(dictionary=True)

    def actualizarNotificaciones(self, usuario_id, estado):
        query = """
        INSERT INTO preferencias (usuario_id, notificaciones)
        VALUES (%s, %s)
        ON DUPLICATE KEY UPDATE notificaciones = VALUES(notificaciones)
        """
        self.cursor.execute(query, (usuario_id, estado))
        self.db.commit()
        return {"success": True, "message": "Notificaciones actualizadas correctamente."}

    def agregarRutaFavorita(self, usuario_id, origen_id, destino_id):
        # Verificar si ya existe la ruta
        query_verificar = """
        SELECT * FROM rutas_favoritas
        WHERE usuario_id = %s AND terminal_origen_id = %s AND terminal_destino_id = %s
        """
        self.cursor.execute(query_verificar, (usuario_id, origen_id, destino_id))
        existe = self.cursor.fetchone()  # <--- Aquí se consume el resultado

        if existe:
            return {"success": False, "message": "Esta ruta ya está guardada como favorita."}

        # Insertar si no existe
        query_insertar = """
        INSERT INTO rutas_favoritas (usuario_id, terminal_origen_id, terminal_destino_id)
        VALUES (%s, %s, %s)
        """
        self.cursor.execute(query_insertar, (usuario_id, origen_id, destino_id))
        self.db.commit()

        return {"success": True, "message": "Ruta favorita agregada correctamente."}


    def obtenerPreferencias(self, usuario_id):
        # Obtener notificaciones
        self.cursor.execute("SELECT notificaciones FROM preferencias WHERE usuario_id = %s", (usuario_id,))
        prefs = self.cursor.fetchone()

        # Obtener rutas favoritas
        self.cursor.execute("""
        SELECT t1.nombre AS origen, t2.nombre AS destino
        FROM rutas_favoritas rf
        JOIN terminales t1 ON rf.terminal_origen_id = t1.id
        JOIN terminales t2 ON rf.terminal_destino_id = t2.id
        WHERE rf.usuario_id = %s
        """, (usuario_id,))
        rutas = self.cursor.fetchall()

        return {
            "notificaciones": prefs['notificaciones'] if prefs else True,
            "rutas_favoritas": rutas
        }

    def cerrarConexion(self):
        self.cursor.close()
        self.db.close()
