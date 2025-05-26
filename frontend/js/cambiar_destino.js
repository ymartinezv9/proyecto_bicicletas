document.addEventListener('DOMContentLoaded', async () => {
  const usuario = JSON.parse(localStorage.getItem("usuario"));
  if (!usuario) {
    alert("Inicia sesión.");
    window.location.href = "login.html";
    return;
  }

  const destinoActual = document.getElementById("destinoActual");
  const nuevaTerminalSelect = document.getElementById("nuevaTerminal");

  // Cargar terminales
  try {
    const resTerm = await fetch("http://localhost:5000/api/terminales");
    const terminales = await resTerm.json();

    terminales.forEach(t => {
      const option = document.createElement("option");
      option.value = t.id;
      option.textContent = t.nombre;
      nuevaTerminalSelect.appendChild(option);
    });
  } catch (error) {
    alert("Error al cargar terminales.");
    console.error(error);
  }

  // Obtener reserva activa (con destino actual)
  try {
    const res = await fetch(`http://localhost:5000/api/reservas/usuario/${usuario.id}`);
    const data = await res.json();

    if (data.success && data.reserva) {
      destinoActual.textContent = data.reserva.destino;
    } else {
      destinoActual.textContent = "No hay reserva activa.";
      document.getElementById("formDestino").style.display = "none";
    }
  } catch (error) {
    console.error("Error al obtener la reserva activa", error);
  }

  // Cambiar destino
  document.getElementById("formDestino").addEventListener("submit", async (e) => {
    e.preventDefault();

    const nueva_terminal_id = nuevaTerminalSelect.value;

    try {
      const res = await fetch("http://localhost:5000/api/reservas/cambiar-destino", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ usuario_id: usuario.id, nueva_terminal_id })
      });

      const resultado = await res.json();
      alert(resultado.message);

      if (resultado.success) {
        window.location.href = "dashboard.html";
      }
    } catch (error) {
      console.error("Error al cambiar destino", error);
    }
  });
});
