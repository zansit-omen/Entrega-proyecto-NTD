from Database.config import get_sqlite_connection

class delegado_repo:

    @staticmethod
    def get_db_connection():
        return get_sqlite_connection()

    @staticmethod
    def buscar_por_id(delegado_id):
        conn = delegado_repo.get_db_connection()
        row = conn.execute("""
            SELECT d.delegadoId, d.Id, d.empresaId, u.nombre, u.correo
            FROM delegado d JOIN usuario u ON d.Id = u.Id
            WHERE d.delegadoId = ?
        """, (delegado_id,)).fetchone()
        conn.close()
        return dict(row) if row else None

    @staticmethod
    def buscar_por_usuario_id(usuario_id):
        conn = delegado_repo.get_db_connection()
        row = conn.execute(
            '''SELECT usuario.nombre, empresa.razonSocial, delegado.empresaId FROM usuario JOIN delegado
                ON usuario.Id = delegado.Id JOIN empresa 
                ON delegado.empresaId = empresa.empresaId 
                WHERE delegado.Id = ?''', (usuario_id,)
        ).fetchone()
        conn.close()
        return dict(row) if row else None

    @staticmethod
    def obtener_empresa_id_por_usuario(usuario_id):
        """Obtiene el empresaId de un delegado basado en su usuario_id"""
        conn = delegado_repo.get_db_connection()
        row = conn.execute(
            "SELECT empresaId FROM delegado WHERE Id = ?", (usuario_id,)
        ).fetchone()
        conn.close()
        return row['empresaId'] if row else None

    @staticmethod
    def ya_es_delegado(usuario_id):
        conn = delegado_repo.get_db_connection()
        row = conn.execute(
            "SELECT * FROM delegado WHERE Id = ?", (usuario_id,)
        ).fetchone()
        conn.close()
        return row is not None

    @staticmethod
    def crear_delegado(usuario_id, empresa_id):
        conn = delegado_repo.get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO delegado (Id, empresaId) VALUES (?, ?)", (usuario_id, empresa_id)
        )
        delegado_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return delegado_id