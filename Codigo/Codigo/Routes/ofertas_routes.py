from flask import Blueprint, request, jsonify, render_template
from Services import oferta_service
from Cross.jwt_middleware import delegado_required, candidato_required

oferta_bp = Blueprint("oferta", __name__)

@oferta_bp.route("/delegado/oferta", methods=["GET"])
@delegado_required
def obtener_ofertas(payload):
    usuario_id = int(payload.get("sub"))
    resultado, e, status = oferta_service.obtener_ofertas_delegado(usuario_id)
    if e:
        return render_template("error_oferta.html", error=e)
    return render_template("lista_ofertas.html", ofertas=resultado, autor=usuario_id, tipoUsuario=payload.get("rol"), usuarioId=usuario_id)


@oferta_bp.route("/delegado/oferta/crear", methods=["GET"])
@delegado_required
def crear_oferta_form(payload):
    return render_template("crear_oferta.html", usuarioId=int(payload.get("sub")), tipoUsuario=payload.get("rol"))

@oferta_bp.route("/delegado/oferta/crear", methods=["POST"])
@delegado_required
def crear_oferta(payload):
    usuario_id = int(payload.get("sub"))
    if request.is_json:
        data = request.get_json()
    else:
        data = request.form

    resultado, e, status = oferta_service.crear_oferta(
        usuario_id,
        data.get("titulo"),
        data.get("descripcionOferta"),
        data.get("profesionBuscar")
    )
    if e:
        return render_template("error_oferta.html", error=e)
    puede_editar, _ = oferta_service.puede_editar_oferta(payload.get("rol"), usuario_id, resultado["ofertaId"])
    return render_template("oferta_detalle.html", oferta=resultado, tipoUsuario=payload.get("rol"), usuarioId=usuario_id, puede_editar=puede_editar)

@oferta_bp.route("/delegado/oferta/<int:oferta_id>", methods=["GET"])
@delegado_required
def buscar_oferta(payload, oferta_id):
    # Usar el ID del token para mayor seguridad
    usuario_id = int(payload.get("sub"))
    
    resultado, e, status = oferta_service.obtener_por_id(oferta_id)
    if e:
        return render_template("error_oferta.html", error=e)
    
    # Debug completo
    rol = payload.get("rol")
    empresa_delegado = oferta_service.obtener_empresa_delegado(usuario_id)
    empresa_oferta = oferta_service.obtener_empresa_oferta(oferta_id)
    puede_editar, msg = oferta_service.puede_editar_oferta(rol, usuario_id, oferta_id)
    
    print(f"=== DEBUG buscar_oferta ===")
    print(f"payload.get('sub'): {usuario_id}")
    print(f"rol: {rol}")
    print(f"oferta_id: {oferta_id}")
    print(f"empresa_delegado (usuario_id={usuario_id}): {empresa_delegado}")
    print(f"empresa_oferta (oferta_id={oferta_id}): {empresa_oferta}")
    print(f"puede_editar: {puede_editar}, msg: {msg}")
    print(f"======================")
    
    return render_template("oferta_detalle.html", oferta=resultado, tipoUsuario=rol, usuarioId=usuario_id, puede_editar=puede_editar)

@oferta_bp.route("/delegado/oferta/<int:oferta_id>", methods=["PUT"])
@delegado_required
def actualizar_oferta(payload, oferta_id):
    usuario_id = int(payload.get("sub"))
    # Verificar permisos de edición
    puede_editar, msg_error = oferta_service.puede_editar_oferta(
        payload.get("rol"), usuario_id, oferta_id
    )
    if not puede_editar:
        return render_template("error_oferta.html", error=msg_error), 403
    
    if request.is_json:
        data = request.get_json()
    else:
        data = request.form
    resultado, e, status = oferta_service.actualizar_oferta(
        oferta_id,
        data.get("titulo"),
        data.get("descripcionOferta"),
        data.get("profesionBuscar"),
        data.get("estadoOferta")
    )
    if e:
        return render_template("error_oferta.html", error=e)
    puede_editar, _ = oferta_service.puede_editar_oferta(payload.get("rol"), usuario_id, oferta_id)
    return render_template("oferta_detalle.html", oferta=resultado, tipoUsuario=payload.get("rol"), usuarioId=usuario_id, puede_editar=puede_editar)

@oferta_bp.route("/delegado/oferta/<int:oferta_id>", methods=["DELETE"])
@delegado_required
def eliminar_oferta(payload,oferta_id):
    usuario_id = int(payload.get("sub"))
    # Verificar permisos de eliminación
    puede_editar, msg_error = oferta_service.puede_editar_oferta(
        payload.get("rol"), usuario_id, oferta_id
    )
    if not puede_editar:
        return render_template("error_oferta.html", error=msg_error), 403
    
    resultado, e, status = oferta_service.eliminar_oferta(oferta_id)
    if e:
        return render_template("error_oferta.html", error=e)
    return render_template("lista_ofertas.html", ofertas=resultado, autor=usuario_id, tipoUsuario=payload.get("rol"), usuarioId=usuario_id)

@oferta_bp.route("/candidato/ofertas/<int:oferta_id>", methods=["GET"])
@candidato_required
def ver_detalle_oferta_candidato(payload, oferta_id):
    usuario_id = int(payload.get("sub"))
    resultado, e, status = oferta_service.obtener_por_id(oferta_id)
    if e:
        return render_template("error_oferta.html", error=e)
    return render_template("oferta_detalle.html", oferta=resultado, tipoUsuario=payload.get("rol"), usuarioId=usuario_id, puede_editar=False)

@oferta_bp.route("/candidato/ofertas", methods=["GET"])
@candidato_required
def ver_ofertas_candidato(payload):
    usuario_id = int(payload.get("sub"))
    resultado, e, status = oferta_service.obtener_todas()
    if e:
        return render_template("error_oferta.html", error=e)
    return render_template("lista_ofertas.html", ofertas=resultado, autor=usuario_id, tipoUsuario=payload.get("rol"), usuarioId=usuario_id)

@oferta_bp.route("/candidato/ofertas/<int:oferta_id>/postular", methods=["POST"])
@candidato_required
def postular_oferta(payload, oferta_id):
    usuario_id = int(payload.get("sub"))

    from Services import postulaciones_service

    resultado, e, status = postulaciones_service.postular(usuario_id, oferta_id)

    if e:
        print(f"[POSTULACIÓN ERROR] user={usuario_id} oferta={oferta_id} error={e}")
        return render_template("error_oferta.html", error=e), status

    return render_template("postulacion_exitosa.html", postulacion=resultado)