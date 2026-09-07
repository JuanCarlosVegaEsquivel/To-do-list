# To-Do List — Full Stack

Aplicación de lista de tareas construida como proyecto de aprendizaje, usando HTML, CSS y JavaScript en el frontend, y FastAPI + MySQL en el backend.

## Tecnologías usadas

- **Frontend:** HTML, CSS, JavaScript (vanilla)
- **Backend:** Python + FastAPI
- **Base de datos:** MySQL
- **ORM:** SQLAlchemy

## Funcionalidades

- Crear tareas nuevas
- Marcar tareas como completadas / pendientes
- Borrar tareas
- Las tareas persisten en una base de datos MySQL (no se pierden al recargar la página)

## Requisitos previos

Antes de correr el proyecto, asegurate de tener instalado:

- [Python 3.11+](https://www.python.org/downloads/)
- [MySQL](https://dev.mysql.com/downloads/) (o MySQL Workbench)
- Un navegador con la extensión [Live Server](https://marketplace.visualstudio.com/items?itemName=ritwickdey.LiveServer) en VS Code (o cualquier servidor local para archivos estáticos)

## Instalación

### 1. Clonar el repositorio

```bash
git clone https://github.com/JuanCarlosVegaEsquivel/To-do-list.git
cd To-do-list
```

### 2. Configurar la base de datos

Abrí MySQL Workbench (o tu cliente de MySQL) y corré:

```sql
CREATE DATABASE todo_list;

USE todo_list;

CREATE TABLE tareas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    titulo VARCHAR(255) NOT NULL,
    completada BOOLEAN DEFAULT FALSE
);
```

### 3. Configurar el backend

```bash
cd backend
pip install fastapi uvicorn sqlalchemy pymysql
```

Abrí `backend/main.py` y actualizá la línea de `DATABASE_URL` con tu usuario y contraseña de MySQL:

```python
DATABASE_URL = "mysql+pymysql://TU_USUARIO:TU_CONTRASEÑA@localhost/todo_list"
```

## Cómo correr el proyecto

Necesitás tener **dos cosas corriendo al mismo tiempo**: el backend y el frontend.

### 1. Iniciar el backend

En una terminal, dentro de la carpeta `backend`:

```bash
cd backend
python -m uvicorn main:app --reload
```

Vas a saber que arrancó bien cuando veas:
```
INFO:     Application startup complete.
```

El backend queda corriendo en `http://127.0.0.1:8000`. Podés probar las rutas de la API en `http://127.0.0.1:8000/docs`.

### 2. Iniciar el frontend

Con el backend ya corriendo, abrí `frontend/index.html` en VS Code y hacé click derecho → **"Open with Live Server"**.

Esto abre el navegador automáticamente (normalmente en `http://127.0.0.1:5500`), y ahí ya podés usar la app.

## Notas

- MySQL debe estar corriendo en segundo plano en tu compu (normalmente arranca solo como servicio de Windows).
- Recordá prender primero el backend y después el frontend.
- Este proyecto usa CORS abierto (`allow_origins=["*"]`) porque es un proyecto local de aprendizaje. En un proyecto en producción, se debería restringir a un origen específico.

## Próximos pasos / ideas a futuro

- [ ] Migrar el frontend a React
- [ ] Agregar validaciones (evitar tareas vacías, límite de caracteres)
- [ ] Agregar categorías o fechas límite a las tareas
- [ ] Mover la contraseña de la base de datos a variables de entorno (`.env`)
