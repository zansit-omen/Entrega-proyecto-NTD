from Repositories.ofertas_repo import oferta_repo
from Repositories.delegado_repo import delegado_repo

def obtener_todas():
    ofertas = oferta_repo.obtener_todas()
    if not ofertas:
        return None, "No hay ofertas disponibles", 404
    return ofertas, None, 200

def obtener_por_id(oferta_id):
    oferta = oferta_repo.buscar_por_id(oferta_id)
    if not oferta:
        return None, "Oferta no encontrada", 404
    return oferta, None, 200

def crear_oferta(usuario_id, titulo, descripcion, profesion):
    if not all([titulo, descripcion, profesion]):
        return None, "Datos no válidos", 400

    delegado = delegado_repo.buscar_por_usuario_id(usuario_id)
    if not delegado:
        return None, "Delegado no encontrado", 404

    oferta_id = oferta_repo.insertar(delegado["empresaId"], titulo, descripcion, profesion)
    return oferta_repo.buscar_por_id(oferta_id), None, 201

def actualizar_oferta(oferta_id, titulo, descripcion, profesion, estado):
    if not all([titulo, descripcion, profesion]):
        return None, "Datos no válidos", 400

    oferta = oferta_repo.buscar_por_id(oferta_id)
    if not oferta:
        return None, "Oferta no encontrada", 404

    oferta_repo.actualizar(
        oferta_id, titulo, descripcion, profesion,
        estado if estado is not None else oferta["estadoOferta"]
    )
    return oferta_repo.buscar_por_id(oferta_id), None, 200

def eliminar_oferta(oferta_id):
    oferta = oferta_repo.buscar_por_id(oferta_id)
    if not oferta:
        return None, "Oferta no encontrada", 404

    oferta_repo.eliminar(oferta_id)
    return oferta, None, 200