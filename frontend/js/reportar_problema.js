document.addEventListener("DOMContentLoaded", async () => {
  const usuario = JSON.parse(localStorage.getItem("usuario"));
  const form = document.getElementById("formReporte");

  if (!usuario) {
    alert("Inicia sesión para reportar problemas.");
    window.location.href = "login.html";
    return;
  }

  // Verificar si el usuario tiene una bicicleta activa
  try {
    const res = await fetch(`http://localhost:5000/api/reservas/usuario/${usuario.id}`);
    const data = await res.json();

    if (!data.success || !data.reserva) {
      alert("No tienes ninguna bicicleta activa para reportar.");
      form.style.display = "none";
      return;
    }
  } catch (error) {
    console.error("Error al verificar reserva activa", error);
    alert("Error al verificar estado de tu bicicleta.");
    form.style.display = "none";
    return;
  }

  // Enviar el reporte si sí tiene bicicleta activa
  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    const problema = document.getElementById("problema").value;

    try {
      const res = await fetch(`http://localhost:5000/api/reportar_problema`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          usuario_id: usuario.id,
          descripcion: problema
        })
      });

      const resultado = await res.json();
      alert(resultado.message);

      if (resultado.success) {
        window.location.href = "dashboard.html";
      }
    } catch (error) {
      console.error("Error al reportar problema", error);
      alert("Ocurrió un error al enviar el reporte.");
    }
  });
});
