document.addEventListener('DOMContentLoaded', async () => {
  const usuario = JSON.parse(localStorage.getItem('usuario'));
  if (!usuario || usuario.tipo !== 'Administrador') {
    alert("Acceso denegado.");
    window.location.href = 'login.html';
    return;
  }

  const tabla = document.getElementById('tablaUsuarios');

  try {
    const res = await fetch('http://localhost:5000/api/usuarios');
    const data = await res.json();

    if (data.success) {
      data.usuarios.forEach(u => {
        const row = document.createElement('tr');
        row.innerHTML = `
          <td>${u.nombre}</td>
          <td>${u.correo}</td>
          <td>${u.tipo}</td>
          <td>${u.estado}</td>
          <td>
            <button onclick="cambiarEstado(${u.id}, '${u.estado === 'Activo' ? 'Bloqueado' : 'Activo'}')">
              ${u.estado === 'Activo' ? 'Suspender' : 'Activar'}
            </button>
          </td>
        `;
        tabla.appendChild(row);
      });
    }
  } catch (error) {
    console.error("Error al cargar usuarios", error);
  }
});

async function cambiarEstado(id, nuevoEstado) {
  if (!confirm(`¿Estás seguro de cambiar el estado a ${nuevoEstado}?`)) return;

  try {
    const res = await fetch('http://localhost:5000/api/usuarios/estado', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ usuario_id: id, estado: nuevoEstado })
    });

    const result = await res.json();
    alert(result.message);
    location.reload();
  } catch (error) {
    console.error("Error al cambiar estado", error);
  }
}

