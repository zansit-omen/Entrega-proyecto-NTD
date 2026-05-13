import sqlite3
import os
import sys

# --- PATH DEL PROYECTO ---
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

try:
    from jwt_middleware import hash_password
except ImportError:
    from Cross.jwt_middleware import hash_password


def setup_database():
    conn = None
    try:
        conn = sqlite3.connect("ProLink.db")
        cursor = conn.cursor()

        cursor.execute("PRAGMA foreign_keys = ON;")

        # =========================
        # TABLAS
        # =========================

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuario (
            Id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre VARCHAR(100),
            correo VARCHAR(50) UNIQUE NOT NULL,
            numero VARCHAR(10) NOT NULL,
            tipoUsuario VARCHAR(20),
            password TEXT NOT NULL
        );
        ''')

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS empresa (
            empresaId INTEGER PRIMARY KEY AUTOINCREMENT,
            razonSocial VARCHAR(100),
            correoContacto VARCHAR(50),
            direccion VARCHAR(50)
        );
        ''')

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS delegado (
            delegadoId INTEGER PRIMARY KEY AUTOINCREMENT,
            Id INTEGER NOT NULL,
            empresaId INTEGER,

            FOREIGN KEY (Id)
                REFERENCES usuario(Id)
                ON DELETE CASCADE,

            FOREIGN KEY (empresaId)
                REFERENCES empresa(empresaId)
                ON DELETE CASCADE
        );
        ''')

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS candidato (
            candidatoId INTEGER PRIMARY KEY AUTOINCREMENT,
            Id INTEGER NOT NULL,
            profesion VARCHAR(50),

            FOREIGN KEY (Id)
                REFERENCES usuario(Id)
                ON DELETE CASCADE
        );
        ''')

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS oferta (
            ofertaId INTEGER PRIMARY KEY AUTOINCREMENT,
            empresaId INTEGER NOT NULL,
            titulo VARCHAR(100) NOT NULL,
            descripcionOferta VARCHAR(500),
            profesionBuscar VARCHAR(50),
            estadoOferta INTEGER DEFAULT 1,

            FOREIGN KEY (empresaId)
                REFERENCES empresa(empresaId)
                ON DELETE CASCADE
        );
        ''')

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS postulacion (
            postulacionId INTEGER PRIMARY KEY AUTOINCREMENT,
            ofertaId INTEGER NOT NULL,
            candidatoId INTEGER NOT NULL,
            fechaPostulacion DATETIME DEFAULT CURRENT_TIMESTAMP,
            estadoPostulacion INTEGER DEFAULT 2,

            FOREIGN KEY (ofertaId)
                REFERENCES oferta(ofertaId)
                ON DELETE CASCADE,

            FOREIGN KEY (candidatoId)
                REFERENCES candidato(candidatoId)
                ON DELETE CASCADE
        );
        ''')

        # =========================
        # SEED
        # =========================
        seed_data(cursor)

        conn.commit()
        print("Base de datos inicializada correctamente.")

    except sqlite3.Error as e:
        print(f"Error al crear la base de datos: {e}")

    finally:
        if conn:
            conn.close()


def seed_data(cursor):
    # =========================
    # LIMPIEZA SEGURA
    # =========================
    tables = ["postulacion", "oferta", "candidato", "delegado", "empresa", "usuario"]

    for table in tables:
        cursor.execute(f"DELETE FROM {table}")

    cursor.execute("DELETE FROM sqlite_sequence")

    # =========================
    # USUARIOS
    # =========================

    cursor.execute('''
        INSERT INTO usuario (nombre, correo, numero, tipoUsuario, password)
        VALUES (?, ?, ?, ?, ?)
    ''', ("Juan Perez", "juan@mail.com", "3001111111", "candidato", hash_password("JuanPerez123")))
    juan_id = cursor.lastrowid

    cursor.execute('''
        INSERT INTO usuario (nombre, correo, numero, tipoUsuario, password)
        VALUES (?, ?, ?, ?, ?)
    ''', ("Maria Gomez", "maria@mail.com", "3002222222", "candidato", hash_password("MariaGomez123")))
    maria_id = cursor.lastrowid

    cursor.execute('''
        INSERT INTO usuario (nombre, correo, numero, tipoUsuario, password)
        VALUES (?, ?, ?, ?, ?)
    ''', ("Carlos Ruiz", "carlos@empresa.com", "3003333333", "delegado", hash_password("CarlosRuiz123")))
    carlos_id = cursor.lastrowid

    cursor.execute('''
        INSERT INTO usuario (nombre, correo, numero, tipoUsuario, password)
        VALUES (?, ?, ?, ?, ?)
    ''', ("Ana Torres", "ana@empresa.com", "3004444444", "delegado", hash_password("AnaTorres123")))
    ana_id = cursor.lastrowid

    # =========================
    # EMPRESAS
    # =========================

    cursor.execute('''
        INSERT INTO empresa (razonSocial, correoContacto, direccion)
        VALUES (?, ?, ?)
    ''', ("Tech Solutions SAS", "contacto@tech.com", "Bogotá"))
    tech_id = cursor.lastrowid

    cursor.execute('''
        INSERT INTO empresa (razonSocial, correoContacto, direccion)
        VALUES (?, ?, ?)
    ''', ("Innovatech Ltda", "info@innovatech.com", "Medellín"))
    innova_id = cursor.lastrowid

    # =========================
    # DELEGADOS
    # =========================

    cursor.execute("INSERT INTO delegado (Id, empresaId) VALUES (?, ?)", (carlos_id, tech_id))
    cursor.execute("INSERT INTO delegado (Id, empresaId) VALUES (?, ?)", (ana_id, innova_id))

    # =========================
    # CANDIDATOS
    # =========================

    cursor.execute("INSERT INTO candidato (Id, profesion) VALUES (?, ?)", (juan_id, "Ingeniero de Software"))
    juan_cand_id = cursor.lastrowid

    cursor.execute("INSERT INTO candidato (Id, profesion) VALUES (?, ?)", (maria_id, "Analista de Datos"))
    maria_cand_id = cursor.lastrowid

    # =========================
    # OFERTA
    # =========================

    cursor.execute('''
        INSERT INTO oferta (empresaId, titulo, descripcionOferta, profesionBuscar, estadoOferta)
        VALUES (?, ?, ?, ?, ?)
    ''', (tech_id, "Backend Developer", "Desarrollador backend con Python", "Ingeniero de Software", 1))
    oferta1_id = cursor.lastrowid

    # =========================
    # POSTULACION
    # =========================

    cursor.execute('''
        INSERT INTO postulacion (ofertaId, candidatoId, estadoPostulacion)
        VALUES (?, ?, ?)
    ''', (oferta1_id, juan_cand_id, 0))


if __name__ == "__main__":
    setup_database()