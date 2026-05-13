import bcrypt
# ──────────────────────────────────────────────────────────────
# Utilidades de contraseña segura
# ──────────────────────────────────────────────────────────────

def hash_password(plain_password: str) -> str:
    """Genera un hash seguro para la contraseña."""
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(plain_password.encode('utf-8'), salt)
    return hashed.decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifica una contraseña contra su hash."""
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

import jwt
import datetime
import os
from functools import wraps
from flask import request, redirect, url_for, flash, jsonify
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# JWT Configuracion desde .env
SECRET_KEY = os.getenv("JWT_SECRET_KEY")
ALGORITHM = os.getenv("JWT_ALGORITHM")
TOKEN_EXP_HOURS = int(os.getenv("JWT_TOKEN_EXP_HOURS"))
COOKIE_NAME = os.getenv("JWT_COOKIE_NAME")


class JWTMiddleware:
    """Middleware de autenticación JWT."""

    @staticmethod
    def generar_token(user_id: int, email: str, rol: str, nombre: str) -> str:
        """
        Genera un token JWT para un usuario.

        Args:
            user_id: ID del usuario
            email: Email del usuario
            rol: Rol del usuario
            nombre: Nombre del usuario

        Returns:
            Cadena del token JWT
        """
        ahora = datetime.datetime.now(datetime.timezone.utc)
        payload = {
            "sub": str(user_id),
            "email": email,
            "rol": rol,
            "nombre": nombre,
            "iat": int(ahora.timestamp()),
            "exp": int(
                (ahora + datetime.timedelta(hours=TOKEN_EXP_HOURS)).timestamp()
            ),
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
        print(f"[JWT] Token generado: {token[:30]}...")
        return token

    @staticmethod
    def obtener_payload_actual() -> dict | None:
        """
        Obtiene el payload JWT actual de las cookies.

        Returns:
            Diccionario de payload o None si es inválido
        """
        token = request.cookies.get(COOKIE_NAME)
        if not token:
            print("[JWT] No se encontró cookie")
            return None
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            print(f"[JWT] Token válido para: {payload.get('email')}")
            return payload
        except jwt.PyJWTError as e:
            print(f"[JWT] Error al decodificar: {e}")
            return None


# ──────────────────────────────────────────────────────────────
# Funciones auxiliares para compatibilidad hacia atrás
# ──────────────────────────────────────────────────────────────


def generar_token(user_id: int, email: str, rol: str, nombre: str) -> str:
    """Genera un token JWT."""
    return JWTMiddleware.generar_token(user_id, email, rol, nombre)


def obtener_payload_actual() -> dict | None:
    """Obtiene el payload JWT actual de las cookies."""
    return JWTMiddleware.obtener_payload_actual()


# ──────────────────────────────────────────────────────────────
# Decoradores de protección
# ──────────────────────────────────────────────────────────────


def login_required(f):
    """Decorador para requerir login (cualquier usuario autenticado)."""

    @wraps(f)
    def decorated(*args, **kwargs):
        payload = obtener_payload_actual()
        if payload is None:
            return redirect('/login')

        user_id_from_token = int(payload.get("sub"))
        user_id_from_url = kwargs.get("id")

        if user_id_from_url:
            if user_id_from_token != int(user_id_from_url):
                return redirect('/login')

        return f(payload, *args, **kwargs)

    return decorated


def delegado_required(f):
    """Decorador para requerir rol de delegado."""

    @wraps(f)
    def decorated(*args, **kwargs):
        payload = obtener_payload_actual()
        if payload is None:
            return redirect('/login')

        if payload.get("rol") != "delegado":
            return redirect('/login')

        user_id_from_token = int(payload.get("sub"))
        user_id_from_url = kwargs.get("idU") or kwargs.get("id")

        if user_id_from_url:
            if user_id_from_token != int(user_id_from_url):
                return redirect('/login')

        return f(payload, *args, **kwargs)

    return decorated    
    
def candidato_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        payload = obtener_payload_actual()
        if not payload:
            return redirect('/login')
        if payload.get("rol") != "candidato":
            return redirect('/login')
        
        id_token = int(payload.get("sub"))  
        id_url = kwargs.get("idU") or kwargs.get("id")
        
        if id_url and id_token != int(id_url):
            return redirect('/login')
        
        return f(payload, *args, **kwargs)
    return decorated