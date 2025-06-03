document.addEventListener('DOMContentLoaded', async () => {
  const usuario = JSON.parse(localStorage.getItem('usuario'));
  if (!usuario || usuario.tipo !== 'Administrador') {
    alert("Acceso no autorizado.");
    window.location.href = 'login.html';
    return;
  }

  const tablaBody = document.querySelector('#tablaBicicletas tbody');

  try {
    const res = await fetch('http://localhost:5000/api/bicicletas');
    const datos = await res.json();

    datos.forEach(b => {
      const fila = document.createElement('tr');

      fila.innerHTML = `
        <td>${b.id}</td>
        <td>${b.codigo}</td>
        <td>${b.estado}</td>
        <td>${b.terminal || 'Sin asignar'}</td>
      `;

      tablaBody.appendChild(fila);
    });

    // Activar DataTables
    $(document).ready(function () {
      $('#tablaBicicletas').DataTable({
        language: {
          url: '//cdn.datatables.net/plug-ins/1.13.6/i18n/es-ES.json'
        }
      });
    });

  } catch (error) {
    alert("Error al cargar bicicletas.");
    console.error(error);
  }
});
