document.addEventListener("DOMContentLoaded", async () => {
  const usuario = JSON.parse(localStorage.getItem("usuario"));
  if (!usuario) {
    alert("Inicia sesión.");
    window.location.href = "login.html";
    return;
  }

  const origenSelect = document.getElementById("origen");
  const destinoSelect = document.getElementById("destino");
  const listaRutas = document.getElementById("listaRutas");
  const notificacionesCheckbox = document.getElementById("notificaciones");
  const btnGuardarRuta = document.querySelector('#formRuta button');

  // Función para prevenir selección igual
  function prevenirSeleccionIgual() {
    function validar() {
      if (origenSelect.value === destinoSelect.value && origenSelect.value !== '') {
        btnGuardarRuta.disabled = true;
        btnGuardarRuta.title = "La terminal de origen y destino no pueden ser iguales.";
      } else {
        btnGuardarRuta.disabled = false;
        btnGuardarRuta.title = "";
      }
    }

    origenSelect.addEventListener('change', validar);
    destinoSelect.addEventListener('change', validar);
  }

  // Cargar terminales
  try {
    const resTerm = await fetch("http://localhost:5000/api/terminales");
    const terminales = await resTerm.json();

    terminales.forEach(t => {
      const op1 = document.createElement("option");
      op1.value = t.id;
      op1.textContent = t.nombre;
      origenSelect.appendChild(op1);

      const op2 = document.createElement("option");
      op2.value = t.id;
      op2.textContent = t.nombre;
      destinoSelect.appendChild(op2);
    });

    prevenirSeleccionIgual(); // Activamos validación
  } catch (error) {
    console.error("Error al cargar terminales", error);
  }

  // Cargar preferencias existentes
  try {
    const res = await fetch(`http://localhost:5000/api/preferencias/${usuario.id}`);
    const data = await res.json();

    if (data.success) {
      notificacionesCheckbox.checked = data.data.notificaciones;

      listaRutas.innerHTML = "";
      data.data.rutas_favoritas.forEach(ruta => {
        const item = document.createElement("li");
        item.textContent = `${ruta.origen} ➝ ${ruta.destino}`;
        listaRutas.appendChild(item);
      });
    }
  } catch (error) {
    console.error("Error al obtener preferencias", error);
  }

  // Guardar notificaciones
  document.getElementById("btnGuardarNotificaciones").addEventListener("click", async () => {
    const activar = notificacionesCheckbox.checked;

    try {
      const res = await fetch("http://localhost:5000/api/preferencias/notificaciones", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ usuario_id: usuario.id, activar })
      });

      const resultado = await res.json();
      alert(resultado.message);
    } catch (error) {
      console.error("Error al guardar notificaciones", error);
    }
  });

  // Guardar nueva ruta
  document.getElementById("formRuta").addEventListener("submit", async (e) => {
    e.preventDefault();

    const datos = {
      usuario_id: usuario.id,
      origen_id: origenSelect.value,
      destino_id: destinoSelect.value
    };

    try {
      const res = await fetch("http://localhost:5000/api/preferencias/ruta", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(datos)
      });

      const resultado = await res.json();
      alert(resultado.message);
      window.location.reload(); // Recargar para mostrar la nueva ruta
    } catch (error) {
      console.error("Error al guardar ruta", error);
    }
  });
});
