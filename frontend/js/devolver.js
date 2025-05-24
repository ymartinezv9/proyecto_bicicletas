document.addEventListener('DOMContentLoaded', () => {
  const usuario = JSON.parse(localStorage.getItem('usuario'));
  if (!usuario) {
    alert("No has iniciado sesión.");
    window.location.href = 'login.html';
    return;
  }

  document.getElementById('btnDevolver').addEventListener('click', async () => {
    try {
      const res = await fetch('http://localhost:5000/api/devolver', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ usuario_id: usuario.id })
      });

      const resultado = await res.json();
      alert(resultado.message);

      if (resultado.success) {
        window.location.href = 'dashboard.html';
      }

    } catch (error) {
      alert("Error al procesar la devolución.");
      console.error(error);
    }
  });
});
