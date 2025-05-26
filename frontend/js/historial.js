document.addEventListener('DOMContentLoaded', async () => {
  const usuario = JSON.parse(localStorage.getItem('usuario'));
  if (!usuario) {
    alert("No has iniciado sesión.");
    window.location.href = 'login.html';
    return;
  }

  try {
    const res = await fetch(`http://localhost:5000/api/historial/${usuario.id}`);
    const resultado = await res.json();

    const tbody = document.querySelector("#tablaHistorial tbody");
    tbody.innerHTML = "";

    if (resultado.success) {
      resultado.historial.forEach((r) => {
        const row = document.createElement("tr");
        row.innerHTML = `
          <td>${r.id}</td>
          <td>${r.bicicleta}</td>
          <td>${r.terminal_origen}</td>
          <td>${r.terminal_destino}</td>
          <td>${r.hora_inicio ? new Date(r.hora_inicio).toLocaleString() : "-"}</td>
          <td>${r.hora_fin ? new Date(r.hora_fin).toLocaleString() : "-"}</td>
          <td>${r.estado}</td>
        `;
        tbody.appendChild(row);
      });
    } else {
      alert(resultado.message);
    }
  } catch (error) {
    alert("Error al obtener el historial.");
    console.error(error);
  }
});
