from models.preferenciasModel import PreferenciasModel

class PreferenciasController:
    def __init__(self):
        self.model = PreferenciasModel()

    def cambiarNotificaciones(self, usuario_id, activar):
        estado = True if activar else False
        self.model.actualizarNotificaciones(usuario_id, estado)
        self.model.cerrarConexion()
        return {"success": True, "message": f"Notificaciones {'activadas' if estado else 'desactivadas'}."}

    def agregarRutaFavorita(self, usuario_id, origen_id, destino_id):
        self.model.agregarRutaFavorita(usuario_id, origen_id, destino_id)
        self.model.cerrarConexion()
        return {"success": True, "message": "Ruta favorita guardada correctamente."}

    def verPreferencias(self, usuario_id):
        datos = self.model.obtenerPreferencias(usuario_id)
        self.model.cerrarConexion()
        return {"success": True, "data": datos}
