document.getElementById('registroForm').addEventListener('submit', async (e) => {
  e.preventDefault();

  const datos = {
    nombre: document.getElementById('nombre').value,
    correo: document.getElementById('correo').value,
    cui: document.getElementById('cui').value,
    telefono: document.getElementById('telefono').value,
    contrasena: document.getElementById('contrasena').value
  };

  try {
    const res = await fetch('http://localhost:5000/api/registro', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(datos)
    });

    const resultado = await res.json();
    alert(resultado.message);
    if (resultado.success) {
      window.location.href = 'login.html';
    }
  } catch (error) {
    alert("Error al registrar usuario.");
    console.error(error);
  }
});
