
import sqlite3
import os
from functools import lru_cache
from dotenv import load_dotenv

# Cargar variables de entorno desde .env
load_dotenv()

SQLITE_DATABASE = os.getenv("SQLITE_DATABASE")


def get_sqlite_connection():
    conn = sqlite3.connect(SQLITE_DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def close_sqlite_connection(conn):
    if conn:
        conn.close()


class DatabaseConfig:
    
    USUARIO = "usuario"
    CANDIDATO = "candidato"
    DELEGADO = "delegado"
    EMPRESA = "empresa"
    OFERTA = "oferta"
    POSTULACION = "postulacion"
    