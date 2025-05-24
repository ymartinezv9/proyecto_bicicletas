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
