ProLink - Sistema de Gestión de Ofertas Laborales
Aplicación web desarrollada con Flask para la gestión integrada de ofertas de empleo, candidatos, empresas y postulaciones.
📋 Requisitos Previos
Python 3.8 o superior
pip (gestor de paquetes de Python)
SQLite (incluido con Python)
🚀 Instalación y Configuración
1. Clonar o descargar el proyecto
```bash
cd Proyecto-NTD-Final
```
2. Crear un entorno virtual (recomendado)
En Windows:
```bash
python -m venv venv
venv\Scripts\activate
```
En macOS/Linux:
```bash
python3 -m venv venv
source venv/bin/activate
```
3. Instalar las dependencias
```bash
pip install -r requirements.txt
```
4. Configurar variables de entorno
Crear un archivo `.env` en la raíz del proyecto:
```env
# Base de datos
SQLITE_DATABASE=ProLink.db


# Flask
SECRET_KEY=tu_clave_secreta_super_segura_aqui
FLASK_ENV=development
FLASK_DEBUG=True

# API Configuration
API_HOST=0.0.0.0
API_PORT=5000
```
Nota: Reemplaza `SECRET_KEY` con una clave segura y única para tu aplicación.
5. Inicializar la base de datos
Si necesitas crear las tablas iniciales:
```bash
python Cross/init_db.py
<img width="457" height="99" alt="image" src="https://github.com/user-attachments/assets/fe931d48-65c3-47c2-8136-de78bbca4908" />
```
▶️ Ejecutar la Aplicación
Desde el directorio raíz del proyecto con el entorno virtual activado:
```bash
python entry/run.py
<img width="1281" height="326" alt="image" src="https://github.com/user-attachments/assets/841f30ca-8a76-4250-b45d-c448b5fedd08" />
<img width="1911" height="915" alt="image" src="https://github.com/user-attachments/assets/08694ca0-e162-406c-932a-54182b95e061" />

```
La aplicación se iniciará en: `http://localhost:5000`
El navegador se abrirá automáticamente. Si no ocurre, accede manualmente a la URL anterior.
📁 Estructura del Proyecto
```
Proyecto-NTD-Final/
├── entry/
│   └── run.py                 # Punto de entrada de la aplicación
├── Routes/                    # Rutas/endpoints de la API
│   ├── auth_routes.py
│   ├── usuario_routes.py
│   ├── empresas_routes.py
│   ├── candidato_routes.py
│   ├── ofertas_routes.py
│   ├── postulaciones_routes.py
│   ├── delegado_routes.py
│   └── chat_routes.py
├── Services/                  # Lógica de negocio
│   ├── auth_service.py
│   ├── usuario_service.py
│   ├── empresa_service.py
│   ├── candidato_service.py
│   ├── oferta_service.py
│   ├── postulaciones_service.py
│   ├── delegado_service.py
│   └── chat_service.py
├── Repositories/              # Acceso a datos
│   ├── usuario_repo.py
│   ├── empresa_repo.py
│   ├── candidato_repo.py
│   ├── ofertas_repo.py
│   ├── postulacione_repo.py
│   ├── delegado_repo.py
│   └── chat_repositorio.py
├── Database/                  # Configuración de BD
│   ├── config.py
│   └── mongo_db.py
├── Cross/                     # Utilidades y middleware
│   ├── jwt_middleware.py      # Autenticación JWT
│   └── init_db.py            # Inicialización de BD
├── static/                    # Archivos estáticos (CSS, JS)
├── templates/                 # Plantillas HTML
├── requirements.txt           # Dependencias del proyecto
└── .env                       # Variables de entorno (crear)
```
🔐 Autenticación
La aplicación utiliza JWT (JSON Web Tokens) para la autenticación.
Tipos de usuarios soportados:
Delegado - Gestiona ofertas de empresas
Empresa - Publica y gestiona ofertas
Candidato - Busca y se postula a ofertas
Usuario - Tipo genérico
📚 API Endpoints Principales
Autenticación
`POST /login` - Iniciar sesión
`POST /usuario/crear` - Registrar nuevo usuario
Usuarios
`GET /usuario/<id>` - Obtener perfil
`PUT /usuario/<id>` - Actualizar perfil
Ofertas
`GET /ofertas` - Listar todas las ofertas
`GET /oferta/<id>` - Obtener detalle de oferta
`POST /oferta/crear` - Crear nueva oferta
`PUT /oferta/<id>` - Actualizar oferta
Postulaciones
`GET /postulaciones` - Listar postulaciones
`POST /postulacion/crear` - Crear postulación
`PUT /postulacion/<id>` - Actualizar estado de postulación
Para más ejemplos de uso, consulta API_EJEMPLOS.md
🛠️ Desarrollo
Modo Debug
El modo debug está habilitado por defecto. Para deshabilitarlo, cambia en `.env`:
```env
FLASK_DEBUG=False
```
Agregar nuevas rutas
Crear archivo en `Routes/`
Registrar el blueprint en `entry/run.py`
Crear nuevos servicios
Crear archivo en `Services/`
Implementar la lógica de negocio
🐛 Solución de Problemas
Error: "No module named 'flask'"
Asegúrate de que el entorno virtual esté activado y ejecuta:
```bash
pip install -r requirements.txt
```
Error: "ProLink.db not found"
Ejecuta:
```bash
python Cross/init_db.py
```
Error: "Secret key not set"
Verifica que el archivo `.env` existe y contiene `SECRET_KEY`
Puerto 5000 en uso
Cambia el puerto en `.env`:
```env
API_PORT=5001
```
📦 Dependencias
Flask - Framework web
flask-cors - Soporte CORS
PyJWT - Autenticación JWT
python-dotenv - Gestión de variables de entorno
pymongo - Driver de MongoDB (si aplica)
bcrypt - Hashing de contraseñas
Consulta requirements.txt para la lista completa.
📝 Licencia
Este proyecto es privado y está en desarrollo.
👥 Contribuciones
Para reportar problemas o sugerencias, contacta al equipo de desarrollo.
---
Última actualización: Mayo 2026
