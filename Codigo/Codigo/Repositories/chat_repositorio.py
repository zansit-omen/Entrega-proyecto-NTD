from datetime import datetime
from bson import ObjectId
from Database.config import get_sqlite_connection
from Database.mongo_db import chats

class chat_repositorio:

    @staticmethod
    def get_db_connection():
        return get_sqlite_connection()

    @staticmethod
    def get_mongo_db():
        return chats

    @staticmethod
    def _id_chat_query(id_chat):
        try:
            return {"id_chat": int(id_chat)}
        except (TypeError, ValueError):
            if ObjectId.is_valid(str(id_chat)):
                return {"_id": ObjectId(str(id_chat))}
            return {"id_chat": id_chat}

    @staticmethod
    def obtener_chats_usuario(id_candidato=None, id_delegado=None):
        try:
            chats_collection = chat_repositorio.get_mongo_db()
            filtros = []

            if id_candidato is not None:
                filtros.append({"id_candidato": int(id_candidato)})

            if id_delegado is not None:
                filtros.append({"id_delegado": int(id_delegado)})

            if not filtros:
                return []

            query = filtros[0] if len(filtros) == 1 else {"$or": filtros}
            chats_cursor = chats_collection.find(query).sort("id_chat", 1)
            return list(chats_cursor)
        except Exception as e:
            print(f"Error obtener chats del usuario: {e}")
            return []

    @staticmethod
    def ver_chat(id_chat):
        try:
            chats_collection = chat_repositorio.get_mongo_db()
            return chats_collection.find_one(chat_repositorio._id_chat_query(id_chat))
        except Exception as e:
            print(f"Error obtener chat: {e}")
            return None

    @staticmethod
    def enviar_mensaje(id_chat, id_usuario, contenido):
        try:
            query = chat_repositorio._id_chat_query(id_chat)
            id_usuario = int(id_usuario)
            chats_collection = chat_repositorio.get_mongo_db()
            
            chat = chats_collection.find_one(query)
            if not chat:
                return False
                
            nuevo_id = 1
            if chat.get("mensajes"):
                ids = []
                for mensaje in chat["mensajes"]:
                    try:
                        ids.append(int(mensaje.get("id_mensaje", 0)))
                    except (TypeError, ValueError):
                        continue
                nuevo_id = (max(ids) + 1) if ids else 1
            
            mensaje = {
                "id_mensaje": nuevo_id,
                "id_emisor": id_usuario,
                "contenido": contenido,
                "timestamp": datetime.now().isoformat(),
            }
            
            result = chats_collection.update_one(
                query,
                {"$push": {"mensajes": mensaje}}
            )
            
            return result.modified_count > 0
        except Exception as e:
            print(f"Error enviar mensaje: {e}")
            return False

    @staticmethod
    def crear_chat_con_mensaje(id_delegado, id_candidato, id_emisor, mensaje_texto):
        try:
            id_delegado = int(id_delegado)
            id_candidato = int(id_candidato)
            id_emisor = int(id_emisor)
            chats_collection = chat_repositorio.get_mongo_db()
            
            ultimo_chat = chats_collection.find_one(sort=[("id_chat", -1)])
            nuevo_id_chat = (ultimo_chat["id_chat"] + 1) if ultimo_chat else 1
            
            nuevo_chat = {
                "id_chat": nuevo_id_chat,
                "id_delegado": id_delegado,
                "id_candidato": id_candidato,
                "mensajes": [
                    {
                        "id_mensaje": 1,
                        "id_emisor": id_emisor,
                        "contenido": mensaje_texto,
                        "timestamp": datetime.now().isoformat(),
                    }
                ],
            }
            
            result = chats_collection.insert_one(nuevo_chat)
            nuevo_chat["_id"] = result.inserted_id
            return nuevo_chat
        except Exception as e:
            print(f"Error crear chat: {e}")
            return None

    @staticmethod
    def eliminar_chat_mensaje(id_chat, id_mensaje, ids_emisor):
        try:
            query = chat_repositorio._id_chat_query(id_chat)
            id_mensaje = int(id_mensaje)
            ids_emisor = [int(id_emisor) for id_emisor in ids_emisor]
            chats_collection = chat_repositorio.get_mongo_db()
            
            result = chats_collection.update_one(
                query,
                {
                    "$pull": {
                        "mensajes": {
                            "id_mensaje": id_mensaje,
                            "id_emisor": {"$in": ids_emisor}
                        }
                    }
                }
            )
            
            return result.modified_count > 0
        except Exception as e:
            print(f"Error eliminar mensaje: {e}")
            return False

    @staticmethod
    def eliminar_chat_db(id_chat):
        try:
            chats_collection = chat_repositorio.get_mongo_db()
            
            result = chats_collection.delete_one(chat_repositorio._id_chat_query(id_chat))
            return result.deleted_count > 0
        except Exception as e:
            print(f"Error eliminar chat: {e}")
            return False

    @staticmethod
    def editar_mensaje(id_chat, id_usuario, id_mensaje, nuevo_contenido):
        try:
            query = chat_repositorio._id_chat_query(id_chat)
            id_usuario = int(id_usuario)
            id_mensaje = int(id_mensaje)
            chats_collection = chat_repositorio.get_mongo_db()
            query.update({
                "mensajes.id_mensaje": id_mensaje,
                "mensajes.id_emisor": id_usuario
            })
            
            result = chats_collection.update_one(
                query,
                {"$set": {"mensajes.$.contenido": nuevo_contenido}}
            )
            
            return result.modified_count > 0
        except Exception as e:
            print(f"Error editar mensaje: {e}")
            return False
