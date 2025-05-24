import mysql.connector

class DBConnection:
    def __init__(self):
        self.host = "localhost"              # Dirección del servidor MySQL
        self.user = "root"                   # Tu usuario de MySQL
        self.password = "12345"                   # Tu contraseña de MySQL
        self.database = "bicicletas_db"      # Nombre de tu base de datos
        self.connection = None

    def conectar(self):
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            print("Conexión a la base de datos exitosa.")
            return self.connection
        except mysql.connector.Error as err:
            print("Error al conectar a la base de datos:", err)
            return None

    def cerrar(self):
        if self.connection:
            self.connection.close()
            print("Conexión cerrada.")
