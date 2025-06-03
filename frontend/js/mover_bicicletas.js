document.addEventListener('DOMContentLoaded', async () => {
  const usuario = JSON.parse(localStorage.getItem('usuario'));
  if (!usuario || (usuario.tipo !== 'Administrador' && usuario.tipo !== 'Soporte')) {
    alert("Acceso denegado.");
    window.location.href = 'login.html';
    return;
  }

  const selectBicicleta = document.getElementById('bicicleta');
  const selectTerminal = document.getElementById('terminal');

  // Cargar bicicletas
  const bicicletasRes = await fetch('http://localhost:5000/api/bicicletas/disponibles');
  const bicicletas = await bicicletasRes.json();
  bicicletas.bicicletas.forEach(b => {
    const option = document.createElement('option');
    option.value = b.id;
    option.textContent = `${b.codigo} (${b.terminal_origen})`;
    selectBicicleta.appendChild(option);
  });

  // Cargar terminales
  const terminalesRes = await fetch('http://localhost:5000/api/terminales');
  const terminales = await terminalesRes.json();
  terminales.forEach(t => {
    const option = document.createElement('option');
    option.value = t.id;
    option.textContent = t.nombre;
    selectTerminal.appendChild(option);
  });

  // Enviar redistribución
  document.getElementById('moverForm').addEventListener('submit', async (e) => {
    e.preventDefault();

    const datos = {
      bicicleta_id: selectBicicleta.value,
      terminal_id: selectTerminal.value
    };

    const res = await fetch('http://localhost:5000/api/bicicletas/mover', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(datos)
    });

    const resultado = await res.json();
    alert(resultado.message);
    if (resultado.success) {
      window.location.reload();
    }
  });
});
