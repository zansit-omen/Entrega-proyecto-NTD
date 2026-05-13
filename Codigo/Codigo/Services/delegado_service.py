from Repositories.delegado_repo import delegado_repo
from Repositories.usuario_repo import usuarios_repo
from Repositories.empresa_repo import empresa_repo

def crear_delegado(usuario_id, empresa_id):
    if not all([usuario_id, empresa_id]):
        return None, "Datos incompletos", 400

    usuario = usuarios_repo.Obtener_user(usuario_id)
    if not usuario:
        return None, "Usuario no encontrado", 404

    if usuario["tipoUsuario"] != "delegado":
        return None, "El usuario no es de tipo delegado", 400

    if not empresa_repo.buscar_por_id(empresa_id):
        return None, "Empresa no encontrada", 404

    if delegado_repo.ya_es_delegado(usuario_id):
        return None, "El usuario ya es delegado", 400

    delegado_id = delegado_repo.crear_delegado(usuario_id, empresa_id)
    return delegado_repo.buscar_por_usuario_id(delegado_id), None, 201

def obtener_delegado(Id):
    delegado = delegado_repo.buscar_por_usuario_id(Id)
    if not delegado:
        return None, "Delegado no encontrado", 404
    return delegado, None, 200