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
    



    def bicicletasDisponibles(self):
        query = """
        SELECT b.id, b.codigo, t.nombre AS terminal_origen
        FROM bicicletas b
        JOIN terminales t ON b.terminal_id = t.id
        WHERE b.estado = 'Disponible'
        """
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def moverBicicleta(self, bicicleta_id, nueva_terminal_id):
        # Obtener terminal actual
        self.cursor.execute("SELECT terminal_id FROM bicicletas WHERE id = %s", (bicicleta_id,))
        original = self.cursor.fetchone()

        if not original:
            return {"success": False, "message": "Bicicleta no encontrada."}

        terminal_origen = original['terminal_id']
        
        # Verificar espacio en destino
        self.cursor.execute("SELECT capacidad, ocupadas FROM terminales WHERE id = %s", (nueva_terminal_id,))
        destino = self.cursor.fetchone()

        if not destino or destino['ocupadas'] >= destino['capacidad']:
            return {"success": False, "message": "No hay espacio en la terminal de destino."}

        # Actualizar terminal y ocupación
        self.cursor.execute("UPDATE bicicletas SET terminal_id = %s WHERE id = %s", (nueva_terminal_id, bicicleta_id))
        self.cursor.execute("UPDATE terminales SET ocupadas = ocupadas + 1 WHERE id = %s", (nueva_terminal_id,))
        self.cursor.execute("UPDATE terminales SET ocupadas = ocupadas - 1 WHERE id = %s", (terminal_origen,))

        self.db.commit()
        return {"success": True, "message": "Bicicleta movida exitosamente."}


    def cerrarConexion(self):
        self.cursor.close()
        self.db.close()
