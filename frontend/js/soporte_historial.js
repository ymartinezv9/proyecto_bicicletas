document.addEventListener('DOMContentLoaded', async () => {
  const usuario = JSON.parse(localStorage.getItem('usuario'));
  if (!usuario) {
    alert("Debes iniciar sesión.");
    window.location.href = 'login.html';
    return;
  }

  try {
    const res = await fetch(`http://localhost:5000/api/soporte/mensajes/usuario/${usuario.id}`);
    const data = await res.json();

    const tbody = document.querySelector('#tablaMensajes tbody');
    tbody.innerHTML = '';

    if (data.success && data.mensajes.length > 0) {
      data.mensajes.forEach(m => {
        const row = `
          <tr>
            <td>${m.asunto}</td>
            <td>${m.mensaje}</td>
            <td>${new Date(m.fecha).toLocaleString()}</td>
            <td>${m.estado}</td>
          </tr>
        `;
        tbody.innerHTML += row;
      });
    } else {
      tbody.innerHTML = '<tr><td colspan="4">No has enviado mensajes al soporte.</td></tr>';
    }

  } catch (error) {
    console.error(error);
    alert("Error al obtener historial.");
  }
});
