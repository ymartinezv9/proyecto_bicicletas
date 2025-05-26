from models.preferenciasModel import PreferenciasModel

class PreferenciasController:
    def __init__(self):
        self.model = PreferenciasModel()

    def cambiarNotificaciones(self, usuario_id, activar):
        self.model = PreferenciasModel()
        estado = True if activar else False
        self.model.actualizarNotificaciones(usuario_id, estado)
        self.model.cerrarConexion()
        return {"success": True, "message": f"Notificaciones {'activadas' if estado else 'desactivadas'}."}

    def agregarRutaFavorita(self, usuario_id, origen_id, destino_id):
        self.model = PreferenciasModel()
        resultado = self.model.agregarRutaFavorita(usuario_id, origen_id, destino_id)
        self.model.cerrarConexion()
        return resultado

    def verPreferencias(self, usuario_id):
        self.model = PreferenciasModel()
        datos = self.model.obtenerPreferencias(usuario_id)
        self.model.cerrarConexion()
        return {"success": True, "data": datos}
