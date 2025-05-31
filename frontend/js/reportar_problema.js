document.addEventListener('DOMContentLoaded', async () => {
  const usuario = JSON.parse(localStorage.getItem('usuario'));
  if (!usuario) {
    alert("Inicia sesión.");
    window.location.href = 'login.html';
    return;
  }

  const selectBici = document.getElementById('bicicleta_id');
  const infoBicicleta = document.getElementById('infoBicicleta');
  let bicicletasMap = {};

  // Cargar bicicletas activas
  try {
    const res = await fetch('http://localhost:5000/api/bicicletas/activas');
    const bicicletas = await res.json();

    bicicletas.forEach(b => {
      bicicletasMap[b.id] = b;

      const opt = document.createElement('option');
      opt.value = b.id;
      opt.textContent = `${b.codigo}`;
      selectBici.appendChild(opt);
    });

    if (bicicletas.length === 0) {
      const opt = document.createElement('option');
      opt.disabled = true;
      opt.textContent = 'No hay bicicletas activas disponibles';
      selectBici.appendChild(opt);
    }

  } catch (error) {
    alert("Error al cargar bicicletas.");
    console.error(error);
  }

  // Mostrar info al seleccionar bicicleta
  selectBici.addEventListener('change', () => {
    const bici = bicicletasMap[selectBici.value];
    if (bici) {
      infoBicicleta.textContent = `Estado: ${bici.estado} | Ubicación: ${bici.terminal || 'Sin asignar'}`;
    } else {
      infoBicicleta.textContent = '';
    }
  });

  // Envío del formulario
  document.getElementById('formProblema').addEventListener('submit', async (e) => {
    e.preventDefault();

    const datos = {
      usuario_id: usuario.id,
      bicicleta_id: selectBici.value,
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
      alert("Error al reportar el problema.");
      console.error(error);
    }
  });
});
