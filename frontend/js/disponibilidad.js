document.addEventListener('DOMContentLoaded', async () => {
  const usuario = JSON.parse(localStorage.getItem('usuario'));
  if (!usuario) {
    alert("Inicia sesión para ver disponibilidad.");
    window.location.href = "login.html";
    return;
  }

  const tbody = document.querySelector("#tablaDisponibilidad tbody");

  try {
    const res = await fetch("http://localhost:5000/api/terminales");
    const terminales = await res.json();

    terminales.forEach(t => {
      const disponibles = t.ocupadas;
      const ocupacion = ((disponibles / t.capacidad) * 100).toFixed(1);
      
      
      const fila = document.createElement("tr");
      fila.innerHTML = `
        <td>${t.nombre}</td>
        <td>${disponibles}</td>
        <td>${t.capacidad}</td>
        <td>${ocupacion}%</td>
      `;
      tbody.appendChild(fila);
    });

  } catch (error) {
    alert("No se pudo cargar la disponibilidad.");
    console.error(error);
  }
});
