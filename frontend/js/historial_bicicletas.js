async function cargarHistorial() {
  const id = document.getElementById('bicicletaId').value;
  if (!id) return alert("Ingresa un ID de bicicleta");

  const res = await fetch(`http://localhost:5000/api/bicicletas/historial/${id}`);
  const data = await res.json();

  const tabla = document.getElementById('tablaHistorial');
  tabla.innerHTML = '';

  if (data.success && data.historial.length > 0) {
    data.historial.forEach(item => {
      const row = `
        <tr>
          <td>${new Date(item.fecha).toLocaleString()}</td>
          <td>${item.tipo}</td>
          <td>${item.descripcion}</td>
          <td>${item.estado}</td>
          <td>${item.usuario || 'Técnico'}</td>
        </tr>
      `;
      tabla.innerHTML += row;
    });
  } else {
    tabla.innerHTML = `<tr><td colspan="5">No hay historial.</td></tr>`;
  }
}
