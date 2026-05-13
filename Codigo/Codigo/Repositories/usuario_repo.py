import sqlite3
from Database.config import get_sqlite_connection, close_sqlite_connection
from flask import request, jsonify
from Cross.jwt_middleware import JWTMiddleware


class usuarios_repo:
    @staticmethod
    def listar_delegados_disponibles_para_candidato(id_candidato):
        """Devuelve una lista de delegados con los que el candidato NO tiene chat."""
        conn = usuarios_repo.get_db_connection()
        conn.row_factory = sqlite3.Row
        # Obtener todos los delegados
        delegados = conn.execute("""
            SELECT d.delegadoId, u.Id, u.nombre, u.correo
            FROM delegado d
            JOIN usuario u ON d.Id = u.Id
        """).fetchall()
        # Obtener delegados con los que ya tiene chat
        from Repositories.chat_repositorio import chat_repositorio
        chats = chat_repositorio.obtener_chats_usuario(id_candidato=id_candidato)
        delegados_con_chat = {int(chat.get('id_delegado')) for chat in chats}
        # Filtrar delegados
        disponibles = [dict(row) for row in delegados if int(row['delegadoId']) not in delegados_con_chat]
        conn.close()
        return disponibles

    @staticmethod
    def listar_candidatos_disponibles_para_delegado(id_delegado):
        """Devuelve una lista de candidatos con los que el delegado NO tiene chat."""
        conn = usuarios_repo.get_db_connection()
        conn.row_factory = sqlite3.Row
        # Obtener todos los candidatos
        candidatos = conn.execute("""
            SELECT c.candidatoId, u.Id, u.nombre, u.correo, c.profesion
            FROM candidato c
            JOIN usuario u ON c.Id = u.Id
        """).fetchall()
        # Obtener candidatos con los que ya tiene chat
        from Repositories.chat_repositorio import chat_repositorio
        chats = chat_repositorio.obtener_chats_usuario(id_delegado=id_delegado)
        candidatos_con_chat = {int(chat.get('id_candidato')) for chat in chats}
        # Filtrar candidatos
        disponibles = [dict(row) for row in candidatos if int(row['candidatoId']) not in candidatos_con_chat]
        conn.close()
        return disponibles

    @staticmethod
    def get_db_connection():
        return get_sqlite_connection()


    @staticmethod
    def crear_user(nombre, correo, numero, tipo, password):
        from Cross.jwt_middleware import hash_password
        hashed_password = hash_password(password)
        conn = usuarios_repo.get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO usuario (nombre, correo, numero, tipoUsuario, password)
            VALUES (?, ?, ?, ?, ?)
            """,
            (nombre, correo, numero, tipo, hashed_password),
        )
        user_id = cursor.lastrowid
        conn.commit()
        new_user = cursor.execute(
            "SELECT Id, nombre, correo, numero, tipoUsuario FROM usuario WHERE Id = ?",
            (user_id,),
        ).fetchone()
        conn.close()
        return jsonify(dict(new_user)), 201

    @staticmethod
    def actualizar_user(id, nombre, correo, numero, tipo):  
        conn = usuarios_repo.get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            UPDATE usuario SET nombre = ?, correo = ?, numero = ?, tipoUsuario = ?
            WHERE Id = ?
            """,
            (nombre, correo, numero, tipo, id),
        )
        updated = cursor.execute(
            "SELECT Id, nombre, correo, numero, tipoUsuario FROM usuario WHERE Id = ?",
            (id,),
        ).fetchone()
        conn.commit()
        conn.close()
        return jsonify(dict(updated)), 200

    @staticmethod
    def actualizar_contra(id, password):
        conn = usuarios_repo.get_db_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE usuario SET password = ? WHERE Id = ?", (password, id))
        conn.commit()
        user = cursor.execute("SELECT Id, nombre, correo, numero, tipoUsuario FROM usuario WHERE Id = ?",(id,),).fetchone()
        conn.close()
        return jsonify(dict(user)), 200

    @staticmethod
    def borrar_user(id):
        conn = usuarios_repo.get_db_connection()
        cursor = conn.cursor()
        user = cursor.execute("SELECT Id, nombre, correo, numero, tipoUsuario FROM usuario WHERE Id = ?",(id,),).fetchone()
        user_dict = dict(user)
        cursor.execute("DELETE FROM usuario WHERE Id = ?", (id,))
        conn.commit()
        conn.close()

        return jsonify(user_dict), 200

    @staticmethod
    def Obtener_user(id):
        conn = usuarios_repo.get_db_connection()
        conn.row_factory = sqlite3.Row 
        usuario = conn.execute(
        "SELECT Id, nombre, correo, numero, tipoUsuario FROM usuario WHERE Id = ?",
        (id,)).fetchone()
        conn.close()
        return dict(usuario) if usuario else None

    @staticmethod
    def obtener_identidad_chat(id_usuario):
        """Devuelve el usuario SQL junto con su id de actividad para chat."""
        try:
            conn = usuarios_repo.get_db_connection()
            conn.row_factory = sqlite3.Row
            row = conn.execute("""
                SELECT
                    u.Id,
                    u.nombre,
                    u.correo,
                    u.numero,
                    u.tipoUsuario,
                    c.candidatoId,
                    d.delegadoId
                FROM usuario u
                LEFT JOIN candidato c ON u.Id = c.Id
                LEFT JOIN delegado d ON u.Id = d.Id
                WHERE u.Id = ?
            """, (id_usuario,)).fetchone()
            conn.close()

            if not row:
                return None

            identidad = dict(row)
            if identidad.get("tipoUsuario") == "candidato":
                identidad["id_actividad"] = identidad.get("candidatoId")
            elif identidad.get("tipoUsuario") == "delegado":
                identidad["id_actividad"] = identidad.get("delegadoId")
            else:
                identidad["id_actividad"] = None

            return identidad
        except Exception as e:
            print(f"Error obteniendo identidad de chat {id_usuario}: {e}")
            return None

    @staticmethod
    def buscar_usuario_por_id(id_usuario):
        """Busca un usuario por Id y retorna un diccionario plano."""
        try:
            conn = usuarios_repo.get_db_connection()
            conn.row_factory = sqlite3.Row
            row = conn.execute("""
                SELECT Id, nombre, correo, numero, tipoUsuario
                FROM usuario
                WHERE Id = ?
            """, (id_usuario,)).fetchone()
            conn.close()
            return dict(row) if row else None
        except Exception as e:
            print(f"Error buscando usuario {id_usuario}: {e}")
            return None
    
    @staticmethod
    def buscar_por_correo(correo):
        conn = usuarios_repo.get_db_connection()
        cursor = conn.cursor()
        user = cursor.execute("SELECT * FROM usuario WHERE correo = ?", (correo,)).fetchone()
        conn.close()
        return dict(user) if user else None
    
    @staticmethod
    def buscar_delegado_por_id(delegado_id):
        """Busca un delegado y retorna su información con nombre del usuario."""
        try:
            conn = usuarios_repo.get_db_connection()
            conn.row_factory = sqlite3.Row
            row = conn.execute("""
                SELECT u.Id, u.nombre, u.correo, d.delegadoId
                FROM usuario u
                JOIN delegado d ON u.Id = d.Id
                WHERE d.delegadoId = ?
            """, (delegado_id,)).fetchone()
            conn.close()
            return dict(row) if row else None
        except Exception as e:
            print(f"Error buscando delegado {delegado_id}: {e}")
            return None

    @staticmethod
    def buscar_candidato_por_id(candidato_id):
        """Busca un candidato y retorna su información con nombre del usuario."""
        try:
            conn = usuarios_repo.get_db_connection()
            conn.row_factory = sqlite3.Row
            row = conn.execute("""
                SELECT u.Id, u.nombre, u.correo, c.candidatoId, c.profesion
                FROM usuario u
                JOIN candidato c ON u.Id = c.Id
                WHERE c.candidatoId = ?
            """, (candidato_id,)).fetchone()
            conn.close()
            return dict(row) if row else None
        except Exception as e:
            print(f"Error buscando candidato {candidato_id}: {e}")
            return None
