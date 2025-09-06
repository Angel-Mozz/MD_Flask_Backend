from flask import Flask
import os
from dotenv import load_dotenv
from config.db import init_db

from routes.tareas import tareas_bp

from routes.usuarios import usuarios_bp

load_dotenv()


def create_app():
    app = Flask(__name__)
    init_db(app)
    app.register_blueprint(tareas_bp, url_prefix="/tareas")
    app.register_blueprint(usuarios_bp, url_prefix="/usuarios")

    return app


app = create_app()

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="127.0.0.1", port=port, debug=True)
