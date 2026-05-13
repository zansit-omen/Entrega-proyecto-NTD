from flask import Blueprint, redirect, render_template, request, jsonify, url_for
from Services import postulaciones_service, candidato_service
from Cross.jwt_middleware import delegado_required, login_required, candidato_required

postulacion_bp = Blueprint("postulacion", __name__)

@postulacion_bp.route("/delegado/<int:idU>/oferta/<int:oferta_id>/postulacion", methods=["GET"])
@delegado_required
def ver_postulaciones(payload, idU, oferta_id):
    resultado, e, status = postulaciones_service.obtener_por_oferta(oferta_id)
    if e:
        return render_template("error_postulacion.html", error=e)
    return render_template(
        "lista_postulaciones.html",
        postulaciones=resultado,
        oferta=oferta_id,
        idUsuario=int(payload.get("sub")),
        tipoUsuario="delegado"
    )
@postulacion_bp.route("/candidato/<int:idU>/postulacion", methods=["GET"])
@candidato_required
def ver_postulaciones_candidato(payload, idU):

    usuario_id = int(payload.get("sub"))

    candidato, e, status = candidato_service.obtener_usuario_id(usuario_id)

    if e:
        return render_template("error_postulacion.html", error=e)

    resultado, e, status = postulaciones_service.postulaciones_canidato(
        candidato.get("candidatoId")
    )

    if e:
        return render_template("error_postulacion.html", error=e)

    return render_template(
    "lista_postulaciones.html",
    postulaciones=resultado,
    idUsuario=usuario_id,
    tipoUsuario="candidato"
    )

@postulacion_bp.route(
    "/delegado/<int:idU>/oferta/<int:oferta_id>/postulacion/<int:postulacion_id>/aceptar",
    methods=["POST"]
)
@delegado_required
def aceptar_postulacion(payload, idU, oferta_id, postulacion_id):

    resultado, e, status = postulaciones_service.aceptar(postulacion_id)

    if e:
        return render_template("error_postulacion.html", error=e)

    return redirect(
        url_for(
            "postulacion.ver_postulaciones",
            idU=idU,
            oferta_id=oferta_id
        )
    )
@postulacion_bp.route(
    "/delegado/<int:idU>/oferta/<int:oferta_id>/postulacion/<int:postulacion_id>/rechazar",
    methods=["POST"]
)
@delegado_required
def rechazar_postulacion(payload, idU, oferta_id, postulacion_id):

    resultado, e, status = postulaciones_service.rechazar(postulacion_id)

    if e:
        return render_template("error_postulacion.html", error=e)

    return redirect(
        url_for(
            "postulacion.ver_postulaciones",
            idU=idU,
            oferta_id=oferta_id
        )
    )
@postulacion_bp.route("/postulacion/<int:postulacion_id>", methods=["GET"])
@login_required
def obtener_postulacion(payload, postulacion_id):
    resultado, e, status = postulaciones_service.obtener_postulacion(postulacion_id)
    if e:
        return render_template("error_postulacion.html", error=e)
    return render_template("postulacion_detalle.html", postulacion=resultado)

@postulacion_bp.route("/postulacion/<int:postulacion_id>/cancelar", methods=["POST"])
@candidato_required
def cancelar_postulacion(payload, postulacion_id):
    resultado, e, status = postulaciones_service.cancelar(postulacion_id)
    if e:
        return render_template("error_postulacion.html", error=e)
    return redirect(f"/candidato/{id(payload.get("sub"))}")