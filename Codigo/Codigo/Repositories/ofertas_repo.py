from Database.config import get_sqlite_connection

class oferta_repo:

    @staticmethod
    def get_db_connection():
        return get_sqlite_connection()

    @staticmethod
    def obtener_todas():
        conn = oferta_repo.get_db_connection()
        rows = conn.execute("SELECT * FROM oferta").fetchall()
        conn.close()
        return [dict(r) for r in rows]

    @staticmethod
    def obtener_por_empresa(empresa_id):
        conn = oferta_repo.get_db_connection()
        rows = conn.execute(
            "SELECT * FROM oferta WHERE empresaId = ?", (empresa_id,)
        ).fetchall()
        conn.close()
        return [dict(r) for r in rows]

    @staticmethod
    def buscar_por_id(oferta_id):
        conn = oferta_repo.get_db_connection()
        row = conn.execute(
            "SELECT * FROM oferta WHERE ofertaId = ?", (oferta_id,)
        ).fetchone()
        conn.close()
        return dict(row) if row else None

    @staticmethod
    def insertar(empresa_id, titulo, descripcion, profesion):
        conn = oferta_repo.get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO oferta (empresaId, titulo, descripcionOferta, profesionBuscar)
            VALUES (?, ?, ?, ?)
        """, (empresa_id, titulo, descripcion, profesion))
        oferta_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return oferta_id

    @staticmethod
    def actualizar(oferta_id, titulo, descripcion, profesion, estado):
        conn = oferta_repo.get_db_connection()
        conn.execute("""
            UPDATE oferta
            SET titulo = ?, descripcionOferta = ?, profesionBuscar = ?, estadoOferta = ?
            WHERE ofertaId = ?
        """, (titulo, descripcion, profesion, estado, oferta_id))
        conn.commit()
        conn.close()

    @staticmethod
    def eliminar(oferta_id):
        conn = oferta_repo.get_db_connection()
        conn.execute("DELETE FROM oferta WHERE ofertaId = ?", (oferta_id,))
        conn.commit()
        conn.close()






