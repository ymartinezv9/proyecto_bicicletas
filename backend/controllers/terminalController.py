from models.terminalModel import TerminalModel

class TerminalController:
    def __init__(self):
        self.terminalModel = TerminalModel()

    def verificarRedistribucion(self):
        terminales = self.terminalModel.obtenerTerminalesBajoMinimo()
        self.terminalModel.cerrarConexion()

        if not terminales:
            return {"success": True, "message": "Todas las terminales tienen suficiente disponibilidad."}
        
        return {"success": True, "alertas": terminales}

    
    def verDisponibilidad(self):
        terminales = self.terminalModel.obtenerDisponibilidad()
        self.terminalModel.cerrarConexion()

        if not terminales:
            return {"success": False, "message": "No hay terminales registradas."}
        
        return {"success": True, "terminales": terminales}
