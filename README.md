# Sistema de Acceso Universitario

Este sistema web permite la gestión eficiente de accesos de estudiantes y visitantes en una institución universitaria. Incluye registro de entradas y salidas, control de tiempo para visitantes, administración de estudiantes y materias, y exportación de registros.

## Tabla de Contenidos

- [Características](#características)
- [Requisitos](#requisitos)
- [Instalación](#instalación)
- [Estructura del Proyecto](#estructura-del-proyecto)
- [Configuración Inicial](#configuración-inicial)
- [Acceso Inicial](#acceso-inicial)
- [Documentación y Manual de Usuario](#documentación-y-manual-de-usuario)
- [Licencia](#licencia)

## Características

- Gestión de usuarios administradores.
- Registro y control de estudiantes con PIN único.
- Panel de administración para gestión de estudiantes y visualización de registros.
- Acceso de estudiantes mediante PIN y gestión de materias.
- Registro y control de visitantes con límite de tiempo configurable.
- Exportación de historial de accesos en formato CSV.
- Interfaz web responsiva y moderna.
- Integración básica para conexión de hardware (Arduino/ESP32) vía Web Serial API.

## Requisitos

- Python 3.8 o superior
- pip
- Navegador web moderno (para Web Serial API, se recomienda Chrome)

## Instalación

1. Clona el repositorio:
   ```sh
   git clone https://github.com/tu_usuario/Sistema-Acceso-Universitario.git
   cd Sistema-Acceso-Universitario
   ```
2. Instala las dependencias:
   ```sh
   pip install -r requirements.txt
   ```
3. Ejecuta la aplicación:
   ```sh
   python app.py
   ```
4. Accede a `http://localhost:5000` en tu navegador.
5. Accede a la aplicación desde tu navegador en `http://localhost:5000`.

## Estructura del Proyecto

```
Sistema-Acceso-Universitario/
│
├── app.py
├── db_setup.py
├── requirements.txt
├── README.md
├── DOCUMENTACION.md
├── MANUAL_USUARIO.md
│
├── db/
│   └── acceso.db
│
├── static/
│   └── css/
│       └── styles.css
│
├── templates/
│   └── *.html
│
└── utils/
    └── pin_utils.py
```

## Configuración Inicial

- [Documentación técnica](DOCUMENTACION.md)
- [Manual de usuario](MANUAL_USUARIO.md)
- El usuario administrador por defecto es:
  - Usuario: `admin`
  - Contraseña: `123`
- Se recomienda cambiar la contraseña tras el primer inicio de sesión.

## Documentación y Manual de Usuario

- [Documentación Técnica](DOCUMENTACION.md)
- [Manual de Usuario](MANUAL_USUARIO.md)

## Licencia

Este proyecto se distribuye bajo la licencia MIT.
