document.addEventListener('DOMContentLoaded', async () => {
  const usuario = JSON.parse(localStorage.getItem('usuario'));
  if (!usuario || (usuario.tipo !== 'Administrador' && usuario.tipo !== 'Soporte')) {
    alert("Acceso denegado.");
    window.location.href = 'login.html';
    return;
  }

  try {
    const res = await fetch('http://localhost:5000/api/terminales/alertas');
    const data = await res.json();

    const tbody = document.querySelector('#tablaAlertas tbody');
    tbody.innerHTML = '';

    if (data.success && data.alertas.length > 0) {
      data.alertas.forEach(t => {
        const row = `
          <tr>
            <td>${t.nombre}</td>
            <td>${t.capacidad}</td>
            <td>${t.ocupadas}</td>
            <td style="color:red;">${t.ocupadas/t.capacidad}%</td>
          </tr>
        `;
        tbody.innerHTML += row;
      });
    } else {
      tbody.innerHTML = '<tr><td colspan="4">No hay terminales con baja disponibilidad.</td></tr>';
    }

  } catch (error) {
    console.error(error);
    alert("Error al obtener alertas.");
  }
});
