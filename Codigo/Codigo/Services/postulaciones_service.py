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

def postulaciones_canidato(candidato_id):
    postulacion = postulacion_repo.buscar_por_candidato(candidato_id)
    if not postulacion:
        return None, "Postulación no encontrada", 404
    return postulacion, None, 200

def postular(usuario_id, oferta_id):
    candidato = candidato_repo.buscar_por_usuario_id(usuario_id)

    if not candidato:
        return None, "El usuario no está registrado como candidato", 400

    oferta = oferta_repo.buscar_por_id(oferta_id)
    if not oferta:
        return None, "La oferta no existe", 404

    ya_postulado = postulacion_repo.buscar_por_candidato_y_oferta(
        candidato["candidatoId"],
        oferta_id
    )

    if ya_postulado:
        return None, "Ya estás postulado a esta oferta", 400

    post_id = postulacion_repo.insertar(candidato["candidatoId"], oferta_id)

    if not post_id:
        return None, "Error al crear la postulación", 500

    return postulacion_repo.buscar_por_id(post_id), None, 201

def aceptar(postulacion_id):
    try:
        if not postulacion_repo.buscar_por_id(postulacion_id):
            return None, "Postulación no encontrada", 404

        exito = postulacion_repo.actualizar_estado(postulacion_id, 1)
        
        if not exito:
            return None, "Error al actualizar el estado de la postulación", 500
            
        return postulacion_repo.buscar_por_id(postulacion_id), None, 200
    except Exception as e:
        return None, f"Error al aceptar postulación: {str(e)}", 500

def rechazar(postulacion_id):
    try:
        if not postulacion_repo.buscar_por_id(postulacion_id):
            return None, "Postulación no encontrada", 404

        exito = postulacion_repo.actualizar_estado(postulacion_id, 0)
        
        if not exito:
            return None, "Error al actualizar el estado de la postulación", 500
            
        return postulacion_repo.buscar_por_id(postulacion_id), None, 200
    except Exception as e:
        return None, f"Error al rechazar postulación: {str(e)}", 500

def cancelar(postulacion_id):
    try:
        postulacion = postulacion_repo.buscar_por_id(postulacion_id)
        if not postulacion:
            return None, "Postulación no encontrada", 404

        exito = postulacion_repo.eliminar(postulacion_id)
        
        if not exito:
            return None, "Error al eliminar la postulación", 500
            
        return postulacion, None, 200
    except Exception as e:
        return None, f"Error al cancelar postulación: {str(e)}", 500