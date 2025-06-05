document.addEventListener('DOMContentLoaded', async () => {
  const usuario = JSON.parse(localStorage.getItem('usuario'));
  if (!usuario || usuario.tipo !== 'Tecnico') {
    alert("Acceso denegado.");
    window.location.href = 'login.html';
    return;
  }

  try {
    const res = await fetch('http://localhost:5000/api/bicicletas/estado');
    const data = await res.json();

    const tabla = document.getElementById('tablaDisponibles');
    tabla.innerHTML = '';

    if (data.success && data.bicicletas.length > 0) {
      data.bicicletas
        .filter(b => b.estado === 'Disponible')
        .forEach(b => {
          const row = document.createElement('tr');
          row.innerHTML = `
            <td>${b.codigo}</td>
            <td>${b.estado}</td>
            <td>${b.terminal || 'Sin asignar'}</td>
            <td>
              <button onclick="marcarMantenimiento(${b.id})">Enviar a mantenimiento</button>
            </td>
          `;
          tabla.appendChild(row);
        });
    } else {
      tabla.innerHTML = '<tr><td colspan="4">No hay bicicletas disponibles.</td></tr>';
    }

  } catch (error) {
    console.error("Error al cargar bicicletas:", error);
  }
});

async function marcarMantenimiento(id) {
  if (!confirm("¿Enviar esta bicicleta a mantenimiento preventivo?")) return;

  try {
    const res = await fetch('http://localhost:5000/api/bicicletas/estado', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ bicicleta_id: id, estado: 'Mantenimiento' })
    });

    const result = await res.json();
    alert(result.message);
    location.reload();
  } catch (error) {
    console.error("Error al cambiar estado", error);
  }
}
