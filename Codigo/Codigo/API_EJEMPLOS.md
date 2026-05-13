# Ejemplos de Uso de la API ProLink

## 1. Autenticación

### Login
```bash
POST /login
Content-Type: application/json

{
  "correo": "usuario@email.com",
  "password": "contraseña123"
}

Response 200:
{
  "message": "Login exitoso",
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "id": 1,
  "nombre": "Juan Pérez",
  "tipoUsuario": "delegado"
}

Response 404:
{
  "error": "Correo no encontrado"
}

Response 401:
{
  "error": "Contraseña incorrecta"
}
```

---

## 2. Gestión de Usuarios

### Crear Usuario
```bash
POST /usuario/crear
Content-Type: application/json

{
  "nombre": "Juan Pérez",
  "correo": "juan@email.com",
  "numero": "1234567890",
  "tipoUsuario": "delegado",
  "password": "contraseña123"
}

Response 201:
{
  "Id": 1,
  "nombre": "Juan Pérez",
  "correo": "juan@email.com",
  "numero": "1234567890",
  "tipoUsuario": "delegado"
}

Response 400:
{
  "error": "Datos incompletos"
}
o
{
  "error": "El correo ya está registrado"
}
```

### Obtener Usuario
```bash
GET /usuario/1
Cookie: jwt_token=<token>

Response 200:
{
  "Id": 1,
  "nombre": "Juan Pérez",
  "correo": "juan@email.com",
  "numero": "1234567890",
  "tipoUsuario": "delegado"
}

Response 404:
{
  "error": "Usuario no encontrado"
}

Response 401:
{
  "error": "Token no válido o expirado"
}
```

### Actualizar Usuario
```bash
PUT /actualizar-usuario/1
Cookie: jwt_token=<token>
Content-Type: application/json

{
  "nombre": "Juan Carlos Pérez",
  "correo": "juancarlos@email.com",
  "numero": "9876543210",
  "tipoUsuario": "delegado",
  "password": "nuevacontraseña123"
}

Response 200:
{
  "Id": 1,
  "nombre": "Juan Carlos Pérez",
  "correo": "juancarlos@email.com",
  "numero": "9876543210",
  "tipoUsuario": "delegado"
}
```

### Actualizar Contraseña
```bash
PUT /actualizar-contrasena/1
Cookie: jwt_token=<token>
Content-Type: application/json

{
  "password": "nuevacontraseña456"
}

Response 200:
{
  "Id": 1,
  "nombre": "Juan Pérez",
  "correo": "juan@email.com",
  "numero": "1234567890",
  "tipoUsuario": "delegado"
}
```

### Eliminar Usuario
```bash
DELETE /borrar-usuario/1
Cookie: jwt_token=<token>

Response 200:
{
  "Id": 1,
  "nombre": "Juan Pérez",
  "correo": "juan@email.com",
  "numero": "1234567890",
  "tipoUsuario": "delegado"
}

Response 404:
{
  "error": "Usuario no encontrado"
}
```

---

## 3. Gestión de Chats

### Ver todos los chats del usuario
```bash
GET /chats/1
Cookie: jwt_token=<token>

Response 200:
[
  {
    "id_chat": "507f1f77bcf86cd799439011",
    "delegado": "Juan Pérez",
    "candidato": "Carlos López",
    "fecha": "2024-05-01T14:30:00"
  },
  {
    "id_chat": "507f1f77bcf86cd799439012",
    "delegado": "Juan Pérez",
    "candidato": "Ana García",
    "fecha": "2024-05-01T10:15:00"
  }
]

Response 404:
{
  "error": "El usuario no tiene chats"
}
```

### Obtener un chat específico
```bash
GET /chats/1/507f1f77bcf86cd799439011
Cookie: jwt_token=<token>

Response 200:
{
  "Candidato": "Carlos López",
  "Delegado": "Juan Pérez",
  "Mensajes": [
    {
      "Enviado por": "Carlos López",
      "Fecha": "2024-05-01T14:30:00",
      "Contenido": "Hola, ¿cuál es el salario?"
    },
    {
      "Enviado por": "Juan Pérez",
      "Fecha": "2024-05-01T14:35:00",
      "Contenido": "El salario es de $2000 USD mensuales"
    }
  ]
}
```

### Crear un nuevo chat
```bash
POST /chats/1/crear
Cookie: jwt_token=<token>
Content-Type: application/json

{
  "id_delegado": 1,
  "id_candidato": 2,
  "mensaje": "Hola, estoy interesado en la posición"
}

Response 201:
{
  "message": "Chat creado exitosamente",
  "chat": {
    "id_chat": "507f1f77bcf86cd799439013",
    "id_delegado": 1,
    "id_candidato": 2,
    "mensajes": [
      {
        "id_mensaje": "507f1f77bcf86cd799439014",
        "id_emisor": 1,
        "contenido": "Hola, estoy interesado en la posición",
        "timestamp": "2024-05-01T14:40:00"
      }
    ]
  }
}
```

