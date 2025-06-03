from config.dbConnection import DBConnection

class BicicletaModel:
    def __init__(self):
        self.db = DBConnection().conectar()
        self.cursor = self.db.cursor(dictionary=True)

    def obtenerBicicletaPorId(self, bicicleta_id):
        self.db = DBConnection().conectar()
        self.cursor = self.db.cursor(dictionary=True)


        query = "SELECT * FROM bicicletas WHERE id = %s"
        self.cursor.execute(query, (bicicleta_id,))
        return self.cursor.fetchone()

    def bloquearBicicleta(self, bicicleta_id):
        self.db = DBConnection().conectar()
        self.cursor = self.db.cursor(dictionary=True)

        query = "UPDATE bicicletas SET estado = 'Fuera de servicio' WHERE id = %s"
        self.cursor.execute(query, (bicicleta_id,))
        self.db.commit()

    def obtenerTodasLasBicicletas(self):
        self.db = DBConnection().conectar()
        self.cursor = self.db.cursor(dictionary=True)

        query = """
        SELECT b.id, b.codigo, b.estado, t.nombre AS terminal
        FROM bicicletas b
        LEFT JOIN terminales t ON b.terminal_id = t.id
        ORDER BY b.estado ASC, b.codigo ASC
        """
        self.cursor.execute(query)
        return self.cursor.fetchall()
    
    def obtenerUbicaciones(self):
        self.db = DBConnection().conectar()
        self.cursor = self.db.cursor(dictionary=True)

        query = """
        SELECT id, codigo, estado, latitud, longitud
        FROM bicicletas
        WHERE latitud IS NOT NULL AND longitud IS NOT NULL
        """
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def obtenerUbicaciones(self):
        self.db = DBConnection().conectar()
        self.cursor = self.db.cursor(dictionary=True)
        
        query = """
        SELECT id, codigo, estado, latitud, longitud
        FROM bicicletas
        WHERE latitud IS NOT NULL AND longitud IS NOT NULL
        """
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def obtenerBicicletasEnMantenimiento(self):
        query = "SELECT * FROM bicicletas WHERE estado = 'Mantenimiento'"
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def cerrarConexion(self):
        self.cursor.close()
        self.db.close()
