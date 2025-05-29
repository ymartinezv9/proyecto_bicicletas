document.addEventListener("DOMContentLoaded", async () => {
  const usuario = JSON.parse(localStorage.getItem("usuario"));
  if (!usuario) {
    alert("Inicia sesión primero.");
    window.location.href = "login.html";
    return;
  }

  const climaTexto = document.getElementById("estadoClima");
  const listaRutas = document.getElementById("listaRutas");

  try {
    // Obtener clima real desde el backend
    const climaRes = await fetch("http://localhost:5000/api/clima");
    const clima = await climaRes.json();
    climaTexto.textContent = `${clima.temperatura}°C, ${clima.descripcion}`;

    // Estilo visual si el clima no es favorable
    if (clima.descripcion.toLowerCase().includes("lluvia")) {
      climaTexto.style.color = "blue";
      climaTexto.textContent += " — Lleva paraguas.";
    }

    // Inicializar el mapa
    const map = L.map("map").setView([14.6349, -90.5069], 13);
    L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
      attribution: "&copy; OpenStreetMap contributors"
    }).addTo(map);

    // Obtener rutas sugeridas desde el backend
    const rutasRes = await fetch("http://localhost:5000/api/rutas-sugeridas");
    const rutas = await rutasRes.json();

    listaRutas.innerHTML = "";

    if (rutas.length === 0) {
      listaRutas.innerHTML = "<li>No hay rutas recomendadas en este momento.</li>";
      return;
    }

    const terminalesMarcadas = new Set();

    rutas.forEach((r, i) => {
      const item = document.createElement("li");
      item.textContent = `Ruta ${i + 1}: De "${r.origen}" a "${r.destino}"`;
      listaRutas.appendChild(item);

      // Coordenadas reales
      const lat1 = parseFloat(r.lat_origen);
      const lon1 = parseFloat(r.lon_origen);
      const lat2 = parseFloat(r.lat_destino);
      const lon2 = parseFloat(r.lon_destino);

      const idOrigen = `${lat1.toFixed(6)},${lon1.toFixed(6)}`;
      const idDestino = `${lat2.toFixed(6)},${lon2.toFixed(6)}`;

      // Marcar solo una vez cada terminal
      if (!terminalesMarcadas.has(idOrigen)) {
        L.marker([lat1, lon1]).addTo(map).bindPopup(`Origen: ${r.origen}`);
        terminalesMarcadas.add(idOrigen);
      }

      if (!terminalesMarcadas.has(idDestino)) {
        L.marker([lat2, lon2]).addTo(map).bindPopup(`Destino: ${r.destino}`);
        terminalesMarcadas.add(idDestino);
      }

      // Línea entre terminales
      L.polyline([[lat1, lon1], [lat2, lon2]], { color: "blue" }).addTo(map);
    });

  } catch (error) {
    console.error(error);
    climaTexto.textContent = "Error al obtener el clima.";
    listaRutas.innerHTML = "<li>Error al cargar rutas.</li>";
  }
});
