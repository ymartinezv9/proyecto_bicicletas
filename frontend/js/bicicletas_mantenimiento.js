document.addEventListener('DOMContentLoaded', async () => {
  const usuario = JSON.parse(localStorage.getItem('usuario'));
  if (!usuario || usuario.tipo !== 'Tecnico') {
    alert("Acceso denegado.");
    window.location.href = 'dashboard.html';
    return;
  }

  try {
    const res = await fetch(`http://localhost:5000/api/bicicletas/mantenimiento/${usuario.id}`);
    const data = await res.json();

    const tbody = document.querySelector('#tablaMantenimiento tbody');
    tbody.innerHTML = '';

    if (data.success && data.bicicletas.length > 0) {
      data.bicicletas.forEach(b => {
        const row = `
          <tr>
            <td>${b.id}</td>
            <td>${b.codigo}</td>
            <td>${b.terminal_id ?? 'Sin terminal'}</td>
            <td>${b.estado}</td>
          </tr>
        `;
        tbody.innerHTML += row;
      });
    } else {
      tbody.innerHTML = '<tr><td colspan="4">No hay bicicletas en mantenimiento.</td></tr>';
    }

  } catch (error) {
    console.error(error);
    alert("Error al cargar bicicletas.");
  }
});
