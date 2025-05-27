from models.reporteModel import ReporteModel

class ReporteController:
    def __init__(self):
        self.reporteModel = ReporteModel()

    def reportarProblemas(self, usuario_id, descripcion):
        reserva = self.reservaModel.obtenerReservaActivaConDestino(usuario_id)
        if not reserva:
            return {"success": False, "message": "No tienes ninguna bicicleta activa para reportar."}

        resultado = self.reservaModel.guardarReporte(usuario_id, descripcion)
        self.reservaModel.cerrarConexion()
        return resultado

    def verReportes(self, estado_filtro=None):
        reportes = self.reporteModel.obtenerReportes(estado_filtro)
        self.reporteModel.cerrarConexion()

        if not reportes:
            return {"success": False, "message": "No hay reportes disponibles."}
        else:
            return {"success": True, "reportes": reportes}

    def procesarRevision(self, reporte_id, bicicleta_id, nuevo_estado_bici, nuevo_estado_reporte):
        if nuevo_estado_bici not in ['Disponible', 'Mantenimiento']:
            return {"success": False, "message": "Estado de bicicleta no válido."}
        
        if nuevo_estado_reporte not in ['Revisado', 'Resuelto']:
            return {"success": False, "message": "Estado del reporte no válido."}

        try:
            self.reporteModel.actualizarEstadoBicicleta(bicicleta_id, nuevo_estado_bici)
            self.reporteModel.actualizarEstadoReporte(reporte_id, nuevo_estado_reporte)
            self.reporteModel.cerrarConexion()
            return {"success": True, "message": "Bicicleta y reporte actualizados correctamente."}
        except Exception as e:
            return {"success": False, "message": f"Error al actualizar: {str(e)}"}