### Enviar un mensaje a un chat
```bash
POST /chats/1/507f1f77bcf86cd799439011/enviar
Cookie: jwt_token=<token>
Content-Type: application/json

{
  "id_usuario": 1,
  "mensaje": "¿Cuándo es la entrevista?"
}

Response 201:
{
  "message": "Mensaje enviado exitosamente",
  "chat": {
    "id_chat": "507f1f77bcf86cd799439011",
    "id_delegado": 1,
    "id_candidato": 2,
    "mensajes": [...]
  }
}
```

### Eliminar un mensaje
```bash
DELETE /chats/1/507f1f77bcf86cd799439011/mensaje/507f1f77bcf86cd799439014/eliminar
Cookie: jwt_token=<token>

Response 200:
{
  "message": "Mensaje eliminado exitosamente"
}

Response 403:
{
  "error": "No se puede editar el mensaje porque no lo envio usted"
}
```

### Eliminar un chat
```bash
DELETE /chats/1/507f1f77bcf86cd799439011/eliminar
Cookie: jwt_token=<token>

Response 200:
{
  "message": "Chat eliminado exitosamente"
}

Response 403:
{
  "error": "No tienes permiso para eliminar este chat"
}
```

---

## 4. Gestión de Ofertas

### Ver todas las ofertas (Candidato)
```bash
GET /candidato/2/ofertas
Cookie: jwt_token=<token>
Rol: candidato

Response 200:
[
  {
    "ofertaId": 1,
    "titulo": "Desarrollador Python",
    "descripcion": "Buscamos desarrollador Python con 3+ años",
    "salario": 2500,
    "ubicacion": "Remoto",
    "empresa": "Tech Corp"
  },
  {
    "ofertaId": 2,
    "titulo": "Diseñador UX",
    "descripcion": "Diseñador UX con experiencia en apps",
    "salario": 2000,
    "ubicacion": "Madrid",
    "empresa": "Design Co"
  }
]
```

### Ver ofertas del delegado
```bash
GET /delegado/1/oferta
Cookie: jwt_token=<token>
Rol: delegado

Response 200:
[
  {
    "ofertaId": 1,
    "titulo": "Desarrollador Python",
    "descripcion": "Buscamos desarrollador Python con 3+ años",
    "salario": 2500,
    "ubicacion": "Remoto",
    "empresa": "Tech Corp"
  }
]
```

---

## 5. Gestión de Postulaciones

### Postularse a una oferta
```bash
POST /candidato/2/ofertas/1/postular
Cookie: jwt_token=<token>
Rol: candidato

Response 201:
{
  "postulacionId": 5,
  "candidatoId": 2,
  "ofertaId": 1,
  "estadoPostulacion": 2,
  "fechaPostulacion": "2024-05-01T15:00:00"
}

Response 400:
{
  "error": "Ya estás postulado a esta oferta"
}
o
{
  "error": "Usuario no es candidato"
}
```

### Obtener una postulación
```bash
GET /postulacion/5
Cookie: jwt_token=<token>

Response 200:
{
  "postulacionId": 5,
  "candidatoId": 2,
  "ofertaId": 1,
  "estadoPostulacion": 2,
  "fechaPostulacion": "2024-05-01T15:00:00"
}

Response 404:
{
  "error": "Postulación no encontrada"
}
```

### Cancelar una postulación
```bash
DELETE /postulacion/5
Cookie: jwt_token=<token>

Response 200:
{
  "postulacionId": 5,
  "candidatoId": 2,
  "ofertaId": 1,
  "estadoPostulacion": 2,
  "fechaPostulacion": "2024-05-01T15:00:00"
}

Response 404:
{
  "error": "Postulación no encontrada"
}
```

---

## Códigos de Estado HTTP Utilizados

| Código | Significado |
|--------|------------|
| 200 | OK - Operación exitosa |
| 201 | Created - Recurso creado exitosamente |
| 400 | Bad Request - Datos incompletos o inválidos |
| 401 | Unauthorized - Token no válido o expirado |
| 403 | Forbidden - Permisos insuficientes |
| 404 | Not Found - Recurso no encontrado |
| 500 | Internal Server Error - Error del servidor |

---

## Variables en Rutas

| Variable | Tipo | Descripción |
|----------|------|------------|
| `id`, `idU` | int | ID del usuario |
| `idChat` | string | ID del chat (MongoDB ObjectId) |
| `idMensaje` | string | ID del mensaje |
| `oferta_id` | int | ID de la oferta |
| `postulacion_id` | int | ID de la postulación |

---

## Headers Requeridos

```
Cookie: jwt_token=<token>
Content-Type: application/json (para POST/PUT)
```

---

## Estados de Postulación

| Código | Significado |
|--------|------------|
| 1 | Aceptada |
| 2 | Pendiente |
| 3 | Rechazada |
