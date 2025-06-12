async function buscar() {
  const termino = document.getElementById('busqueda').value.trim();
  if (!termino) {
    alert("Ingresa un código o parte del código de bicicleta.");
    return;
  }

  try {
    const res = await fetch(`http://localhost:5000/api/bicicletas/historial/buscar/${encodeURIComponent(termino)}`);
    const data = await res.json();

    const tabla = document.getElementById('tablaHistorial');
    tabla.innerHTML = '';

    if (data.success && data.historial.length > 0) {
      data.historial.forEach(item => {
        const row = `
          <tr>
            <td>${item.bicicleta}</td>
            <td>${item.tipo}</td>
            <td>${item.descripcion}</td>
            <td>${item.estado}</td>
            <td>${item.usuario || 'Técnico'}</td>
            <td>${new Date(item.fecha).toLocaleString()}</td>
          </tr>
        `;
        tabla.innerHTML += row;
      });
    } else {
      tabla.innerHTML = `<tr><td colspan="6">No se encontraron registros.</td></tr>`;
    }

  } catch (error) {
    console.error("Error al buscar historial:", error);
    alert("Ocurrió un error al buscar.");
  }
}
