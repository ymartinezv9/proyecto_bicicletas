from datetime import datetime
from config.dbConnection import DBConnection
import random

class ReservaModel:
    def __init__(self):
        self.db = DBConnection().conectar()
        self.cursor = self.db.cursor(dictionary=True)

    def crearPin(self):
        return str(random.randint(1000, 9999))

    def obtenerBicicletaDisponible(self, terminal_id):
        self.db = DBConnection().conectar()
        self.cursor = self.db.cursor(dictionary=True)

        query = """
        SELECT * FROM bicicletas
        WHERE terminal_id = %s AND estado = 'Disponible'
        LIMIT 1
        """
        self.cursor.execute(query, (terminal_id,))
        return self.cursor.fetchone()

    def espacioDisponibleEnDestino(self, terminal_id):
        self.db = DBConnection().conectar()
        self.cursor = self.db.cursor(dictionary=True)

        query = "SELECT capacidad, ocupadas FROM terminales WHERE id = %s"
        self.cursor.execute(query, (terminal_id,))
        terminal = self.cursor.fetchone()
        if terminal:
            return terminal['ocupadas'] < terminal['capacidad']
        return False

    def crearReserva(self, usuario_id, origen_id, destino_id):
        self.db = DBConnection().conectar()
        self.cursor = self.db.cursor(dictionary=True)

        self.cursor.execute("SELECT * FROM reservas WHERE usuario_id = %s AND estado = 'Activa'", (usuario_id,))
        if self.cursor.fetchone():
            return {"success": False, "message": "Ya tienes una reserva activa."}

        bicicleta = self.obtenerBicicletaDisponible(origen_id)
        if not bicicleta:
            return {"success": False, "message": "No hay bicicletas disponibles en la terminal de origen."}

        bicicleta_id = bicicleta['id']
        pin = self.crearPin()

        self.cursor.execute("UPDATE bicicletas SET estado = 'En Uso' WHERE id = %s", (bicicleta_id,))

        self.cursor.execute("""
            INSERT INTO reservas (usuario_id, bicicleta_id, terminal_origen_id, terminal_destino_id, estado, hora_inicio, pin)
            VALUES (%s, %s, %s, %s, 'Activa', %s, %s)
        """, (usuario_id, bicicleta_id, origen_id, destino_id, datetime.now(), pin))

        self.cursor.execute("UPDATE terminales SET ocupadas = ocupadas - 1 WHERE id = %s", (origen_id,))
        self.db.commit()

        return {
            "success": True,
            "message": f"Reserva confirmada. Bicicleta ID: {bicicleta_id}, PIN: {pin}",
            "bicicleta_id": bicicleta_id,
            "pin": pin
        }

    def obtenerReservaPorPin(self, pin):
        self.db = DBConnection().conectar()
        self.cursor = self.db.cursor(dictionary=True)

        query = """
        SELECT r.*, b.estado AS estado_bicicleta
        FROM reservas r
        JOIN bicicletas b ON r.bicicleta_id = b.id
        WHERE r.pin = %s AND r.estado = 'Activa'
        """
        self.cursor.execute(query, (pin,))
        return self.cursor.fetchone()

    def devolverBicicleta(self, usuario_id):
        self.db = DBConnection().conectar()
        self.cursor = self.db.cursor(dictionary=True)

        self.cursor.execute("SELECT * FROM reservas WHERE usuario_id = %s AND estado = 'Activa'", (usuario_id,))
        reserva = self.cursor.fetchone()

        if not reserva:
            return {"success": False, "message": "No hay reservas activas para este usuario."}

        self.cursor.execute("SELECT capacidad, ocupadas FROM terminales WHERE id = %s", (reserva['terminal_destino_id'],))
        terminal = self.cursor.fetchone()
        if terminal['ocupadas'] >= terminal['capacidad']:
            return {"success": False, "message": "No hay espacio en la terminal de destino."}

        try:
            hora_inicio = reserva['hora_inicio']
            hora_fin = datetime.now()
            tiempo_usado = hora_fin - hora_inicio
            minutos_usados = tiempo_usado.total_seconds() / 60
            penalizado = minutos_usados > 30

            self.cursor.execute("UPDATE bicicletas SET estado = 'Disponible', terminal_id = %s WHERE id = %s",
                                (reserva['terminal_destino_id'], reserva['bicicleta_id']))

            self.cursor.execute("UPDATE reservas SET estado = 'Completada', hora_fin = %s WHERE id = %s",
                                (hora_fin, reserva['id']))

            self.cursor.execute("UPDATE terminales SET ocupadas = ocupadas + 1 WHERE id = %s",
                                (reserva['terminal_destino_id'],))

            if penalizado:
                self.cursor.execute("SELECT intentos_fallidos FROM usuarios WHERE id = %s", (usuario_id,))
                usuario = self.cursor.fetchone()
                nuevos_intentos = usuario['intentos_fallidos'] + 1

                if nuevos_intentos >= 3:
                    self.cursor.execute("UPDATE usuarios SET estado = 'Bloqueado', intentos_fallidos = %s WHERE id = %s",
                                        (nuevos_intentos, usuario_id))
                    self.db.commit()
                    return {"success": False, "message": "Has sido bloqueado por exceder el tiempo 3 veces."}
                else:
                    self.cursor.execute("UPDATE usuarios SET intentos_fallidos = %s WHERE id = %s",
                                        (nuevos_intentos, usuario_id))
                    self.db.commit()
                    return {"success": True, "message": f"Bicicleta devuelta. Pero excediste el tiempo. Advertencia {nuevos_intentos}/3."}

            self.db.commit()
            return {"success": True, "message": "Bicicleta devuelta con éxito."}

        except Exception as e:
            return {"success": False, "message": f"Error al devolver: {str(e)}"}

    def obtenerHistorial(self, usuario_id):
        self.db = DBConnection().conectar()
        self.cursor = self.db.cursor(dictionary=True)

        query = """
        SELECT r.id, b.codigo AS bicicleta, t1.nombre AS terminal_origen, 
               t2.nombre AS terminal_destino, r.estado, r.hora_inicio, r.hora_fin
        FROM reservas r
        JOIN bicicletas b ON r.bicicleta_id = b.id
        JOIN terminales t1 ON r.terminal_origen_id = t1.id
        JOIN terminales t2 ON r.terminal_destino_id = t2.id
        WHERE r.usuario_id = %s
        ORDER BY r.hora_inicio DESC
        """
        self.cursor.execute(query, (usuario_id,))
        return self.cursor.fetchall()

    def cambiarDestino(self, usuario_id, nueva_terminal_id):
        self.db = DBConnection().conectar()
        self.cursor = self.db.cursor(dictionary=True)
        
        self.cursor.execute("SELECT * FROM reservas WHERE usuario_id = %s AND estado = 'Activa'", (usuario_id,))
        reserva = self.cursor.fetchone()

        if not reserva:
            return {"success": False, "message": "No tienes reservas activas para cambiar."}

        self.cursor.execute("SELECT capacidad, ocupadas FROM terminales WHERE id = %s", (nueva_terminal_id,))
        terminal = self.cursor.fetchone()

        if not terminal:
            return {"success": False, "message": "La terminal seleccionada no existe."}

        if terminal['ocupadas'] >= terminal['capacidad']:
            return {"success": False, "message": "No hay espacio en la nueva terminal seleccionada."}

        self.cursor.execute("UPDATE reservas SET terminal_destino_id = %s WHERE id = %s", (nueva_terminal_id, reserva['id']))
        self.db.commit()

        return {"success": True, "message": "Terminal de destino actualizada exitosamente."}
    def obtenerReservaActivaConDestino(self, usuario_id):
        self.db = DBConnection().conectar()
        self.cursor = self.db.cursor(dictionary=True)
        query = """
        SELECT r.id, t.nombre AS terminal_destino
        FROM reservas r
        JOIN terminales t ON r.terminal_destino_id = t.id
        WHERE r.usuario_id = %s AND r.estado = 'Activa'
        LIMIT 1
        """
        self.cursor.execute(query, (usuario_id,))
        return self.cursor.fetchone()

    def guardarReporte(self, usuario_id, descripcion):
        self.db = DBConnection().conectar()
        self.cursor = self.db.cursor(dictionary=True)
        query = """
        INSERT INTO reportar_problema (usuario_id, descripcion, fecha_reporte)
        VALUES (%s, %s, NOW())
        """
        self.cursor.execute(query, (usuario_id, descripcion))
        self.db.commit()
        return {"success": True, "message": "Reporte enviado correctamente."}

    def reportarBicicletaDanada(self, usuario_id, bicicleta_id, tipo_problema, descripcion):
        try:
            self.cursor.execute("""
                INSERT INTO reportes_problemas (usuario_id, bicicleta_id, tipo_problema, descripcion)
                VALUES (%s, %s, %s, %s)
            """, (usuario_id, bicicleta_id, tipo_problema, descripcion))

            self.cursor.execute("UPDATE bicicletas SET estado = 'Mantenimiento' WHERE id = %s", (bicicleta_id,))
            self.db.commit()

            return {"success": True, "message": "Bicicleta reportada como dañada y marcada en mantenimiento."}
        except Exception as e:
            return {"success": False, "message": str(e)}


    def cerrarConexion(self):
        self.cursor.close()
        self.db.close()
