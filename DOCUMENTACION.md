# Documentación Técnica

## Descripción General

El Sistema de Acceso Universitario es una aplicación web desarrollada en Python utilizando Flask y SQLite. Permite gestionar el acceso de estudiantes y visitantes, así como la administración de materias y exportación de registros.

---

## Arquitectura

- **Backend:** Python (Flask)
- **Frontend:** HTML5, CSS3 (Bootstrap), Jinja2
- **Base de datos:** SQLite3

---

## Estructura de la Base de Datos

- **Admin:** id, username, password_hash
- **Estudiante:** id, nombre, dni, telefono, curso, salon, pin
- **Materia:** id, nombre, hora_inicio, hora_fin, estudiante_id
- **Visitante:** id, nombre, motivo, hora_entrada, hora_salida, tiempo_limite, unidad
- **Registro:** id, persona_id, nombre, rol, hora_entrada, hora_salida, activo

---

## Principales Rutas y Funcionalidades

| Ruta                              | Método   | Descripción                                      |
|------------------------------------|----------|--------------------------------------------------|
| `/`                               | GET      | Página de inicio                                 |
| `/login`                          | GET/POST | Autenticación de administrador                   |
| `/logout`                         | GET      | Cierre de sesión de administrador                |
| `/admin`                          | GET      | Panel de administración                          |
| `/admin/nuevo_estudiante`         | POST     | Registro de nuevo estudiante                     |
| `/admin/eliminar_estudiante/<id>` | POST     | Eliminación de estudiante                        |
| `/admin/exportar_csv`             | GET      | Exportación de historial en CSV                  |
| `/visitante`                      | GET/POST | Registro y control de visitantes                 |
| `/estudiante/login`               | GET/POST | Acceso de estudiante por PIN                     |
| `/estudiante/dashboard`           | GET      | Panel de materias del estudiante                 |
| `/estudiante/agregar_materia`     | POST     | Agregar materia al estudiante                    |
| `/estudiante/eliminar_materia/<id>` | POST   | Eliminar materia del estudiante                  |
| `/estudiante/logout`              | GET      | Cierre de sesión de estudiante                   |
| `/hardware`                       | GET      | Conexión con hardware externo                    |

---

## Plantillas HTML

Las vistas HTML se encuentran en la carpeta `templates/` y están organizadas de la siguiente manera:

- **base.html**: Plantilla base para herencia y estructura común.
- **index.html**: Página de inicio.
- **login.html**: Login de administrador.
- **admin_dashboard.html**: Panel principal del administrador.
- **dashboard.html**: Panel general de usuario.
- **estudiante_login.html**: Login de estudiante por PIN.
- **estudiante_dashboard.html**: Panel de materias del estudiante.
- **visitante.html**: Registro y control de visitantes.
- **hardware.html**: Interfaz para conexión con hardware externo.
- **terminal.html**: Terminal o consola web para administración (si aplica).

Cada plantilla utiliza Jinja2 para la renderización dinámica y Bootstrap para el diseño responsivo.

---

## Utilidades

- **utils/pin_utils.py:** Generación y validación de PINs aleatorios de 6 dígitos para estudiantes.

---

## Exportación de Datos

El historial de accesos puede exportarse en formato CSV desde el panel de administración, facilitando la gestión y análisis externo de los registros.

---

## Integración con Hardware

La sección `/hardware` permite la conexión con dispositivos Arduino/ESP32 mediante la Web Serial API. Esta funcionalidad está disponible únicamente en navegadores compatibles.

---

## Dependencias Principales

- Flask
- Flask-Login
- SQLite3
- Jinja2
- Bootstrap

Para el listado completo, consulta `requirements.txt`.

---

## Seguridad

- Contraseñas de administradores almacenadas con hash seguro.
- Validación de formularios y manejo de sesiones.
- Se recomienda utilizar HTTPS en producción.
