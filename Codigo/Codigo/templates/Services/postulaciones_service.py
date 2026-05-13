from Repositories.postulacione_repo import postulacion_repo
from Repositories.candidato_repo import candidato_repo
from Repositories.ofertas_repo import oferta_repo

def obtener_por_oferta(oferta_id):
    rows = postulacion_repo.buscar_por_oferta(oferta_id)
    if not rows:
        return None, "No hay postulaciones para esta oferta", 404
    return rows, None, 200

def obtener_postulacion(postulacion_id):
    postulacion = postulacion_repo.buscar_por_id(postulacion_id)
    if not postulacion:
        return None, "Postulación no encontrada", 404
    return postulacion, None, 200

def postular(usuario_id, oferta_id):
    candidato = candidato_repo.buscar_por_usuario_id(usuario_id)
    if not candidato:
        return None, "El usuario no es candidato", 400

    if not oferta_repo.buscar_por_id(oferta_id):
        return None, "Oferta no encontrada", 404

    if postulacion_repo.buscar_por_candidato_y_oferta(candidato["candidatoId"], oferta_id):
        return None, "Ya estás postulado a esta oferta", 400

    post_id = postulacion_repo.insertar(candidato["candidatoId"], oferta_id)
    return postulacion_repo.buscar_por_id(post_id), None, 201

def aceptar(postulacion_id):
    if not postulacion_repo.buscar_por_id(postulacion_id):
        return None, "Postulación no encontrada", 404

    postulacion_repo.actualizar_estado(postulacion_id, 1)
    return postulacion_repo.buscar_por_id(postulacion_id), None, 200

def rechazar(postulacion_id):
    if not postulacion_repo.buscar_por_id(postulacion_id):
        return None, "Postulación no encontrada", 404

    postulacion_repo.actualizar_estado(postulacion_id, 0)
    return postulacion_repo.buscar_por_id(postulacion_id), None, 200

def cancelar(postulacion_id):
    postulacion = postulacion_repo.buscar_por_id(postulacion_id)
    if not postulacion:
        return None, "Postulación no encontrada", 404

    postulacion_repo.eliminar(postulacion_id)
    return postulacion, None, 200