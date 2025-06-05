from models.bicicletaModel import BicicletaModel

class BicicletaController:
    def __init__(self):
        self.bicicletaModel = BicicletaModel()

    def bloquearRemotamente(self, bicicleta_id):
        bici = self.bicicletaModel.obtenerBicicletaPorId(bicicleta_id)

        if not bici:
            return {"success": False, "message": "Bicicleta no encontrada."}

        if bici['estado'] in ['Mantenimiento', 'Fuera de servicio']:
            return {"success": False, "message": "No se puede bloquear una bicicleta en mantenimiento o fuera de servicio."}

        self.bicicletaModel.bloquearBicicleta(bicicleta_id)
        self.bicicletaModel.cerrarConexion()
        return {"success": True, "message": "Bicicleta bloqueada remotamente con éxito."}
    
    def verEstadoGeneral(self):
        bicicletas = self.bicicletaModel.obtenerTodasLasBicicletas()
        self.bicicletaModel.cerrarConexion()

        if not bicicletas:
            return {"success": False, "message": "No hay bicicletas registradas."}
        
        return {"success": True, "bicicletas": bicicletas}


    def verUbicacionTiempoReal(self):
        ubicaciones = self.bicicletaModel.obtenerUbicaciones()
        self.bicicletaModel.cerrarConexion()

        if not ubicaciones:
            return {"success": False, "message": "No hay ubicaciones registradas."}
        
        return {"success": True, "ubicaciones": ubicaciones}
    
    def bicicletasEnMantenimiento(self):
        resultado = self.bicicletaModel.obtenerBicicletasEnMantenimiento()
        self.bicicletaModel.cerrarConexion()
        return {"success": True, "bicicletas": resultado}
    
    def obtenerBicicletasDisponibles(self):
        data = self.bicicletaModel.bicicletasDisponibles()
        self.bicicletaModel.cerrarConexion()
        return {"success": True, "bicicletas": data}

    def mover(self, bicicleta_id, terminal_id):
        resultado = self.bicicletaModel.moverBicicleta(bicicleta_id, terminal_id)
        self.bicicletaModel.cerrarConexion()
        return resultado
    
    def obtenerEstadoBicicletas(self):
        data = self.bicicletaModel.estadoBicicletas()
        self.bicicletaModel.cerrarConexion()
        return {"success": True, "bicicletas": data}

    def verMantenimiento(self):
        bicicletas = self.bicicletaModel.obtenerEnMantenimiento()
        self.bicicletaModel.cerrarConexion()
        return {"success": True, "bicicletas": bicicletas}

    def cambiarEstado(self, bicicleta_id, nuevo_estado):
        self.bicicletaModel.actualizarEstado(bicicleta_id, nuevo_estado)
        self.bicicletaModel.cerrarConexion()
        return {"success": True, "message": f"Bicicleta actualizada a {nuevo_estado}"}
    

    def guardarHistorial(self, bicicleta_id, usuario_id, tipo, descripcion, estado='Pendiente'):
        self.bicicletaModel.registrarHistorial(bicicleta_id, usuario_id, tipo, descripcion, estado)
        self.bicicletaModel.cerrarConexion()
        return {"success": True, "message": "Historial registrado"}

    def verHistorial(self, bicicleta_id):
        historial = self.bicicletaModel.obtenerHistorialPorBicicleta(bicicleta_id)
        self.bicicletaModel.cerrarConexion()
        return {"success": True, "historial": historial}
