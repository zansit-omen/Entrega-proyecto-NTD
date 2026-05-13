from datetime import datetime
from Repositories.chat_repositorio import chat_repositorio
from Repositories.usuario_repo import usuarios_repo


class chat_service:
    @staticmethod
    def _parse_fecha(valor):
        if isinstance(valor, datetime):
            return valor

        if not valor:
            return None

        try:
            return datetime.fromisoformat(str(valor).replace("Z", "+00:00"))
        except ValueError:
            return None

    @staticmethod
    def _formatear_fecha(valor):
        fecha = chat_service._parse_fecha(valor)
        return fecha.strftime("%d/%m/%Y %H:%M") if fecha else str(valor or "")

    @staticmethod
    def _obtener_identidad(id_usuario):
        identidad = usuarios_repo.obtener_identidad_chat(id_usuario)
        if not identidad:
            return None, "Usuario no encontrado", 404

        if not identidad.get("id_actividad"):
            return None, "El usuario no tiene una actividad de chat asociada", 400

        return identidad, None, None

    @staticmethod
    def _usuario_tiene_acceso(chat, identidad):
        if identidad.get("tipoUsuario") == "candidato":
            return int(chat.get("id_candidato")) == int(identidad.get("candidatoId"))

        if identidad.get("tipoUsuario") == "delegado":
            return int(chat.get("id_delegado")) == int(identidad.get("delegadoId"))

        return False

    @staticmethod
    def _ids_emisor_validos(identidad):
        return [int(identidad["Id"])]

    @staticmethod
    def _es_emisor_propio(mensaje, ids_emisor):
        try:
            return int(mensaje.get("id_emisor")) in ids_emisor
        except (TypeError, ValueError):
            return False

    @staticmethod
    def _nombres_participantes(chat):
        delegado = usuarios_repo.buscar_delegado_por_id(chat.get("id_delegado"))
        candidato = usuarios_repo.buscar_candidato_por_id(chat.get("id_candidato"))

        return {
            "delegado": delegado or {},
            "candidato": candidato or {},
            "nombre_delegado": (delegado or {}).get("nombre", "Delegado desconocido"),
            "nombre_candidato": (candidato or {}).get("nombre", "Candidato desconocido"),
        }

    @staticmethod
    def _nombre_emisor(mensaje, participantes):
        id_emisor = mensaje.get("id_emisor")

        try:
            id_emisor = int(id_emisor)
        except (TypeError, ValueError):
            return "Usuario desconocido"

        candidato = participantes["candidato"]
        delegado = participantes["delegado"]

        if id_emisor in {candidato.get("Id"), candidato.get("candidatoId")}:
            return participantes["nombre_candidato"]

        if id_emisor in {delegado.get("Id"), delegado.get("delegadoId")}:
            return participantes["nombre_delegado"]

        usuario = usuarios_repo.buscar_usuario_por_id(id_emisor)
        return usuario.get("nombre") if usuario else "Usuario desconocido"

    @staticmethod
    def obtener_chats_de_usuario(id_usuario):
        try:
            identidad, error, status = chat_service._obtener_identidad(id_usuario)
            if error:
                return None, error, status

            chats = chat_repositorio.obtener_chats_usuario(
                id_candidato=identidad.get("candidatoId"),
                id_delegado=identidad.get("delegadoId"),
            )

            resultado = []
            for chat in chats:
                participantes = chat_service._nombres_participantes(chat)
                fechas = [
                    chat_service._parse_fecha(mensaje.get("timestamp"))
                    for mensaje in chat.get("mensajes", [])
                ]
                fechas = [fecha for fecha in fechas if fecha]
                ultimo_mensaje = (chat.get("mensajes") or [{}])[-1]

                resultado.append({
                    "id_chat": chat.get("id_chat") or str(chat.get("_id")),
                    "delegado": participantes["nombre_delegado"],
                    "candidato": participantes["nombre_candidato"],
                    "fecha": max(fechas).strftime("%d/%m/%Y %H:%M") if fechas else "Sin mensajes",
                    "ultimo_mensaje": ultimo_mensaje.get("contenido", ""),
                })

            return resultado, None, 200
        except Exception as e:
            return None, f"Error al obtener chats: {str(e)}", 500

    @staticmethod
    def obtener_chat_detalle(id_usuario, id_chat):
        try:
            identidad, error, status = chat_service._obtener_identidad(id_usuario)
            if error:
                return None, error, status

            chat = chat_repositorio.ver_chat(id_chat)
            if not chat:
                return None, "Chat no encontrado", 404

            if not chat_service._usuario_tiene_acceso(chat, identidad):
                return None, "No tienes permiso para acceder a este chat", 403

            participantes = chat_service._nombres_participantes(chat)
            ids_emisor = set(chat_service._ids_emisor_validos(identidad))
            mensajes = []

            for mensaje in chat.get("mensajes", []):
                mensajes.append({
                    "id_mensaje": str(mensaje.get("id_mensaje")),
                    "emisor": chat_service._nombre_emisor(mensaje, participantes),
                    "contenido": mensaje.get("contenido", ""),
                    "timestamp": chat_service._formatear_fecha(mensaje.get("timestamp")),
                    "es_propio": chat_service._es_emisor_propio(mensaje, ids_emisor),
                })

            resultado = {
                "id_chat": chat.get("id_chat") or str(chat.get("_id")),
                "delegado": participantes["nombre_delegado"],
                "candidato": participantes["nombre_candidato"],
                "mensajes": mensajes,
            }

            return resultado, None, 200
        except Exception as e:
            return None, f"Error al obtener detalle del chat: {str(e)}", 500

    @staticmethod
    def crear_chat(id_usuario, id_delegado, id_candidato, mensaje_texto):
        try:
            identidad, error, status = chat_service._obtener_identidad(id_usuario)
            if error:
                return None, error, status

            id_delegado = int(id_delegado)
            id_candidato = int(id_candidato)

            if identidad.get("tipoUsuario") == "delegado" and identidad.get("delegadoId") != id_delegado:
                return None, "El delegado autenticado no corresponde al chat", 403

            if identidad.get("tipoUsuario") == "candidato" and identidad.get("candidatoId") != id_candidato:
                return None, "El candidato autenticado no corresponde al chat", 403

            if not usuarios_repo.buscar_delegado_por_id(id_delegado):
                return None, "Delegado no encontrado", 404

            if not usuarios_repo.buscar_candidato_por_id(id_candidato):
                return None, "Candidato no encontrado", 404

            if not mensaje_texto or not mensaje_texto.strip():
                return None, "El mensaje no puede estar vacio", 400

            nuevo_chat = chat_repositorio.crear_chat_con_mensaje(
                id_delegado,
                id_candidato,
                identidad["Id"],
                mensaje_texto.strip(),
            )

            if not nuevo_chat:
                return None, "Error al crear chat", 500

            return nuevo_chat, None, 201
        except Exception as e:
            return None, f"Error al crear chat: {str(e)}", 500

    @staticmethod
    def enviar_mensaje(id_chat, id_usuario, mensaje_texto):
        try:
            identidad, error, status = chat_service._obtener_identidad(id_usuario)
            if error:
                return None, error, status

            chat = chat_repositorio.ver_chat(id_chat)
            if not chat:
                return None, "Chat no encontrado", 404

            if not chat_service._usuario_tiene_acceso(chat, identidad):
                return None, "No tienes permiso para enviar mensajes en este chat", 403

            if not mensaje_texto or not mensaje_texto.strip():
                return None, "El mensaje no puede estar vacio", 400

            exito = chat_repositorio.enviar_mensaje(id_chat, identidad["Id"], mensaje_texto.strip())
            if not exito:
                return None, "Error al enviar el mensaje", 500

            return chat_repositorio.ver_chat(id_chat), None, 201
        except Exception as e:
            return None, f"Error al enviar mensaje: {str(e)}", 500

    @staticmethod
    def eliminar_mensaje(id_usuario, id_chat, id_mensaje):
        try:
            identidad, error, status = chat_service._obtener_identidad(id_usuario)
            if error:
                return None, error, status

            chat = chat_repositorio.ver_chat(id_chat)
            if not chat:
                return None, "Chat no encontrado", 404

            if not chat_service._usuario_tiene_acceso(chat, identidad):
                return None, "No tienes permiso para acceder a este chat", 403

            ids_emisor = chat_service._ids_emisor_validos(identidad)
            mensaje = None
            for item in chat.get("mensajes", []):
                if str(item.get("id_mensaje")) == str(id_mensaje):
                    mensaje = item
                    break

            if not mensaje:
                return None, "Mensaje no encontrado", 404

            if not chat_service._es_emisor_propio(mensaje, set(ids_emisor)):
                return None, "No puedes eliminar mensajes de otros usuarios", 403

            exito = chat_repositorio.eliminar_chat_mensaje(id_chat, id_mensaje, ids_emisor)
            if not exito:
                return None, "Error al eliminar el mensaje", 500

            return chat_repositorio.ver_chat(id_chat), None, 200
        except Exception as e:
            return None, f"Error al eliminar mensaje: {str(e)}", 500

    @staticmethod
    def eliminar_chat(id_usuario, id_chat):
        try:
            identidad, error, status = chat_service._obtener_identidad(id_usuario)
            if error:
                return None, error, status

            chat = chat_repositorio.ver_chat(id_chat)
            if not chat:
                return None, "Chat no encontrado", 404

            if not chat_service._usuario_tiene_acceso(chat, identidad):
                return None, "No tienes permiso para eliminar este chat", 403

            eliminado = chat_repositorio.eliminar_chat_db(id_chat)
            if not eliminado:
                return None, "Error al eliminar el chat", 500

            return {"id_chat": id_chat}, None, 200
        except Exception as e:
            return None, f"Error al eliminar chat: {str(e)}", 500
