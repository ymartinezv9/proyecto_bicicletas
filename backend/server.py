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


import requests
import os

@app.route('/api/clima', methods=['GET'])
def obtener_clima():
    # Usa tu propia API key aquí
    api_key = os.getenv("OPENWEATHER_API_KEY", "edf3f9680b1a391f6309d2b920c7156b")  # Reemplaza con tu API key real
    ciudad = "Guatemala"  # Puedes cambiarlo si gustas

    url = f"https://api.openweathermap.org/data/2.5/weather?q={ciudad}&appid={api_key}&units=metric&lang=es"

    try:
        response = requests.get(url)
        data = response.json()

        temperatura = data["main"]["temp"]
        descripcion = data["weather"][0]["description"]

        return jsonify({
            "temperatura": temperatura,
            "descripcion": descripcion.capitalize()
        })
    except Exception as e:
        return jsonify({
            "temperatura": None,
            "descripcion": "No se pudo obtener el clima"
        }), 500


@app.route('/api/rutas-sugeridas', methods=['GET'])
def rutas_sugeridas():
    from models.terminalModel import TerminalModel
    modelo = TerminalModel()
    query = """
        SELECT 
        t1.nombre AS origen,
        t2.nombre AS destino,
        t1.latitud AS lat_origen,
        t1.longitud AS lon_origen,
        t2.latitud AS lat_destino,
        t2.longitud AS lon_destino
        FROM terminales t1
        JOIN terminales t2 ON t1.id < t2.id
        WHERE
        (SELECT COUNT(*) FROM bicicletas WHERE terminal_id = t1.id AND estado = 'Disponible') > 0
        AND (SELECT capacidad - ocupadas FROM terminales WHERE id = t2.id) > 0
        LIMIT 5
        """
    modelo.cursor.execute(query)
    rutas = modelo.cursor.fetchall()
    modelo.cerrarConexion()
    return jsonify(rutas)

@app.route('/api/reportar-danio', methods=['POST'])
def reportar_danio():
    datos = request.json
    return jsonify(reservaCtrl.reportarDanioBicicleta(
        datos['usuario_id'],
        datos['bicicleta_id'],
        datos['tipo_problema'],
        datos['descripcion']
    ))

@app.route('/api/bicicletas/activas', methods=['GET'])
def obtener_bicicletas_activas():
    from models.reservaModel import ReservaModel
    modelo = ReservaModel()
    query = """
        SELECT b.id, b.codigo, b.estado, t.nombre AS terminal
        FROM bicicletas b
        LEFT JOIN terminales t ON b.terminal_id = t.id
        WHERE b.estado IN ('Disponible', 'En Uso')
    """
    modelo.cursor.execute(query)
    bicicletas = modelo.cursor.fetchall()
    modelo.cerrarConexion()
    return jsonify(bicicletas)

@app.route('/api/bicicletas/mantenimiento/<int:tecnico_id>', methods=['GET'])
def ver_bicicletas_mantenimiento(tecnico_id):
    # Opcionalmente podrías validar si el usuario es Técnico
    from controllers.bicicletaController import BicicletaController
    controller = BicicletaController()
    return jsonify(controller.bicicletasEnMantenimiento())


@app.route('/api/soporte/mensaje', methods=['POST'])
def enviar_mensaje_soporte():
    datos = request.json
    from controllers.soporteController import SoporteController
    controller = SoporteController()
    return jsonify(controller.enviarMensajeSoporte(datos['usuario_id'], datos['asunto'], datos['mensaje']))

@app.route('/api/soporte/mensajes', methods=['GET'])
def obtener_mensajes_soporte():
    from controllers.soporteController import SoporteController
    controller = SoporteController()
    return jsonify(controller.verMensajesPendientes())

@app.route('/api/soporte/mensaje/<int:mensaje_id>/atender', methods=['PUT'])
def atender_mensaje_soporte(mensaje_id):
    from controllers.soporteController import SoporteController
    controller = SoporteController()
    return jsonify(controller.atenderMensaje(mensaje_id))

@app.route('/api/soporte/mensajes/usuario/<int:usuario_id>', methods=['GET'])
def ver_mensajes_usuario(usuario_id):
    from controllers.soporteController import SoporteController
    controller = SoporteController()
    return jsonify(controller.verMensajesUsuario(usuario_id))

@app.route('/api/terminales/alertas', methods=['GET'])
def alertas_disponibilidad():
    from controllers.terminalController import TerminalController
    controller = TerminalController()
    return jsonify(controller.verificarRedistribucion())

@app.route('/api/bicicletas/disponibles', methods=['GET'])
def bicicletas_disponibles():
    from controllers.bicicletaController import BicicletaController
    ctrl = BicicletaController()
    return jsonify(ctrl.obtenerBicicletasDisponibles())

@app.route('/api/bicicletas/mover', methods=['POST'])
def mover_bicicleta():
    datos = request.json
    from controllers.bicicletaController import BicicletaController
    ctrl = BicicletaController()
    return jsonify(ctrl.mover(datos['bicicleta_id'], datos['terminal_id']))


@app.route('/api/bicicletas/estado', methods=['GET'])
def estado_bicicletas():
    from controllers.bicicletaController import BicicletaController
    ctrl = BicicletaController()
    return jsonify(ctrl.obtenerEstadoBicicletas())



@app.route('/api/usuarios', methods=['GET'])
def ver_usuarios():
    from controllers.usuarioController import UsuarioController
    ctrl = UsuarioController()
    return jsonify(ctrl.listarUsuarios())

@app.route('/api/usuarios/estado', methods=['POST'])
def cambiar_estado_usuario():
    datos = request.json
    from controllers.usuarioController import UsuarioController
    ctrl = UsuarioController()
    return jsonify(ctrl.modificarEstado(datos['usuario_id'], datos['estado']))

@app.route('/api/bicicletas/mantenimiento', methods=['GET'])
def ver_mantenimiento():
    from controllers.bicicletaController import BicicletaController
    ctrl = BicicletaController()
    return jsonify(ctrl.verMantenimiento())


@app.route('/api/bicicletas/estado', methods=['POST'])
def cambiar_estado_bicicleta():
    datos = request.json
    from controllers.bicicletaController import BicicletaController
    ctrl = BicicletaController()
    return jsonify(ctrl.cambiarEstado(datos['bicicleta_id'], datos['estado']))


@app.route('/api/bicicletas/historial/<int:bicicleta_id>', methods=['GET'])
def ver_historial_bici(bicicleta_id):
    from controllers.bicicletaController import BicicletaController
    ctrl = BicicletaController()
    return jsonify(ctrl.verHistorial(bicicleta_id))

@app.route('/api/bicicletas/historial', methods=['POST'])
def guardar_historial():
    datos = request.json
    from controllers.bicicletaController import BicicletaController
    ctrl = BicicletaController()
    return jsonify(ctrl.guardarHistorial(
        datos['bicicleta_id'],
        datos.get('usuario_id'),
        datos['tipo'],
        datos['descripcion'],
        datos.get('estado', 'Pendiente')
    ))

@app.route('/api/bicicletas/historial/buscar/<string:termino>', methods=['GET'])
def buscar_historial(termino):
    from controllers.bicicletaController import BicicletaController
    ctrl = BicicletaController()
    return jsonify(ctrl.buscarHistorial(termino))


if __name__ == '__main__':
    app.run(debug=True, port=5000)
 