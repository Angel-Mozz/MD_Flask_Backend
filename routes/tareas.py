from flask import Blueprint, request, jsonify
from config.db import get_db_connection
import os
from dotenv import load_dotenv

load_dotenv()

tareas_bp = Blueprint("tareas", __name__)


@tareas_bp.route("/", methods=["GET"])
def get():
    cursor = None

    try:
        cursor = get_db_connection()
        cursor.execute("SELECT * FROM tareas")
        tareas = cursor.fetchall()

        return jsonify({"tareas": tareas}), 200

    except Exception as e:
        return jsonify({"Error obteniendo tareas": str(e)}), 500

    finally:
        cursor.close()


@tareas_bp.route("/", methods=["POST"])
def create():
    cursor = None
    data = request.get_json()
    descripcion = data.get("descripcion")

    if not descripcion:
        return jsonify({"error": "Faltan datos"}), 400

    try:
        cursor = get_db_connection()
        cursor.execute("INSERT INTO tareas (descripcion) values (%s)", (descripcion,))
        cursor.connection.commit()
        tarea_id = cursor.lastrowid

        return jsonify({"Tarea creada con id": tarea_id}), 201

    except Exception as e:
        return jsonify({"Error creando tarea": str(e)}), 500

    finally:
        cursor.close()


@tareas_bp.route("/<int:id>", methods=["PUT"])
def update(id):
    cursor = None
    data = request.get_json()
    descripcion = data.get("descripcion")

    if not descripcion:
        return jsonify({"error": "Faltan datos"}), 400

    try:
        cursor = get_db_connection()
        cursor.execute(
            "UPDATE tareas SET descripcion = (%s) WHERE id_tarea = (%s)",
            (descripcion, id),
        )
        cursor.connection.commit()

        if cursor.rowcount == 0:
            return jsonify({"error": "Tarea no encontrada"}), 404

        return jsonify({"Tarea modificada con id": id}), 200

    except Exception as e:
        return jsonify({"Error actualizando tarea": str(e)}), 500

    finally:
        cursor.close()


@tareas_bp.route("/<int:id>", methods=["DELETE"])
def delete(id):
    cursor = None

    try:
        cursor = get_db_connection()
        cursor.execute("DELETE FROM tareas WHERE id_tarea = (%s)", (id,))
        cursor.connection.commit()

        if cursor.rowcount == 0:
            return jsonify({"error": "Tarea no encontrada"}), 404

        return jsonify({"Tarea eliminada con id": id}), 200

    except Exception as e:
        return jsonify({"Error eliminando tarea": str(e)}), 500

    finally:
        cursor.close()
