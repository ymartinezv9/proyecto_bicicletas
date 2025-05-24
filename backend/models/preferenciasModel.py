from config.dbConnection import DBConnection

class PreferenciasModel:
    def __init__(self):
        self.db = DBConnection().conectar()
        self.cursor = self.db.cursor(dictionary=True)

    def actualizarNotificaciones(self, usuario_id, estado):
        self.db = DBConnection().conectar()
        self.cursor = self.db.cursor(dictionary=True)

        query = """
        INSERT INTO preferencias (usuario_id, notificaciones)
        VALUES (%s, %s)
        ON DUPLICATE KEY UPDATE notificaciones = VALUES(notificaciones)
        """
        self.cursor.execute(query, (usuario_id, estado))
        self.db.commit()

    def agregarRutaFavorita(self, usuario_id, origen_id, destino_id):
        self.db = DBConnection().conectar()
        self.cursor = self.db.cursor(dictionary=True)

        query = """
        INSERT INTO rutas_favoritas (usuario_id, terminal_origen_id, terminal_destino_id)
        VALUES (%s, %s, %s)
        """
        self.cursor.execute(query, (usuario_id, origen_id, destino_id))
        self.db.commit()

    def obtenerPreferencias(self, usuario_id):
        self.db = DBConnection().conectar()
        self.cursor = self.db.cursor(dictionary=True)
        
        self.cursor.execute("SELECT notificaciones FROM preferencias WHERE usuario_id = %s", (usuario_id,))
        prefs = self.cursor.fetchone()

        self.cursor.execute("""
        SELECT t1.nombre AS origen, t2.nombre AS destino
        FROM rutas_favoritas rf
        JOIN terminales t1 ON rf.terminal_origen_id = t1.id
        JOIN terminales t2 ON rf.terminal_destino_id = t2.id
        WHERE rf.usuario_id = %s
        """, (usuario_id,))
        rutas = self.cursor.fetchall()

        return {"notificaciones": prefs['notificaciones'] if prefs else True, "rutas_favoritas": rutas}

    def cerrarConexion(self):
        self.cursor.close()
        self.db.close()
