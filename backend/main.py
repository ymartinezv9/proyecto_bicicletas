from config.dbConnection import DBConnection
from controllers.usuarioController import UsuarioController
from controllers.reservaController import ReservaController
from controllers.reporteController import ReporteController
from controllers.bicicletaController import BicicletaController
from controllers.soporteController import SoporteController
from controllers.preferenciasController import PreferenciasController
from controllers.terminalController import TerminalController



def main():

    db = DBConnection()
    conexion = db.conectar()
    
    if conexion:
        print("Conexión verificada.")
        db.cerrar()
    else:
        print("No se pudo conectar a la base de datos.")
 
    controller = UsuarioController()
'''
    # Prueba de registro 
    # nuevoUsuario = {
    #     "nombre": "Lutwing Martínez",
    #     "correo": "lutwing@example.com",
    #     "cui": "1234567890101",
    #     "telefono": "55512345",
    #     "contrasena": "miContrasena123"
    # }
    # print(controller.registrarUsuario(nuevoUsuario))

    # Prueba de inicio de sesión
    # correo = "lutwing@example.com"
    #contrasena = "miContrasena123"  # Prueba con la contraseña correcta e incorrecta
    
    #resultado = controller.iniciarSesion(correo, contrasena)
    #print(resultado)


    reservaCtrl = ReservaController()

    usuario_id = 1         # Asegúrate de que este usuario exista
    origen_id = 1          # ID de la terminal de origen
    destino_id = 2         # ID de la terminal de destino


    resultado = reservaCtrl.reservarBicicleta(usuario_id, origen_id, destino_id)
    print(resultado)


reservaCtrl = ReservaController()

pin = input("Ingresa el PIN de tu reserva: ").strip()
resultado = reservaCtrl.desbloquearBicicleta(pin)
print(resultado)

reservaCtrl = ReservaController()

usuario_id = int(input("Ingresa tu ID de usuario para devolver la bicicleta: ").strip())
resultado = reservaCtrl.procesarDevolucion(usuario_id)
print(resultado)

reservaCtrl = ReservaController()

usuario_id = int(input("Ingrese su ID de usuario para ver historial: ").strip())
resultado = reservaCtrl.verHistorial(usuario_id)

if resultado["success"]:
    print("Historial de préstamos:")
    for r in resultado["historial"]:
        print(f"- #{r['id']} | Bicicleta: {r['bicicleta']} | Origen: {r['terminal_origen']} → Destino: {r['terminal_destino']} | Estado: {r['estado']} | Fecha: {r['fecha_reserva']}")
else:
    print(resultado["message"])

reporteCtrl = ReporteController()

print("Reportar problema con bicicleta")
usuario_id = int(input("ID del usuario: "))
bicicleta_id = int(input("ID de la bicicleta: "))
tipo_problema = input("Tipo de problema (frenos, llantas, cadena, etc.): ")
descripcion = input("Descripción adicional (opcional): ")

resultado = reporteCtrl.reportarProblema(usuario_id, bicicleta_id, tipo_problema, descripcion)
print(resultado)

reporteCtrl = ReporteController()

print("Ver reportes de bicicletas")
filtro = input("¿Desea filtrar por estado? (Pendiente, Revisado, Resuelto) [deja vacío para todos]: ").strip()
filtro = filtro if filtro else None

resultado = reporteCtrl.verReportes(filtro)

if resultado["success"]:
    print("Reportes encontrados:")
    for r in resultado["reportes"]:
        print(f"- #{r['id']} | Bicicleta: {r['bicicleta']} | Usuario: {r['usuario']} | Problema: {r['tipo_problema']} | Estado: {r['estado']} | Fecha: {r['fecha_reporte']}")
else:
    print(resultado["message"])

ctrl = ReporteController()

print("Procesar revisión de bicicleta reportada")
reporte_id = int(input("ID del reporte: "))
bicicleta_id = int(input("ID de la bicicleta: "))
nuevo_estado_bici = input("Nuevo estado de bicicleta (Disponible/Mantenimiento): ").strip()
nuevo_estado_reporte = input("Nuevo estado de reporte (Revisado/Resuelto): ").strip()

resultado = ctrl.procesarRevision(reporte_id, bicicleta_id, nuevo_estado_bici, nuevo_estado_reporte)
print(resultado)


ctrl = BicicletaController()

print("Bloqueo remoto de bicicleta (ADMINISTRADOR)")
bicicleta_id = int(input("Ingrese el ID de la bicicleta a bloquear: "))

resultado = ctrl.bloquearRemotamente(bicicleta_id)
print(resultado)


soporteCtrl = SoporteController()

print("Contactar al soporte")
usuario_id = int(input("ID del usuario: "))
asunto = input("Asunto del mensaje: ").strip()
mensaje = input("Describe tu problema o duda: ").strip()

resultado = soporteCtrl.enviarMensajeSoporte(usuario_id, asunto, mensaje)
print(resultado)


ctrl = PreferenciasController()

print("Gestión de Preferencias")
usuario_id = int(input("ID de usuario: "))

accion = input("¿Deseas (1) cambiar notificaciones, (2) agregar ruta favorita, (3) ver preferencias? ")

if accion == "1":
    activar = input("¿Activar notificaciones? (s/n): ").lower() == 's'
    print(ctrl.cambiarNotificaciones(usuario_id, activar))

elif accion == "2":
    origen = int(input("ID terminal origen: "))
    destino = int(input("ID terminal destino: "))
    print(ctrl.agregarRutaFavorita(usuario_id, origen, destino))

elif accion == "3":
    resultado = ctrl.verPreferencias(usuario_id)
    if resultado["success"]:
        prefs = resultado["data"]
        print(f"Notificaciones: {'activadas' if prefs['notificaciones'] else 'desactivadas'}")            
        print("Rutas favoritas:")
        for r in prefs["rutas_favoritas"]:
            print(f"- {r['origen']} → {r['destino']}")
    else:
        print("No hay preferencias registradas.")


reservaCtrl = ReservaController()

print("Cambiar terminal de destino")
usuario_id = int(input("ID del usuario: "))
nueva_terminal_id = int(input("Nueva terminal de destino (ID): "))

resultado = reservaCtrl.modificarTerminalDestino(usuario_id, nueva_terminal_id)
print(resultado)

ctrl = BicicletaController()

print("Estado general de todas las bicicletas")
resultado = ctrl.verEstadoGeneral()

if resultado["success"]:
    for bici in resultado["bicicletas"]:
        terminal = bici["terminal"] if bici["terminal"] else "Sin terminal"
        print(f"- ID: {bici['id']} | Código: {bici['codigo']} | Estado: {bici['estado']} | Terminal: {terminal}")
else:
    print(resultado["message"])

ctrl = BicicletaController()
print("Ubicación en tiempo real de bicicletas")
resultado = ctrl.verUbicacionTiempoReal()

if resultado["success"]:
    for bici in resultado["ubicaciones"]:
         print(f" {bici['codigo']} | Estado: {bici['estado']} | Ubicación: ({bici['latitud']}, {bici['longitud']})")
else:
    print(resultado["message"])
   
ctrl = TerminalController()
print("Verificar necesidad de redistribución de bicicletas")
resultado = ctrl.verificarRedistribucion()

if "alertas" in resultado:
    print("Terminales con menos del 25% de bicicletas:")
    for t in resultado["alertas"]:
        print(f"- {t['nombre']} ({t['ocupadas']}/{t['capacidad']}) → {t['porcentaje_ocupacion']}%")
else:
    print(resultado["message"])


ctrl = BicicletaController()

print("Ubicación en tiempo real de bicicletas")
resultado = ctrl.verUbicacionTiempoReal()

if resultado["success"]:
    for bici in resultado["ubicaciones"]:
        print(f"{bici['codigo']} | Estado: {bici['estado']} | Ubicación: ({bici['latitud']}, {bici['longitud']})")
else:
    print(resultado["message"])

ctrl = TerminalController()

print("Verificar necesidad de redistribución de bicicletas")
resultado = ctrl.verificarRedistribucion()

if "alertas" in resultado:
    print("Terminales con menos del 25% de bicicletas:")
    for t in resultado["alertas"]:
        print(f"- {t['nombre']} ({t['ocupadas']}/{t['capacidad']}) → {t['porcentaje_ocupacion']}%")
else:
    print(resultado["message"])
'''

ctrl = TerminalController()

print("Disponibilidad de bicicletas por terminal")
resultado = ctrl.verDisponibilidad()

if resultado["success"]:
    for t in resultado["terminales"]:
        print(f"- {t['nombre']} | Bicicletas disponibles: {t['ocupadas']} | Espacios libres: {t['espacios_libres']} / {t['capacidad']}")
else:
    print(resultado["message"])


if __name__ == "__main__":
    main()
