from Database.config import get_sqlite_connection

class candidato_repo:

    @staticmethod
    def get_db_connection():
        return get_sqlite_connection()

    @staticmethod
    def buscar_por_id(candidato_id):
        conn = candidato_repo.get_db_connection()
        row = conn.execute("""
            SELECT c.candidatoId, c.Id, c.profesion, u.nombre, u.correo
            FROM candidato c JOIN usuario u ON c.Id = u.Id
            WHERE c.Id = ?
        """, (candidato_id,)).fetchone()
        conn.close()
        return dict(row) if row else None

    @staticmethod
    def buscar_por_usuario_id(usuario_id):
        conn = candidato_repo.get_db_connection()
        row = conn.execute("""
            SELECT 
                c.candidatoId,
                c.Id,
                c.profesion,
                u.nombre,
                u.correo
            FROM candidato c
            JOIN usuario u ON c.Id = u.Id
            WHERE c.Id = ?
        """, (usuario_id,)).fetchone()
        conn.close()
        return dict(row) if row else None

    @staticmethod
    def ya_es_candidato(usuario_id):
        conn = candidato_repo.get_db_connection()
        row = conn.execute(
            "SELECT candidatoId FROM candidato WHERE Id = ?", (usuario_id,)
        ).fetchone()
        conn.close()
        return row is not None

    @staticmethod
    def crear_candidato(usuario_id, profesion):
        conn = candidato_repo.get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO candidato (Id, profesion) VALUES (?, ?)", (usuario_id, profesion)
        )
        candidato_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return candidato_id