document.addEventListener("DOMContentLoaded", async () => {
  const usuario = JSON.parse(localStorage.getItem("usuario"));
  if (!usuario) {
    alert("Inicia sesión primero.");
    window.location.href = "login.html";
    return;
  }

  const terminalSelect = document.getElementById("terminal");
  const resultado = document.getElementById("resultadoEspacio");
  const form = document.getElementById("formEspacio");

  try {
    const res = await fetch("http://localhost:5000/api/terminales");
    const terminales = await res.json();

    terminales.forEach(t => {
      const option = document.createElement("option");
      option.value = t.id;
      option.textContent = t.nombre;
      terminalSelect.appendChild(option);
    });
  } catch (error) {
    alert("Error al cargar terminales.");
    console.error(error);
  }

  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    const terminalId = terminalSelect.value;

    try {
      const res = await fetch(`http://localhost:5000/api/terminal/${terminalId}/espacio`);
      const data = await res.json();

      resultado.textContent = data.message;
      resultado.style.color = data.success ? "green" : "red";
    } catch (error) {
      alert("No se pudo verificar el espacio.");
      console.error(error);
    }
  });
});
