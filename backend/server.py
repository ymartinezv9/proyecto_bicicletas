from flask import Flask, request, jsonify
from flask_cors import CORS

from controllers.preferenciasController import PreferenciasController
from controllers.usuarioController import UsuarioController
from controllers.reservaController import ReservaController
from controllers.terminalController import TerminalController

app = Flask(__name__)
CORS(app)  # Permite solicitudes desde cualquier origen (frontend)


usuarioCtrl = UsuarioController()
reservaCtrl = ReservaController()
terminalCtrl = TerminalController()
preferenciasCtrl = PreferenciasController()
reservaCtrl = ReservaController()


@app.route('/api/registro', methods=['POST'])
def registrar_usuario():
    datos = request.json
    resultado = usuarioCtrl.registrarUsuario(datos)
    return jsonify(resultado)

@app.route('/api/login', methods=['POST'])
def login_usuario():
    datos = request.json
    resultado = usuarioCtrl.iniciarSesion(datos)
    return jsonify(resultado)

@app.route('/api/terminales', methods=['GET'])
def listar_terminales():
    resultado = terminalCtrl.verDisponibilidad()
    if resultado["success"]:
        return jsonify(resultado["terminales"])
    return jsonify([])

@app.route('/api/reservar', methods=['POST'])
def reservar_bicicleta():
    datos = request.json
    resultado = reservaCtrl.realizarReserva(datos)
    return jsonify(resultado)


@app.route('/api/desbloquear', methods=['POST'])
def desbloquear_bicicleta():
    
    datos = request.get_json()
    if not datos:
        return jsonify({"success": False, "message": "No se recibieron datos"}), 400

    pin = datos.get('pin')
    if not pin:
        return jsonify({"success": False, "message": "Pin es requerido"}), 400

    resultado = reservaCtrl.desbloquearBicicleta(datos)
    return jsonify(resultado)


@app.route('/api/devolver', methods=['POST'])
def devolver_bicicleta():
    datos = request.json
    resultado = reservaCtrl.procesarDevolucion(datos['usuario_id'])
    return jsonify(resultado)


@app.route('/api/historial/<int:usuario_id>', methods=['GET'])
def historial_usuario(usuario_id):
    resultado = reservaCtrl.verHistorial(usuario_id)
    return jsonify(resultado)

@app.route('/api/preferencias/<int:usuario_id>', methods=['GET'])
def get_preferencias(usuario_id):
    return jsonify(preferenciasCtrl.verPreferencias(usuario_id))

@app.route('/api/preferencias/notificaciones', methods=['POST'])
def set_notificaciones():
    datos = request.json
    return jsonify(preferenciasCtrl.cambiarNotificaciones(datos['usuario_id'], datos['activar']))

@app.route('/api/preferencias/ruta', methods=['POST'])
def set_ruta_favorita():
    datos = request.json
    return jsonify(preferenciasCtrl.agregarRutaFavorita(datos['usuario_id'], datos['origen_id'], datos['destino_id']))

@app.route('/api/reservas/usuario/<int:usuario_id>', methods=['GET'])
def obtener_reserva_activa(usuario_id):
    # Lógica para mostrar terminal destino actual
    resultado = reservaCtrl.obtenerReservaActiva(usuario_id)
    return jsonify(resultado)

@app.route('/api/reservas/cambiar-destino', methods=['POST'])
def cambiar_terminal_destino():
    datos = request.json
    resultado = reservaCtrl.modificarTerminalDestino(
        datos['usuario_id'],
        datos['nueva_terminal_id']
    )
    return jsonify(resultado)

@app.route('/api/reportar_problema', methods=['POST'])
def reportar_problema():
    datos = request.json
    return jsonify(reservaCtrl.reportarProblema(datos['usuario_id'], datos['descripcion']))

@app.route('/api/terminal/<int:terminal_id>/espacio', methods=['GET'])
def verificar_espacio_terminal(terminal_id):
    from models.terminalModel import TerminalModel
    terminalModel = TerminalModel()
    query = "SELECT capacidad, ocupadas FROM terminales WHERE id = %s"
    terminalModel.cursor.execute(query, (terminal_id,))
    terminal = terminalModel.cursor.fetchone()
    terminalModel.cerrarConexion()

    if not terminal:
        return jsonify({"success": False, "message": "Terminal no encontrada"})

    if terminal['ocupadas'] >= terminal['capacidad']:
        return jsonify({"success": False, "message": "No hay espacio disponible en esta terminal."})
    else:
        return jsonify({"success": True, "message": "Sí hay espacio disponible para devolución."})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
 