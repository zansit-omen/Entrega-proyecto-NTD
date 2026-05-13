from Repositories.candidato_repo import candidato_repo
from Repositories.usuario_repo import usuarios_repo

def crear_candidato(usuario_id, profesion):
    if not all([usuario_id, profesion]):
        return None, "Datos incompletos", 400

    usuario = usuarios_repo.Obtener_user(usuario_id)
    if not usuario:
        return None, "Usuario no encontrado", 404

    if usuario["tipoUsuario"] != "candidato":
        return None, "El usuario no es de tipo candidato", 400

    if candidato_repo.ya_es_candidato(usuario_id):
        return None, "El usuario ya es candidato", 400

    candidato_id = candidato_repo.crear_candidato(usuario_id, profesion)
    return candidato_repo.buscar_por_id(candidato_id), None, 201

def obtener_candidato(candidato_id):
    candidato = candidato_repo.buscar_por_id(candidato_id)
    if not candidato:
        return None, "Candidato no encontrado", 404
    return candidato, None, 200