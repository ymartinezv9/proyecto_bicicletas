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
        </ul>
      `;
      break;




    case 'Técnico':
      opciones.innerHTML = `
        <ul>
          <li><a href="#">Reportes Técnicos</a></li>
          <li><a href="#">Revisiones</a></li>
        </ul>
      `;
      break;
    case 'Administrador':
      opciones.innerHTML = `
        <ul>
          <li><a href="#">Estadísticas</a></li>
          <li><a href="#">Bloqueos</a></li>
        </ul>
      `;
      break;
    default:
      opciones.innerHTML = "<p>Rol no reconocido.</p>";
  }
});
