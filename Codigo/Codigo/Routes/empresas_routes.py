from flask import Blueprint, request, jsonify, render_template
from Services import empresa_service
from Cross.jwt_middleware import delegado_required

empresa_bp = Blueprint("empresa", __name__)

@empresa_bp.route("/delegado/<int:idU>/empresa", methods=["POST"])
@delegado_required
def crear_empresa(payload, idU):
    if request.is_json():
        data = request.get_json()
    else:
        data = request.form
        
    resultado, e, status = empresa_service.crear_empresa(
        data.get("razonSocial"),
        data.get("correoContacto"),
        data.get("direccion")
    )
    if e:
        return render_template("error_empresa.html", error=e)
    return render_template("empresa_detalle.html", empresa=resultado)

@empresa_bp.route("/delegado/<int:idU>/empresa/<int:empresa_id>", methods=["GET"])
@delegado_required
def obtener_empresa(payload, idU, empresa_id):
    resultado, e, status = empresa_service.obtener_empresa(empresa_id)
    if e:
        return render_template("error_empresa.html", error=e)
    return render_template("empresa_detalle.html", empresa=resultado)

@empresa_bp.route("/delegado/<int:idU>/empresa/<int:empresa_id>", methods=["PUT"])
@delegado_required
def actualizar_empresa(payload, idU, empresa_id):
    data = request.get_json()
    resultado, e, status = empresa_service.actualizar_empresa(
        empresa_id,
        data.get("razonSocial"),
        data.get("correoContacto"),
        data.get("direccion")
    )
    if e:
        return render_template("error_empresa.html", error=e)
    return render_template("empresa_detalle.html", empresa=resultado)

@empresa_bp.route("/delegado/<int:idU>/empresa/<int:empresa_id>", methods=["DELETE"])
@delegado_required
def eliminar_empresa(payload, idU, empresa_id):
    resultado, e, status = empresa_service.eliminar_empresa(empresa_id)
    if e:
        return render_template("error_empresa.html", error=e)
    return render_template("perfil_delegado.html", usuario=idU)