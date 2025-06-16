# Documentación Técnica — Sistema de Acceso Universitario

## Estructura del proyecto

```
app.py
db_setup.py
requirements.txt
db/
    acceso.db
static/
    css/
        styles.css
templates/
    *.html
utils/
    pin_utils.py
```

## Base de datos

Tablas principales:

- **Estudiante**: id, nombre, dni, telefono, curso, salon, pin
- **Materia**: id, nombre, hora_inicio, hora_fin, estudiante_id
- **Visitante**: id, nombre, motivo, hora_entrada, hora_salida, tiempo_limite, unidad
- **Registro**: id, persona_id, nombre, rol, hora_entrada, hora_salida, activo
- **Admin**: id, username, password_hash

## Principales rutas y funcionalidades

- `/` — Inicio
- `/login` — Login administrador
- `/logout` — Logout administrador
- `/admin` — Panel administrador
- `/admin/nuevo_estudiante` — Registrar estudiante (POST)
- `/admin/eliminar_estudiante/<id>` — Eliminar estudiante (POST)
- `/admin/exportar_csv` — Descargar historial CSV
- `/visitante` — Registro y control de visitantes
- `/estudiante/login` — Login estudiante por PIN
- `/estudiante/dashboard` — Panel estudiante
- `/estudiante/agregar_materia` — Agregar materia (POST)
- `/estudiante/eliminar_materia/<id>` — Eliminar materia (POST)
- `/estudiante/logout` — Logout estudiante
- `/hardware` — Conexión hardware

## Utilidades

- `utils/pin_utils.py`: Generación de PIN aleatorio de 6 dígitos.

## Plantillas

Las vistas HTML están en la carpeta `templates/`, usando Jinja2 y Bootstrap.

## Exportación de datos

El historial de accesos puede exportarse a CSV desde el panel de administrador.

## Integración con hardware

La sección `/hardware` permite conectar dispositivos Arduino/ESP32 mediante la Web Serial API (solo navegadores compatibles).

## Dependencias principales

- Flask
- SQLite3
- Jinja2
- Bootstrap

Consulta `requirements.txt` para el listado completo.