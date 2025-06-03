document.addEventListener('DOMContentLoaded', () => {
  const usuario = JSON.parse(localStorage.getItem('usuario'));
  if (!usuario) {
    alert("Debes iniciar sesión para contactar soporte.");
    window.location.href = 'login.html';
    return;
  }

  const form = document.getElementById('soporteForm');
  form.addEventListener('submit', async (e) => {
    e.preventDefault();

    const datos = {
      usuario_id: usuario.id,
      asunto: document.getElementById('asunto').value,
      mensaje: document.getElementById('mensaje').value
    };

    try {
      const res = await fetch('http://localhost:5000/api/soporte/mensaje', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(datos)
      });

      const resultado = await res.json();
      alert(resultado.message);
      if (resultado.success) {
        form.reset();
      }
    } catch (error) {
      console.error(error);
      alert("Ocurrió un error al enviar el mensaje.");
    }
  });
});
