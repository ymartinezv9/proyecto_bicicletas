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
    // Obtener clima real desde el backend (API OpenWeatherMap)
    const climaRes = await fetch("http://localhost:5000/api/clima");
    const clima = await climaRes.json();
    climaTexto.textContent = `${clima.temperatura}°C, ${clima.descripcion}`;

    // Cambiar color si clima es desfavorable
    if (clima.descripcion.toLowerCase().includes("lluvia")) {
      climaTexto.classList.add("mensaje-error");
      climaTexto.textContent += " — Se recomienda precaución.";
    }

    // Inicializar mapa
    const map = L.map('map').setView([14.6349, -90.5069], 13);
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      attribution: '&copy; OpenStreetMap contributors'
    }).addTo(map);

    // Obtener rutas recomendadas desde el backend
    const rutasRes = await fetch("http://localhost:5000/api/rutas-sugeridas");
    const rutas = await rutasRes.json();

    listaRutas.innerHTML = "";

    if (rutas.length === 0) {
      listaRutas.innerHTML = "<li>No hay rutas recomendadas en este momento.</li>";
    } else {
      rutas.forEach((r, i) => {
        const item = document.createElement("li");
        item.textContent = `Ruta ${i + 1}: De "${r.origen}" a "${r.destino}"`;
        listaRutas.appendChild(item);

        // Simulación de coordenadas (puedes reemplazar con las reales más adelante)
        const lat1 = 14.62 + Math.random() * 0.02;
        const lng1 = -90.52 + Math.random() * 0.02;
        const lat2 = 14.62 + Math.random() * 0.02;
        const lng2 = -90.52 + Math.random() * 0.02;

        // Marcadores
        const origenMarker = L.marker([lat1, lng1]).addTo(map).bindPopup(`Origen: ${r.origen}`);
        const destinoMarker = L.marker([lat2, lng2]).addTo(map).bindPopup(`Destino: ${r.destino}`);

        // Línea entre los dos puntos
        L.polyline([[lat1, lng1], [lat2, lng2]], { color: 'blue' }).addTo(map);
      });
    }

  } catch (error) {
    console.error(error);
    climaTexto.textContent = "No se pudo obtener el clima.";
    listaRutas.innerHTML = "<li>Error al cargar rutas sugeridas.</li>";
  }
});
