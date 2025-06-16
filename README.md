# Sistema de Acceso Universitario

Sistema web para la gestión y control de accesos de estudiantes y visitantes en una institución universitaria. Permite registrar entradas y salidas, controlar el tiempo de permanencia de visitantes, administrar estudiantes y materias, y exportar registros para su análisis.

---

## Tabla de Contenidos

- [Características](#características)
- [Requisitos](#requisitos)
- [Instalación](#instalación)
- [Estructura del Proyecto](#estructura-del-proyecto)
- [Configuración Inicial](#configuración-inicial)
- [Acceso Inicial](#acceso-inicial)
- [Documentación y Manual de Usuario](#documentación-y-manual-de-usuario)
- [Licencia](#licencia)

---

## Características

- Gestión de usuarios administradores.
- Registro y control de estudiantes con PIN único.
- Panel de administración para gestión de estudiantes y visualización de registros.
- Acceso de estudiantes mediante PIN y gestión de materias.
- Registro y control de visitantes con límite de tiempo configurable.
- Exportación de historial de accesos en formato CSV.
- Interfaz web responsiva y moderna.
- Integración básica para conexión de hardware (Arduino/ESP32) vía Web Serial API.

---

## Requisitos

- Python 3.8 o superior
- pip
- Navegador web moderno (para Web Serial API, se recomienda Chrome)

---

## Instalación

1. Clona el repositorio:
   ```sh
   git clone https://github.com/EM-DEV03/Sistema-Acceso-Universitario.git
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
4. Accede a la aplicación desde tu navegador en `http://localhost:5000`.

---

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
│   ├── admin_dashboard.html
│   ├── base.html
│   ├── dashboard.html
│   ├── estudiante_dashboard.html
│   ├── estudiante_login.html
│   ├── hardware.html
│   ├── index.html
│   ├── login.html
│   ├── terminal.html
│   └── visitante.html
│
└── utils/
    └── pin_utils.py
```

---

## Configuración Inicial

- El usuario administrador por defecto es:
  - Usuario: `admin`
  - Contraseña: `admin123`

---

## Documentación y Manual de Usuario

- [Documentación Técnica](DOCUMENTACION.md)
- [Manual de Usuario](MANUAL_USUARIO.md)

---


## Desarrollado por: 

$$$$$$$$\ $$\      $$\        $$$$$$$\  $$$$$$$$\ $$\    $$\ 
$$  _____|$$$\    $$$ |       $$  __$$\ $$  _____|$$ |   $$ |
$$ |      $$$$\  $$$$ |       $$ |  $$ |$$ |      $$ |   $$ |
$$$$$\    $$\$$\$$ $$ |       $$ |  $$ |$$$$$\    \$$\  $$  |
$$  __|   $$ \$$$  $$ |       $$ |  $$ |$$  __|    \$$\$$  / 
$$ |      $$ |\$  /$$ |       $$ |  $$ |$$ |        \$$$  /  
$$$$$$$$\ $$ | \_/ $$ |       $$$$$$$  |$$$$$$$$\    \$  /   
\________|\__|     \__|$$$$$$\\_______/ \________|    \_/    
                       \______|                              
                                                             
                                                             
