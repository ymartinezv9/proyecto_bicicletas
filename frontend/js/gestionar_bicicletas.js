document.addEventListener('DOMContentLoaded', async () => {
  const usuario = JSON.parse(localStorage.getItem('usuario'));
  if (!usuario || usuario.tipo !== 'Tecnico') {
    alert("Acceso denegado.");
    window.location.href = 'login.html';
    return;
  }

  try {
    const res = await fetch('http://localhost:5000/api/bicicletas/mantenimiento');
    const data = await res.json();

    const tabla = document.getElementById('tablaMantenimiento');
    tabla.innerHTML = '';

    if (data.success && data.bicicletas.length > 0) {
      data.bicicletas.forEach(b => {
        const row = document.createElement('tr');
        row.innerHTML = `
          <td>${b.codigo}</td>
          <td>${b.estado}</td>
          <td>${b.terminal || 'Sin asignar'}</td>
          <td>
            <button onclick="cambiarEstado(${b.id}, 'Disponible')">Habilitar</button>
            <button onclick="cambiarEstado(${b.id}, 'Mantenimiento')">Mantener</button>
          </td>
        `;
        tabla.appendChild(row);
      });
    } else {
      tabla.innerHTML = '<tr><td colspan="4">No hay bicicletas en mantenimiento.</td></tr>';
    }

  } catch (error) {
    console.error("Error al cargar bicicletas:", error);
  }
});

async function cambiarEstado(id, estado) {
  try {
    const res = await fetch('http://localhost:5000/api/bicicletas/estado', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ bicicleta_id: id, estado })
    });

    const result = await res.json();
    alert(result.message);
    location.reload();
  } catch (error) {
    console.error("Error al cambiar estado:", error);
  }
}
