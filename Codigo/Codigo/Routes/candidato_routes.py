from flask import Blueprint, request, jsonify, render_template
from Services import candidato_service
from Cross.jwt_middleware import login_required, candidato_required


candidato_bp = Blueprint("candidato", __name__)

# ─────────────────────────────────────────────────────────────
# Rutas de Candidatos
# ─────────────────────────────────────────────────────────────

@candidato_bp.route("/crear-candidato", methods=["POST"])
@login_required
def crear_candidato(payload):
    data = request.get_json()
    resultado, error, status = candidato_service.crear_candidato(
        data.get("usuarioId"),
        data.get("profesion")
    )
    if error:
        return render_template("error_candidato.html", error=error)
    return render_template("perfil_candidato.html", candidato=resultado)

@candidato_bp.route("/candidato/<int:id>", methods=["GET"])
@candidato_required
def obtener_candidato(payload, id):

    resultado, error, status = candidato_service.obtener_candidato(id)

    if error:
        return render_template("error_candidato.html", error=error)

    return render_template(
        "perfil_candidato.html",
        candidato=resultado,
        idUsuario=resultado["Id"]
    )