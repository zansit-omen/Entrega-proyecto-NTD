from Database.config import get_sqlite_connection

class postulacion_repo:

    @staticmethod
    def get_db_connection():
        return get_sqlite_connection()

    @staticmethod
    def buscar_por_id(postulacion_id):

        conn = postulacion_repo.get_db_connection()

        row = conn.execute("""
            SELECT 
                p.postulacionId,
                p.estadoPostulacion,
                o.titulo,
                e.razonSocial,
                u.nombre,
                u.Id,
                c.profesion
            FROM postulacion p
            JOIN candidato c 
                ON p.candidatoId = c.candidatoId
            JOIN usuario u 
                ON c.Id = u.Id
            JOIN oferta o 
                ON p.ofertaId = o.ofertaId
            JOIN empresa e 
                ON o.empresaId = e.empresaId
            WHERE p.postulacionId = ?
        """, (postulacion_id,)).fetchone()

        conn.close()

        return dict(row) if row else None


    @staticmethod
    def buscar_por_oferta(oferta_id):

        conn = postulacion_repo.get_db_connection()

        rows = conn.execute("""
            SELECT 
                p.postulacionId,
                u.nombre,
                u.Id,
                c.profesion,
                o.titulo,
                o.ofertaId,
                e.razonSocial,
                p.estadoPostulacion
            FROM postulacion p
            JOIN candidato c 
                ON p.candidatoId = c.candidatoId
            JOIN usuario u 
                ON c.Id = u.Id
            JOIN oferta o 
                ON p.ofertaId = o.ofertaId
            JOIN empresa e
                ON o.empresaId = e.empresaId
            WHERE o.ofertaId = ?
        """, (oferta_id,)).fetchall()

        conn.close()

        resultado = []

        for row in rows:

            estado = row["estadoPostulacion"]

            if estado == 1:
                estado_texto = "Aceptado"
            elif estado == 2:
                estado_texto = "Pendiente"
            else:
                estado_texto = "Rechazado"

            resultado.append({
                "postulacionId": row["postulacionId"],
                "nombre": row["nombre"],
                "profesion": row["profesion"],
                "titulo": row["titulo"],
                "razonSocial": row["razonSocial"],
                "estado": estado_texto
            })

        return resultado


    @staticmethod
    def buscar_por_candidato(candidato_id):

        conn = postulacion_repo.get_db_connection()

        rows = conn.execute("""
            SELECT 
                p.postulacionId,
                o.titulo,
                e.razonSocial,
                p.estadoPostulacion
            FROM postulacion p
            JOIN oferta o 
                ON p.ofertaId = o.ofertaId
            JOIN empresa e 
                ON o.empresaId = e.empresaId
            WHERE p.candidatoId = ?
        """, (candidato_id,)).fetchall()

        conn.close()

        resultado = []

        for row in rows:

            estado = row["estadoPostulacion"]

            if estado == 1:
                estado_texto = "Aceptado"
            elif estado == 2:
                estado_texto = "Pendiente"
            else:
                estado_texto = "Rechazado"

            resultado.append({
                "postulacionId": row["postulacionId"],
                "titulo": row["titulo"],
                "razonSocial": row["razonSocial"],
                "estado": estado_texto
            })

        return resultado


    @staticmethod
    def buscar_por_candidato_y_oferta(candidato_id, oferta_id):

        conn = postulacion_repo.get_db_connection()

        row = conn.execute("""
            SELECT postulacionId 
            FROM postulacion 
            WHERE candidatoId = ? 
            AND ofertaId = ?
        """, (candidato_id, oferta_id)).fetchone()

        conn.close()

        return row is not None


    @staticmethod
    def insertar(candidato_id, oferta_id):

        conn = postulacion_repo.get_db_connection()

        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO postulacion 
            (candidatoId, ofertaId, estadoPostulacion)
            VALUES (?, ?, 2)
        """, (candidato_id, oferta_id))

        postulacion_id = cursor.lastrowid

        conn.commit()
        conn.close()

        return postulacion_id


    @staticmethod
    def actualizar_estado(postulacion_id, estado):
        try:
            conn = postulacion_repo.get_db_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                UPDATE postulacion
                SET estadoPostulacion = ?
                WHERE postulacionId = ?
            """, (estado, postulacion_id))
            
            rows_affected = cursor.rowcount
            conn.commit()
            conn.close()
            
            return rows_affected > 0
        except Exception as e:
            print(f"Error actualizando estado de postulación: {e}")
            return False


    @staticmethod
    def eliminar(postulacion_id):
        try:
            conn = postulacion_repo.get_db_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                DELETE FROM postulacion
                WHERE postulacionId = ?
            """, (postulacion_id,))
            
            rows_affected = cursor.rowcount
            conn.commit()
            conn.close()
            
            return rows_affected > 0
        except Exception as e:
            print(f"Error eliminando postulación: {e}")
            return False