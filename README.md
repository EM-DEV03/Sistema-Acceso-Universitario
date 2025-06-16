# Sistema de Acceso Universitario

Sistema web para la gestión de accesos de estudiantes y visitantes en una universidad, con registro de entradas/salidas, control de tiempo para visitantes y administración de estudiantes y materias.

## Características principales

- Registro y autenticación de administradores.
- Registro de estudiantes con generación automática de PIN.
- Panel de control para administración de estudiantes y visualización de registros.
- Acceso de estudiantes mediante PIN y gestión de materias.
- Registro de visitantes con control de tiempo de permanencia.
- Exportación de historial de accesos a CSV.
- Interfaz web moderna y responsiva.
- Integración básica para conexión de hardware (Arduino/ESP32) vía Web Serial API.

## Instalación rápida

1. Clona el repositorio y entra a la carpeta del proyecto.
2. Instala las dependencias:
   ```sh
   pip install -r requirements.txt
   ```
3. Inicializa la base de datos:
   ```sh
   python db_setup.py
   ```
4. Ejecuta la aplicación:
   ```sh
   python app.py
   ```
5. Accede a `http://localhost:5000` en tu navegador.

## Acceso administrador por defecto

- Usuario: `admin`
- Contraseña: `123` (puedes cambiarla en la base de datos)

## Más información

- [Documentación técnica](DOCUMENTACION.md)
- [Manual de usuario](MANUAL_USUARIO.md)