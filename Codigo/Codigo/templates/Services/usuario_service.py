from flask import jsonify

from Repositories.usuario_repo import usuarios_repo

def crear_usuario(nombre, correo, numero, tipo, password):
    
    if not all([nombre, correo, numero, tipo, password]):
            return jsonify({"error": "Datos incompletos"}), 400
        
    if usuarios_repo.Obtener_user(correo):
        return None, "El correo ya está registrado", 400
    
    user_id = usuarios_repo.crear_user(nombre, correo, numero, tipo, password)
    return usuarios_repo.Obtener_user(user_id), None, 201

def obtener_usuario(id):
    usuario = usuarios_repo.Obtener_user(id)
    if not usuario:
        return None, "Usuario no encontrado", 404
    return usuario, None, 200

def actualizar_usuario (id, nombre, correo, numero, tipo, password):
    
    if not all([nombre, correo, numero, tipo, password]):
            return jsonify({"error": "Datos incompletos"}), 400
        
    if not usuarios_repo.Obtener_user(id):
        return None, "Usuario no encontrado", 404
    
    usuarios_repo.actualizar_user(id, nombre, correo, numero, tipo, password)
    return usuarios_repo.Obtener_user(id), None, 200

def actualizar_contrasena(id, password):
    if not password:
        return jsonify({"error": "Contraseña es requerida"}), 400
    
    if not usuarios_repo.Obtener_user(id):
        return None, "Usuario no encontrado", 404
    
    usuarios_repo.actualizar_contra(id, password)
    return usuarios_repo.Obtener_user(id), None, 200


def eliminar_usuario(id):
    usuario = usuarios_repo.Obtener_user(id)
    if not usuario:
        return None, "Usuario no encontrado", 404
    
    usuarios_repo.borrar_user(id)
    return usuario, None, 200