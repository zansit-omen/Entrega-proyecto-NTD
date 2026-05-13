from datetime import datetime
from Repositories.chat_repo import chat_repo
from Repositories.usuario_repo import usuarios_repo

def obtener_chats_de_usuario(idU):
    if not usuarios_repo.Obtener_user(idU):
        return None, "Usuario no encontrado", 404

    chats = chat_repo.obtener_chats_usuario(idU)
    if not chats:
        return None, "El usuario no tiene chats", 404

    resultado = []
    for chat in chats:
        nombre_delegado = usuarios_repo.buscar_delegado_por_id(chat["id_delegado"])
        nombre_candidato = usuarios_repo.buscar_candidato_por_id(chat["id_candidato"])

        fecha = None
        for mensaje in chat.get("mensajes", []):
            fecha1 = datetime.strptime(mensaje["timestamp"], "%Y-%m-%dT%H:%M:%S")
            if fecha is None or fecha1 > fecha:
                fecha = fecha1

        resultado.append({
            "id_chat": chat["id_chat"],
            "delegado": nombre_delegado,
            "candidato": nombre_candidato,
            "fecha": fecha.isoformat() if fecha else None
        })

    return resultado, None, 200

def obtener_chat_detalle(idU, idChat):
    chats = chat_repo.obtener_chats_usuario(idU)
    chat = next((c for c in chats if c["id_chat"] == idChat), None)

    if not chat:
        return None, "El chat no pertenece a este usuario", 404

    nombre_candidato = usuarios_repo.buscar_candidato_por_id(chat["id_candidato"])
    nombre_delegado = usuarios_repo.buscar_delegado_por_id(chat["id_delegado"])
    mensajes = chat.get("mensajes", [])

    if not mensajes:
        return {
            "candidato": nombre_candidato,
            "delegado": nombre_delegado,
            "mensajes": "No hay mensajes aún"
        }, None, 200

    info_mensajes = []
    for mensaje in mensajes:
        emisor = (nombre_candidato if mensaje["id_emisor"] == chat["id_candidato"]
                  else nombre_delegado)
        timestamp = mensaje.get("timestamp")
        fecha = datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%S") if timestamp else None
        info_mensajes.append({
            "enviado_por": emisor,
            "fecha": fecha.isoformat() if fecha else None,
            "contenido": mensaje["contenido"]
        })

    return {
        "candidato": nombre_candidato,
        "delegado": nombre_delegado,
        "mensajes": info_mensajes
    }, None, 200

def enviar_mensaje(id_chat, id_usuario, contenido):
    if not id_usuario or not contenido:
        return None, "Datos incompletos", 400

    chat = chat_repo.ver_chat(id_chat)
    if not chat:
        return None, "Chat no encontrado", 404

    if id_usuario != chat["id_delegado"] and id_usuario != chat["id_candidato"]:
        return None, "El usuario no pertenece a este chat", 403

    chat_repo.enviar_mensaje(id_chat, id_usuario, contenido)
    return chat_repo.ver_chat(id_chat), None, 201

def crear_chat(idU, id_delegado, id_candidato, mensaje):
    if not all([id_delegado, id_candidato, mensaje]):
        return None, "Datos incompletos", 400

    if idU != id_delegado and idU != id_candidato:
        return None, "El usuario no está involucrado en este chat", 403

    if not usuarios_repo.buscar_delegado_por_id(id_delegado):
        return None, "Delegado no encontrado", 404

    if not usuarios_repo.buscar_candidato_por_id(id_candidato):
        return None, "Candidato no encontrado", 404

    nuevo_chat = chat_repo.crear_chat_con_mensaje(
        id_delegado, id_candidato, idU, mensaje
    )
    return nuevo_chat, None, 201

def eliminar_mensaje(idU, id_chat, id_mensaje):
    if not usuarios_repo.Obtener_user(idU):
        return None, "Usuario no encontrado", 404

    chat = chat_repo.ver_chat(id_chat)
    if not chat:
        return None, "Chat no encontrado", 404

    exito = chat_repo.eliminar_chat_mensaje(id_chat, idU, id_mensaje)
    if not exito:
        return None, "No se pudo eliminar. Verifica que eres el autor.", 403

    return {"message": "Mensaje eliminado"}, None, 200

def eliminar_chat(idU, id_chat):
    if not usuarios_repo.Obtener_user(idU):
        return None, "Usuario no encontrado", 404

    chat = chat_repo.ver_chat(id_chat)
    if not chat:
        return None, "Chat no encontrado", 404

    if chat["id_candidato"] != idU:
        return None, "No tienes permiso para eliminar este chat", 403

    chat_repo.eliminar_chat(id_chat)
    return {"message": "Chat eliminado"}, None, 200