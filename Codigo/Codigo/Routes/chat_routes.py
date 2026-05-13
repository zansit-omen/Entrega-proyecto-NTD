from flask import Blueprint, render_template, request, jsonify, redirect, url_for
from Services.chat_service import chat_service
from Repositories.usuario_repo import usuarios_repo
from Cross.jwt_middleware import login_required

chat_bp = Blueprint("chat", __name__)



@chat_bp.route("/chats/<int:idU>", methods=["GET"])
@login_required
def ver_chats(payload, idU):
    id_usuario = int(payload.get("sub"))
    if id_usuario != idU:
        return render_template(
            "error_chat.html",
            error="No tienes permiso para ver estos chats",
            usuario=id_usuario,
        ), 403

    resultado, error, status = chat_service.obtener_chats_de_usuario(id_usuario)
    if error:
        return render_template("error_chat.html", error=error, usuario=id_usuario), status

    # Obtener identidad para saber si es candidato o delegado
    identidad = usuarios_repo.obtener_identidad_chat(id_usuario)
    disponibles = []
    tipo = None
    if identidad:
        if identidad.get("tipoUsuario") == "candidato" and identidad.get("candidatoId"):
            disponibles = usuarios_repo.listar_delegados_disponibles_para_candidato(identidad["candidatoId"])
            tipo = "delegado"
        elif identidad.get("tipoUsuario") == "delegado" and identidad.get("delegadoId"):
            disponibles = usuarios_repo.listar_candidatos_disponibles_para_delegado(identidad["delegadoId"])
            tipo = "candidato"

    return render_template(
        "lista_chats.html",
        chats=resultado,
        idUsuario=id_usuario,
        disponibles=disponibles,
        tipo_disponible=tipo,
        identidad=identidad,
    )


@chat_bp.route("/chats/<int:idU>/<int:idChat>", methods=["GET"])
@login_required
def obtener_chat(payload, idU, idChat):
    id_usuario = int(payload.get("sub"))
    if id_usuario != idU:
        return render_template(
            "error_chat.html",
            error="No tienes permiso para ver este chat",
            usuario=id_usuario,
        ), 403

    resultado, error, status = chat_service.obtener_chat_detalle(id_usuario, idChat)
    if error:
        return render_template("error_chat.html", error=error, usuario=id_usuario), status

    return render_template("chat_detalle.html", chat=resultado, usuario=id_usuario)



@chat_bp.route("/chats/<int:idU>", methods=["POST"])
@login_required
def crear_chat(payload, idU):
    try:
        id_usuario = int(payload.get("sub"))
        if id_usuario != idU:
            return render_template("error_chat.html", error="No tienes permiso para crear chats para este usuario", usuario=id_usuario), 403

        data = request.get_json() if request.is_json else request.form.to_dict()
        id_delegado = int(data.get("id_delegado"))
        id_candidato = int(data.get("id_candidato"))
        mensaje = data.get("mensaje", "").strip()

        if not mensaje:
            return render_template("error_chat.html", error="El mensaje no puede estar vacio", usuario=id_usuario), 400

        resultado, error, status = chat_service.crear_chat(
            id_usuario,
            id_delegado,
            id_candidato,
            mensaje,
        )
        if error:
            return render_template("error_chat.html", error=error, usuario=id_usuario), status

        # Redirigir al detalle del chat creado
        return redirect(url_for("chat.obtener_chat", idU=id_usuario, idChat=resultado.get("id_chat")))
    except (TypeError, ValueError):
        return render_template("error_chat.html", error="Datos invalidos para crear el chat", usuario=idU), 400
    except Exception as e:
        return render_template("error_chat.html", error=f"Error al crear chat: {str(e)}", usuario=idU), 500


@chat_bp.route("/chats/<int:id_chat>/mensaje", methods=["POST"])
@chat_bp.route("/chats/<int:idU>/<int:id_chat>/mensaje", methods=["POST"])
@login_required
def enviar_mensaje(payload, id_chat, idU=None):
    try:
        id_usuario = int(payload.get("sub"))
        if idU is not None and id_usuario != idU:
            return jsonify({"error": "No tienes permiso para enviar mensajes para este usuario"}), 403

        data = request.get_json() if request.is_json else request.form.to_dict()
        mensaje = data.get("mensaje", "").strip()

        if not mensaje:
            return jsonify({"error": "El mensaje no puede estar vacio"}), 400

        resultado, error, status = chat_service.enviar_mensaje(id_chat, id_usuario, mensaje)
        if error:
            return jsonify({"error": error}), status

        return jsonify({
            "message": "Mensaje enviado exitosamente",
            "chat": {"id_chat": str(resultado.get("id_chat")) if resultado else str(id_chat)},
        }), 201
    except Exception as e:
        return jsonify({"error": f"Error al enviar mensaje: {str(e)}"}), 500


@chat_bp.route("/chats/<int:idU>/<int:id_chat>/<int:id_mensaje>", methods=["DELETE"])
@login_required
def eliminar_mensaje(payload, idU, id_chat, id_mensaje):
    id_usuario = int(payload.get("sub"))
    if id_usuario != idU:
        return jsonify({"error": "No tienes permiso para eliminar este mensaje"}), 403

    resultado, error, status = chat_service.eliminar_mensaje(id_usuario, id_chat, id_mensaje)
    if error:
        return jsonify({"error": error}), status

    return jsonify({
        "message": "Mensaje eliminado exitosamente",
        "chat": {"id_chat": str(resultado.get("id_chat")) if resultado else str(id_chat)},
    }), 200


@chat_bp.route("/chats/<int:idU>/<int:id_chat>", methods=["DELETE"])
@login_required
def eliminar_chat(payload, idU, id_chat):
    id_usuario = int(payload.get("sub"))
    if id_usuario != idU:
        return jsonify({"error": "No tienes permiso para eliminar este chat"}), 403

    resultado, error, status = chat_service.eliminar_chat(id_usuario, id_chat)
    if error:
        return jsonify({"error": error}), status

    return jsonify({
        "message": "Chat eliminado exitosamente",
        "chat": {"id_chat": str(resultado.get("id_chat")) if resultado else str(id_chat)},
    }), 200
