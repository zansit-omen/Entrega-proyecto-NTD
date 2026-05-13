from flask import Blueprint, redirect, render_template, request, jsonify, url_for
from Services import delegado_service
from Cross.jwt_middleware import login_required, delegado_required

delegado_bp = Blueprint("delegado", __name__)

# ─────────────────────────────────────────────────────────────
# Rutas de Delegados
# ─────────────────────────────────────────────────────────────

@delegado_bp.route("/crear-delegado", methods=["POST"])
def crear_delegado(payload):
    if request.is_json:
        data = request.get_json()
    else:
        data = request.form
    resultado, e, status = delegado_service.crear_delegado(
        data.get("usuarioId"),
        data.get("empresaId")
    )
    if e:
        return render_template("error_delegado.html", error=e)
    return redirect(url_for("login"))

@delegado_bp.route("/delegado/<int:id>", methods=["GET"])
@delegado_required
def buscar_delegado(payload, id):
    usuario_id = int(payload.get("sub"))
    resultado, e, status = delegado_service.obtener_delegado(id)
    if e:
        return render_template("error_delegado.html", error=e)
    return render_template("perfil_delegado.html", delegado=resultado, usuarioId=usuario_id)