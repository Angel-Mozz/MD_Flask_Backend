from flask_mysqldb import MySQL
import os
from dotenv import load_dotenv

load_dotenv()

mysql = MySQL()


def init_db(app):
    app.config["MYSQL_HOST"] = os.getenv("DB_HOST", "127.0.0.1")
    app.config["MYSQL_PORT"] = int(os.getenv("DB_PORT", "3306"))
    app.config["MYSQL_USER"] = os.getenv("DB_USER")
    app.config["MYSQL_PASSWORD"] = os.getenv("DB_PASSWORD")
    app.config["MYSQL_DB"] = os.getenv("DB_NAME")

    mysql.init_app(app)


def get_db_connection():
    try:
        connection = mysql.connection
        return connection.cursor()

    except Exception as e:
        raise RuntimeError(f"Error al conectar a la base de datos: {e}")
