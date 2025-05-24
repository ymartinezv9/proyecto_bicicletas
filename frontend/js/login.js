document.getElementById('loginForm').addEventListener('submit', async (e) => {
  e.preventDefault();

  const datos = {
    correo: document.getElementById('correo').value,
    contrasena: document.getElementById('contrasena').value
  };

  try {
    const res = await fetch('http://localhost:5000/api/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(datos)
    });

    const resultado = await res.json();
    alert(resultado.message);

    if (resultado.success) {
      // Guardar datos en localStorage o redirigir
      window.location.href = 'dashboard.html';
    }

  if (resultado.success) {
    localStorage.setItem('usuario', JSON.stringify(resultado.usuario));
    window.location.href = 'dashboard.html';
  }
  
  } catch (error) {
    alert("Error al iniciar sesión.");
    console.error(error);
  }
});


