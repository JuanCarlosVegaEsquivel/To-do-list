// La URL base de tu API
const API_URL = "http://127.0.0.1:8000/tareas";

const input = document.getElementById("input-tarea");
const boton = document.getElementById("btn-agregar");
const lista = document.getElementById("lista-tareas");

// Dibuja UNA tarea en la pantalla (crea el <li> + botón de borrar + botón de completar)
function dibujarTarea(tarea) {
  const item = document.createElement("li");
  item.textContent = tarea.titulo;

  // Si la tarea ya está completada, la tachamos visualmente
  if (tarea.completada) {
    item.style.textDecoration = "line-through";
  }

  // Botón para marcar como completada/pendiente
  const botonCompletar = document.createElement("button");
  botonCompletar.textContent = "✓";
  botonCompletar.addEventListener("click", async function () {
    await fetch(`${API_URL}/${tarea.id}`, { method: "PUT" });
    cargarTareas(); // recarga la lista para reflejar el cambio
  });

  // Botón para borrar
  const botonBorrar = document.createElement("button");
  botonBorrar.textContent = "Borrar";
  botonBorrar.classList.add("btn-borrar");
  botonBorrar.addEventListener("click", async function () {
    await fetch(`${API_URL}/${tarea.id}`, { method: "DELETE" });
    cargarTareas(); // recarga la lista para reflejar el cambio
  });

  item.appendChild(botonCompletar);
  item.appendChild(botonBorrar);
  lista.appendChild(item);
}

// Pide todas las tareas a la API y las dibuja en pantalla
async function cargarTareas() {
  const respuesta = await fetch(API_URL);
  const tareas = await respuesta.json();

  lista.innerHTML = ""; // limpia la lista antes de redibujar

  tareas.forEach(function (tarea) {
    dibujarTarea(tarea);
  });
}

// Cuando le dan click a "Agregar"
boton.addEventListener("click", async function () {
  const texto = input.value;

  if (texto === "") {
    return;
  }

  await fetch(API_URL, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ titulo: texto }),
  });

  input.value = "";
  cargarTareas(); // recarga la lista para mostrar la tarea nueva
});

// Al abrir la página, cargamos las tareas que ya existan
cargarTareas();
