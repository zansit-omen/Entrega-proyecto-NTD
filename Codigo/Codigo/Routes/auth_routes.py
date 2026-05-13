from flask import Blueprint, render_template, request, jsonify, make_response, redirect
from Services.auth_service import login
from Cross.jwt_middleware import COOKIE_NAME

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/login", methods=["GET"])
def login_form():
    return render_template("login.html")

@auth_bp.route("/login", methods=["POST"])
def login_route():
    if request.is_json:
        data = request.get_json()
    else:
        data = request.form

    correo = data.get("correo")
    password = data.get("password")

    resultado, error, status = login(correo, password)
    if error:
        return render_template("error_login.html", error=error)

    # Siempre establecer la cookie JWT, tanto para JSON como para form
    destino = f"/delegado/{resultado['id']}" if resultado["tipoUsuario"] == "delegado" else f"/candidato/{resultado['id']}"
    response = make_response(redirect(destino))
    response.set_cookie(
        COOKIE_NAME,
        resultado["token"],
        httponly=True,
        secure=False,  # Importante para desarrollo local
        samesite="Lax",
        path="/"
    )
    return response