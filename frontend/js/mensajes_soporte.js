document.addEventListener('DOMContentLoaded', async () => {
  const usuario = JSON.parse(localStorage.getItem('usuario'));
  if (!usuario || usuario.tipo !== 'Soporte') {
    alert("Acceso restringido.");
    window.location.href = 'login.html';
    return;
  }

  async function cargarMensajes() {
    try {
      const res = await fetch('http://localhost:5000/api/soporte/mensajes');
      const data = await res.json();

      const tbody = document.querySelector('#tablaMensajes tbody');
      tbody.innerHTML = '';

      if (data.success && data.mensajes.length > 0) {
        data.mensajes.forEach(m => {
          const row = document.createElement('tr');

          row.innerHTML = `
            <td>${m.remitente}</td>
            <td>${m.asunto}</td>
            <td>${m.mensaje}</td>
            <td>${new Date(m.fecha).toLocaleString()}</td>
            <td>${m.estado}</td>
            <td>
              <button ${m.estado === 'Atendido' ? 'disabled' : ''} data-id="${m.id}">
                Marcar como Atendido
              </button>
            </td>
          `;

          tbody.appendChild(row);
        });

        document.querySelectorAll('button[data-id]').forEach(btn => {
          btn.addEventListener('click', async () => {
            const id = btn.getAttribute('data-id');
            const res = await fetch(`http://localhost:5000/api/soporte/mensaje/${id}/atender`, {
              method: 'PUT'
            });
            const result = await res.json();
            alert(result.message);
            cargarMensajes(); // Recargar tabla
          });
        });

      } else {
        tbody.innerHTML = '<tr><td colspan="6">No hay mensajes pendientes.</td></tr>';
      }

    } catch (error) {
      console.error(error);
      alert("Error al cargar mensajes.");
    }
  }

  cargarMensajes();
});
