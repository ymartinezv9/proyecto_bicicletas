document.addEventListener('DOMContentLoaded', () => {
  const usuario = JSON.parse(localStorage.getItem('usuario'));
  const opciones = document.getElementById('opciones');
  const titulo = document.getElementById('titulo-bienvenida');

  if (!usuario) {
    alert("No has iniciado sesión.");
    window.location.href = 'login.html';
    return;
  }

  titulo.textContent = `Bienvenido, ${usuario.nombre}`;
  
  switch (usuario.tipo) {

    case 'Usuario':
      opciones.innerHTML = `
        <ul>
          <li><a href="reservar.html">Reservar Bicicleta</a></li>
          <li><a href="prestar.html">Recoger bicicleta con PIN</a></li>
          <li><a href="devolver.html">Devolver Bicicleta</a></li>
          <li><a href="historial.html">Ver Historial</a></li>
          <li><a href="preferencias.html">Preferencias</a></li>
          <li><a href="cambiar_destino.html" class="btn">Cambiar Terminal de Destino</a></li>
          <li><a href="reportar_problema.html">Reportar Problema</a></li>
          <li><a href="disponibilidad.html">Consultar Disponibilidad</a></li>
          <li><a href="espacios.html">Verificar Espacio para Devolución</a></li>
          <li><a href="rutas.html">Rutas y Clima</a></li>
          <li><a href="reportar_danio.html">Reportar Bicicleta Dañada</a></li>
          <li><a href="soporte.html">Contactar Soporte</a></li>
        </ul>
      `;
      break;


    case 'Tecnico':
      opciones.innerHTML = `
        <ul>
          <li><a href="bicicletas_mantenimiento.html">Bicicletas en Mantenimiento</a></li>
          <li><a href="#">Revisiones</a></li>
        </ul>
      `;
      break;

    case 'Soporte':
      opciones.innerHTML = `
        <ul>
          <li><a href="mensajes_soporte.html">Ver Mensajes de Soporte</a></li>
          <li><a href="#">Desbloquear bicicletas</a></li>
        </ul>
      `;
      break;
      
    case 'Administrador':
      opciones.innerHTML = `
        <ul>
          <li><a href="estado_bicicletas.html">Estado de Bicicletas</a></li>
          <li><a href="#">Ubicacion en tiempo real</a></li> 
          <li><a href="#">Bloqueos</a></li>
          <li><a href="mover_bicicletas.html">Mover Bicicleta</a></li>
          <li><a href="gestionar_usuarios.html">Gestionar Usuarios</a></li>
          <li><a href="#">Estadísticas</a></li>
          
        </ul>
      `;
      break;

    default:
      opciones.innerHTML = "<p>Rol no reconocido.</p>";
  }
});
