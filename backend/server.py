from flask import Flask, request, jsonify
from flask_cors import CORS

from controllers.usuarioController import UsuarioController
from controllers.reservaController import ReservaController
from controllers.terminalController import TerminalController

app = Flask(__name__)
CORS(app)  # Permite solicitudes desde cualquier origen (frontend)


usuarioCtrl = UsuarioController()
reservaCtrl = ReservaController()
terminalCtrl = TerminalController()

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



if __name__ == '__main__':
    app.run(debug=True, port=5000)
