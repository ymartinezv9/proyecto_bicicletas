from models.reservaModel import ReservaModel

class ReservaController:
    def __init__(self):
        self.reservaModel = ReservaModel()

    def realizarReserva(self, datos):
        usuario_id = datos.get('usuario_id')
        origen_id = datos.get('origen_id')
        destino_id = datos.get('destino_id')

        resultado = self.reservaModel.crearReserva(usuario_id, origen_id, destino_id)
        self.reservaModel.cerrarConexion()
        return resultado

    def desbloquearBicicleta(self, datos):
        pin = datos.get('pin')

        reserva = self.reservaModel.obtenerReservaPorPin(pin)

        if not reserva:
            self.reservaModel.cerrarConexion()
            return {"success": False, "message": "PIN inválido o la reserva ya fue completada/cancelada."}

        if reserva['estado_bicicleta'] == 'Mantenimiento':
            self.reservaModel.cerrarConexion()
            return {"success": False, "message": "La bicicleta está en mantenimiento."}

        self.reservaModel.cerrarConexion()
        return {
            "success": True,
            "message": "Bicicleta desbloqueada. ¡Disfruta tu viaje!",
            "bicicleta_id": reserva['bicicleta_id']
        }

    def procesarDevolucion(self, usuario_id):
        resultado = self.reservaModel.devolverBicicleta(usuario_id)
        self.reservaModel.cerrarConexion()
        return resultado

    def verHistorial(self, usuario_id):
        historial = self.reservaModel.obtenerHistorial(usuario_id)
        self.reservaModel.cerrarConexion()

        if not historial:
            return {"success": False, "message": "No se ha realizado ningún préstamo."}
        else:
            return {"success": True, "historial": historial}

    def modificarTerminalDestino(self, usuario_id, nueva_terminal_id):
        resultado = self.reservaModel.cambiarDestino(usuario_id, nueva_terminal_id)
        self.reservaModel.cerrarConexion()
        return resultado
    def obtenerReservaActiva(self, usuario_id):
        reserva = self.reservaModel.obtenerReservaActivaConDestino(usuario_id)
        self.reservaModel.cerrarConexion()

        if not reserva:
            return {"success": False, "message": "No tienes reservas activas."}
        
        return {
            "success": True,
            "reserva": {
                "destino": reserva["terminal_destino"]
            }
        }
    def reportarProblema(self, usuario_id, descripcion):
        reserva = self.reservaModel.obtenerReservaActivaConDestino(usuario_id)
        if not reserva:
            return {"success": False, "message": "No tienes ninguna bicicleta activa para reportar."}

        resultado = self.reservaModel.guardarReporte(usuario_id, descripcion)
        self.reservaModel.cerrarConexion()
        return resultado
