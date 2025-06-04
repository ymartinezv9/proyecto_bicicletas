document.addEventListener('DOMContentLoaded', async () => {
  const usuario = JSON.parse(localStorage.getItem('usuario'));
  if (!usuario || usuario.tipo !== 'Administrador') {
    alert("Acceso no autorizado.");
    window.location.href = 'login.html';
    return;
  }

  const tablaBody = document.querySelector('#tablabicicleta tbody');

  try {
    const res = await fetch('http://localhost:5000/api/bicicletas/estado');
    const datos = await res.json();


if (datos.success && datos.bicicletas.length > 0) {
  datos.bicicletas.forEach(b => {

    const row = `
      <tr>

        <td>${b.id}</td>
        <td>${b.codigo}</td>
        <td>${b.estado}</td>
        <td>${b.terminal || 'Sin asignar'}</td>
      </tr>
    `;
    document.querySelector('#tablaBicicletas tbody').innerHTML += row;
  });
} else {
  document.querySelector('#tablaBicicletas tbody').innerHTML = `
    <tr><td colspan="3">No hay bicicletas para mostrar.</td></tr>
  `;
}


  } catch (error) {
    console.error('Error al cargar el estado de las bicicletas:', error);
    alert('No se pudo cargar el estado de las bicicletas. Inténtalo más tarde.');
  }
});
