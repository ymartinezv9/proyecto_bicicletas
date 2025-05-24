document.addEventListener('DOMContentLoaded', () => {
  const usuario = JSON.parse(localStorage.getItem('usuario'));
  if (!usuario) {
    alert("No has iniciado sesión.");
    window.location.href = 'login.html';
    return;
  }

  document.getElementById('pinForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    const pin = document.getElementById('pin').value;

    try {
      const res = await fetch('http://localhost:5000/api/desbloquear', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          usuario_id: usuario.id,
          pin: pin
        })
      });

      const resultado = await res.json();
      alert(resultado.message);

      if (resultado.success) {
        window.location.href = 'dashboard.html';
      }

    } catch (error) {
      alert("Error al verificar el PIN.");
      console.error(error);
    }
  });
});
