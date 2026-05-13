from Database.config import get_sqlite_connection

class empresa_repo:

    @staticmethod
    def get_db_connection():
        return get_sqlite_connection()

    @staticmethod
    def buscar_por_id(empresa_id):
        conn = empresa_repo.get_db_connection()
        row = conn.execute(
            "SELECT * FROM empresa WHERE empresaId = ?", (empresa_id,)
        ).fetchone()
        conn.close()
        return dict(row) if row else None
    
    @staticmethod
    def buscar_por_razon_social(razon_social):
        conn = empresa_repo.get_db_connection()
        row = conn.execute(
            "SELECT * FROM empresa WHERE razonSocial = ?", (razon_social,)
        ).fetchone()
        conn.close()
        return dict(row) if row else None

    @staticmethod
    def crear_empresa(razon_social, correo_contacto, direccion):
        conn = empresa_repo.get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO empresa (razonSocial, correoContacto, direccion)
            VALUES (?, ?, ?)
        """, (razon_social, correo_contacto, direccion))
        empresa_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return empresa_id

    @staticmethod
    def actualizar_empresa(empresa_id, razon_social, correo_contacto, direccion):
        conn = empresa_repo.get_db_connection()
        conn.execute("""
            UPDATE empresa SET razonSocial = ?, correoContacto = ?, direccion = ?
            WHERE empresaId = ?
        """, (razon_social, correo_contacto, direccion, empresa_id))
        conn.commit()
        conn.close()

    @staticmethod
    def eliminar_empresa(empresa_id):
        conn = empresa_repo.get_db_connection()
        conn.execute("DELETE FROM empresa WHERE empresaId = ?", (empresa_id,))
        conn.commit()
        conn.close()