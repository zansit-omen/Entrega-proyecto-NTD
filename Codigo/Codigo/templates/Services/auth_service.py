from Repositories.usuario_repo import usuarios_repo
from Cross.jwt_middleware import JWTMiddleware

def login(correo, password):
    usuario = usuarios_repo.buscar_por_correo(correo)
    
    if not usuario:
        return None, "Correo no encontrado", 404
    
    if usuario["password"] != password:
        return None, "Contraseña incorrecta", 401
    
    token = JWTMiddleware.generar_token(
        usuario["Id"],
        usuario["correo"],
        usuario["tipoUsuario"],
        usuario["nombre"]
    )
    
    return {
        "token": token,
        "id": usuario["Id"],
        "nombre": usuario["nombre"],
        "tipoUsuario": usuario["tipoUsuario"]
    }, None, 200