from flask import Blueprint, redirect, render_template, request, jsonify, url_for
import Services.usuario_service as usuario_service 
import Services.candidato_service as candidato_service
import Services.delegado_service as delegado_service 
import Services.empresa_service as empresa_service
from Cross.jwt_middleware import login_required

usuario_bp = Blueprint("usuario", __name__)

@usuario_bp.route("/usuario/crear", methods=["GET"])
def crear_usuario_form():
    return render_template("registro.html")

@usuario_bp.route("/usuario/crear", methods=["POST"])
def crear_usuario():

    nombre = request.form.get("nombre")
    correo = request.form.get("correo")
    numero = request.form.get("numero")
    tipoU = request.form.get("tipoUsuario")
    password = request.form.get("password")

    # =========================
    # CREAR USUARIO
    # =========================

    resultado, e, status = usuario_service.crear_usuario(
        nombre,
        correo,
        numero,
        tipoU,
        password
    )
    print("usuario creado")
    if e:
        return render_template("error_usuario.html", error=e)

    # =========================
    # CREAR DELEGADO
    # =========================

    if tipoU == "delegado":
        print("acceso al if donde se verifica delegado")
        delegado, e, status = usuario_service.obtener_usuario_por_correo(correo)

        empresa, e, status = empresa_service.obtener_empresa_razon(
            request.form.get("razonSocial")
        )
        if not empresa:
            return render_template(
                "error_usuario.html",
                error="Empresa no encontrada"
            )
        print ("se accedio a la empresa de acuerdo a su razon social")
        resultado, e, status = delegado_service.crear_delegado(
            delegado.get("Id"),
            empresa.get("empresaId")
        )
        print ("Se creo delegado")
    # =========================
    # CREAR CANDIDATO
    # =========================

    elif tipoU == "candidato":

        candidato, e, status = usuario_service.obtener_usuario_por_correo(correo)

        resultado, e, status = candidato_service.crear_candidato(
            candidato.get("Id"),
            request.form.get("profesion")
        )

    # =========================
    # VALIDAR ERRORES
    # =========================

    if e:
        return render_template("error_usuario.html", error=e)

    return render_template("login.html"), 201

@usuario_bp.route("/usuario/<int:id>", methods=["GET"])
@login_required
def obtener_usuario(payload, id):
    resultado, e, status = usuario_service.obtener_usuario(id)
    if e:
        return render_template("error_usuario.html", error=e)
    return render_template("perfil_usuario.html", usuario=resultado)

@usuario_bp.route("/actualizar-usuario/<int:id>", methods=["PUT"])
@login_required
def actualizar_usuario(payload, id):
    resultado, e, status = usuario_service.actualizar_usuario(
        id,
        request.form.get("nombre"),
        request.form.get("correo"),
        request.form.get("numero"),
        request.form.get("tipoUsuario"),
    )
    if e:
        return render_template("error_usuario.html", error=e)
    return render_template("perfil_usuario.html", usuario=resultado)

@usuario_bp.route("/actualizar-contrasena/<int:id>", methods=["PUT"])
@login_required
def actualizar_contrasena(payload, id):
    resultado, e, status = usuario_service.actualizar_contrasena(
        id,
        request.form.get("password")
    )
    if e:
        return render_template("error_usuario.html", error=e)
    return url_for('auth.login_form')

@usuario_bp.route("/borrar-usuario/<int:id>", methods=["DELETE"])
@login_required
def borrar_usuario(payload, id):
    resultado, e, status = usuario_service.eliminar_usuario(id)
    if e:
        return render_template("error_usuario.html", error=e)
    return render_template("registro.html")