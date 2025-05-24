document.addEventListener('DOMContentLoaded', async () => {
  const usuario = JSON.parse(localStorage.getItem('usuario'));
  if (!usuario) {
    alert("Inicia sesión para reservar.");
    window.location.href = 'login.html';
    return;
  }

  const origenSelect = document.getElementById('origen');
  const destinoSelect = document.getElementById('destino');

  try {
    const res = await fetch('http://localhost:5000/api/terminales');
    const terminales = await res.json();

    terminales.forEach(t => {
      const optionOrigen = document.createElement('option');
      optionOrigen.value = t.id;
      optionOrigen.textContent = t.nombre;
      origenSelect.appendChild(optionOrigen);

      const optionDestino = document.createElement('option');
      optionDestino.value = t.id;
      optionDestino.textContent = t.nombre;
      destinoSelect.appendChild(optionDestino);
    });

  } catch (error) {
    alert("No se pudieron cargar las terminales.");
    console.error(error);
  }

  document.getElementById('reservaForm').addEventListener('submit', async (e) => {
    e.preventDefault();

    const datos = {
      usuario_id: usuario.id,
      origen_id: origenSelect.value,
      destino_id: destinoSelect.value
    };

    try {
      const res = await fetch('http://localhost:5000/api/reservar', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(datos)
      });

      const resultado = await res.json();

      if (resultado.success) {
      alert(`Reserva exitosa.\nID Bicicleta: ${resultado.bicicleta_id}\nPIN de desbloqueo: ${resultado.pin}`);
      window.location.href = 'dashboard.html';
      } else {
        alert(resultado.message);
      }

    } catch (error) {
      alert("Error al hacer la reserva.");
      console.error(error);
    }
  });
});
