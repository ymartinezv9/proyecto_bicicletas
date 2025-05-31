document.addEventListener('DOMContentLoaded', () => {
  const usuario = JSON.parse(localStorage.getItem('usuario'));
  if (!usuario) {
    alert("Inicia sesión.");
    window.location.href = 'login.html';
    return;
  }

  document.getElementById('formDanio').addEventListener('submit', async (e) => {
    e.preventDefault();

    const datos = {
      usuario_id: usuario.id,
      bicicleta_id: document.getElementById('bicicleta_id').value,
      tipo_problema: document.getElementById('tipo_problema').value,
      descripcion: document.getElementById('descripcion').value
    };

    try {
      const res = await fetch('http://localhost:5000/api/reportar-danio', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(datos)
      });

      const resultado = await res.json();
      alert(resultado.message);

      if (resultado.success) {
        window.location.href = 'dashboard.html';
      }

    } catch (error) {
      alert("Error al reportar.");
      console.error(error);
    }
  });
});
