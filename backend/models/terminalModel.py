from config.dbConnection import DBConnection

class TerminalModel:
    def __init__(self):
        self.db = DBConnection().conectar()
        self.cursor = self.db.cursor(dictionary=True)

    def obtenerTerminalesBajoMinimo(self):
        self.db = DBConnection().conectar()
        self.cursor = self.db.cursor(dictionary=True)

        query = """
        SELECT id, nombre, capacidad, ocupadas,
               ROUND((ocupadas / capacidad) * 100, 2) AS porcentaje_ocupacion
        FROM terminales
        WHERE capacidad > 0 AND (ocupadas / capacidad) < 0.25
        """
        self.cursor.execute(query)
        return self.cursor.fetchall()
    
    def obtenerDisponibilidad(self):
        self.db = DBConnection().conectar()
        self.cursor = self.db.cursor(dictionary=True)
        
        query = """
        SELECT id, nombre, ubicacion, capacidad, ocupadas,
            (capacidad - ocupadas) AS espacios_libres
        FROM terminales
        ORDER BY nombre
        """
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def cerrarConexion(self):
        self.cursor.close()
        self.db.close()
