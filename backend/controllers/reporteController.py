from models.reporteModel import ReporteModel

class ReporteController:
    def __init__(self):
        self.reporteModel = ReporteModel()

    def reportarProblema(self, usuario_id, bicicleta_id, tipo_problema, descripcion=""):
        if not tipo_problema:
            return {"success": False, "message": "Debe seleccionar un tipo de problema."}

        resultado = self.reporteModel.crearReporte(usuario_id, bicicleta_id, tipo_problema, descripcion)
        self.reporteModel.cerrarConexion()
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
