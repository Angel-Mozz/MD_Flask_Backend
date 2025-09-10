from flask import Blueprint, request, jsonify
from config.db import get_db_connection
import os
from dotenv import load_dotenv
from flask_jwt_extended import jwt_required, get_jwt_identity

load_dotenv()

tareas_bp = Blueprint("tareas", __name__)


@tareas_bp.route("/", methods=["GET"])
@jwt_required()
def get():
    cursor = None
    current_user = get_jwt_identity()
    try:
        cursor = get_db_connection()
        query = """
            SELECT a.id_usuario, a.descripcion, b.nombre, b.email, a.creado_en
            FROM tareas as a
            INNER JOIN usuarios as b on a.id_usuario = b.id_usuario
            WHERE a.id_usuario = %s    
            """
        cursor.execute(query, (current_user,))
        lista = cursor.fetchall()

        if not lista:
            return jsonify({"Error": "El usuario no tiene tareas"}), 404
        else:
            return jsonify({"lista": lista}), 200

    except Exception as e:
        return jsonify({"Error obteniendo tareas": str(e)}), 500

    finally:
        cursor.close()


@tareas_bp.route("/", methods=["POST"])
@jwt_required()
def create():
    cursor = None
    current_user = get_jwt_identity()
    data = request.get_json()
    descripcion = data.get("descripcion")

    if not descripcion:
        return jsonify({"error": "Faltan datos"}), 400

    try:
        cursor = get_db_connection()
        cursor.execute(
            "INSERT INTO tareas (descripcion, id_usuario) values (%s, %s)",
            (
                descripcion,
                current_user,
            ),
        )
        cursor.connection.commit()
        tarea_id = cursor.lastrowid

        return jsonify({"Tarea creada con id": tarea_id}), 201

    except Exception as e:
        return jsonify({"Error creando tarea": str(e)}), 500

    finally:
        cursor.close()


@tareas_bp.route("/<int:id>", methods=["PUT"])
@jwt_required()
def update(id):
    cursor = None
    data = request.get_json()
    descripcion = data.get("descripcion")
    current_user = get_jwt_identity()

    if not descripcion:
        return jsonify({"error": "Faltan datos"}), 400

    try:
        cursor = get_db_connection()
        cursor.execute(
            "UPDATE tareas SET descripcion = (%s) WHERE id_tarea = (%s) AND id_usuario = (%s)",
            (descripcion, id, current_user),
        )
        cursor.connection.commit()

        if cursor.rowcount == 0:
            return jsonify({"error": "Tarea no encontrada para ese usuario"}), 404

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
