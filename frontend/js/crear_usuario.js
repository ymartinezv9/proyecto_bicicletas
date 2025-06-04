document.addEventListener('DOMContentLoaded', () => {
  const usuario = JSON.parse(localStorage.getItem('usuario'));
  if (!usuario || usuario.tipo !== 'Administrador') {
    alert("Acceso denegado.");
    window.location.href = 'dashboard.html';
    return;
  }

  const form = document.getElementById('crearUsuarioForm');

  form.addEventListener('submit', async (e) => {
    e.preventDefault();

    const datos = {
      nombre: document.getElementById('nombre').value,
      correo: document.getElementById('correo').value,
      cui: document.getElementById('cui').value,
      telefono: document.getElementById('telefono').value,
      contrasena: document.getElementById('contrasena').value,
      tipo: document.getElementById('tipo').value,
      admin_token: "admin123"  // protección básica temporal
    };

    try {
      const res = await fetch('http://localhost:5000/api/admin/crear-usuario', {
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
      alert("Error al crear usuario.");
      console.error(error);
    }
  });
});
