from flask import Blueprint, request, jsonify
import psycopg2
from datetime import datetime
from flask_cors import cross_origin
from db import get_db

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/employees', methods=['GET'])
@cross_origin()
def get_users():
    db = get_db()
    cur = db.cursor()

    cur.execute("""
        SELECT id, username FROM users
    """)
    users = cur.fetchall()
    return jsonify([{"id": user[0], "username": user[1]} for user in users])

@admin_bp.route('/servers', methods=['GET'])
@cross_origin()
def get_servers():
    db = get_db()
    cur = db.cursor()

    cur.execute("""
        SELECT s.id, s.name, b.name as block 
        FROM servers s
        JOIN blocks b ON s.block_id = b.id
    """)
    servers = cur.fetchall()
    return jsonify([{"id": server[0], "name": server[1], "block": server[2]} for server in servers])

@admin_bp.route('/accesses', methods=['GET'])
@cross_origin()
def get_accesses():
    db = get_db()
    cur = db.cursor()

    cur.execute("""
        SELECT sa.id, u.username, s.name, sa.granted_at, sa.valid_from, sa.valid_to 
        FROM server_access sa
        JOIN users u ON sa.employee_id = u.id
        JOIN servers s ON sa.server_id = s.id
    """)
    accesses = cur.fetchall()
    return jsonify([{
        "id": access[0],
        "username": access[1],
        "server": access[2],
        "granted_at": access[3].strftime('%Y-%m-%d %H:%M:%S'),
        "valid_from": access[4].strftime('%Y-%m-%d %H:%M:%S') if access[4] else None,
        "valid_to": access[5].strftime('%Y-%m-%d %H:%M:%S') if access[5] else None
    } for access in accesses])

@admin_bp.route('/grant-access', methods=['POST'])
@cross_origin()
def grant_access():
    data = request.json

    if not all(k in data for k in ('employee_id', 'server_id', 'valid_from', 'valid_to')):
        return jsonify({"error": "Missing required fields"}), 400

    employee_id = data['employee_id']
    server_id = data['server_id']
    valid_from = data['valid_from']
    valid_to = data['valid_to']

    db = get_db()
    cur = db.cursor()

    cur.execute("""
        SELECT 1 FROM server_access 
        WHERE employee_id = %s AND server_id = %s
    """, (employee_id, server_id))
    
    if cur.fetchone():
        return jsonify({"error": "Этот сотрудник уже имеет доступ к этому серверу"}), 400

    cur.execute("""
        INSERT INTO server_access (employee_id, server_id, granted_at, valid_from, valid_to) 
        VALUES (%s, %s, NOW(), %s, %s)
    """, (employee_id, server_id, valid_from, valid_to))
    
    db.commit()
    return jsonify({"message": "Доступ успешно выдан"})

@admin_bp.route('/revoke-access/<int:access_id>', methods=['DELETE'])
@cross_origin()
def revoke_access(access_id):
    db = get_db()
    cur = db.cursor()

    cur.execute("""
        DELETE FROM server_access WHERE id = %s
    """, (access_id,))

    db.commit()
    return jsonify({"message": "Доступ успешно отозван"})

@admin_bp.route('/access-requests', methods=['GET'])
@cross_origin()
def get_access_requests():
    db = get_db()
    cur = db.cursor()

    cur.execute("""
        SELECT ar.id, u.username, s.name, ar.created_at 
        FROM access_requests ar
        JOIN users u ON ar.employee_id = u.id
        JOIN servers s ON ar.server_id = s.id
        WHERE ar.status = 'pending'
    """)
    requests = cur.fetchall()
    return jsonify([{
        "id": req[0],
        "username": req[1],
        "server": req[2],
        "created_at": req[3].strftime('%Y-%m-%d %H:%M:%S')
    } for req in requests])

@admin_bp.route('/approve-request/<int:request_id>', methods=['POST'])
@cross_origin()
def approve_request(request_id):
    data = request.json
    
    if not all(k in data for k in ('valid_from', 'valid_to')):
        return jsonify({"error": "Необходимо указать даты начала и окончания доступа"}), 400

    valid_from = data['valid_from']
    valid_to = data['valid_to']

    db = get_db()
    cur = db.cursor()

    cur.execute("""
        SELECT employee_id, server_id FROM access_requests 
        WHERE id = %s
    """, (request_id,))
    req = cur.fetchone()
    if not req:
        return jsonify({"error": "Запрос не найден"}), 404

    employee_id, server_id = req

    cur.execute("""
        SELECT 1 FROM server_access 
        WHERE employee_id = %s AND server_id = %s
    """, (employee_id, server_id))
    if cur.fetchone():
        return jsonify({"error": "Доступ уже существует"}), 400

    cur.execute("""
        INSERT INTO server_access (employee_id, server_id, granted_at, valid_from, valid_to) 
        VALUES (%s, %s, NOW(), %s, %s)
    """, (employee_id, server_id, valid_from, valid_to))

    cur.execute("""
        UPDATE access_requests 
        SET status = 'approved' 
        WHERE id = %s
    """, (request_id,))

    db.commit()

    cur.execute("""
        SELECT s.name, b.name, sa.granted_at, sa.valid_from, sa.valid_to
        FROM server_access sa
        JOIN servers s ON sa.server_id = s.id
        JOIN blocks b ON s.block_id = b.id
        WHERE sa.employee_id = %s AND sa.server_id = %s
    """, (employee_id, server_id))
    access_data = cur.fetchone()

    return jsonify({
        "message": "Запрос одобрен",
        "access": {
            "server": access_data[0],
            "block": access_data[1],
            "granted_at": access_data[2].strftime('%Y-%m-%d %H:%M:%S'),
            "valid_from": access_data[3].strftime('%Y-%m-%d %H:%M:%S'),
            "valid_to": access_data[4].strftime('%Y-%m-%d %H:%M:%S')
        }
    })

@admin_bp.route('/reject-request/<int:request_id>', methods=['POST'])
@cross_origin()
def reject_request(request_id):
    db = get_db()
    cur = db.cursor()

    cur.execute("""
        UPDATE access_requests 
        SET status = 'rejected' 
        WHERE id = %s
    """, (request_id,))

    db.commit()
    return jsonify({"message": "Запрос отклонён"})

@admin_bp.route('/blocks', methods=['GET'])
@cross_origin()
def get_blocks():
    db = get_db()
    cur = db.cursor()

    cur.execute("SELECT id, name FROM blocks")
    blocks = cur.fetchall()
    return jsonify([{"id": block[0], "name": block[1]} for block in blocks])

@admin_bp.route('/add-block', methods=['POST'])
@cross_origin()
def add_block():
    data = request.json
    name = data.get('name')

    if not name:
        return jsonify({"error": "Необходимо указать название блока"}), 400

    db = get_db()
    cur = db.cursor()

    try:
        cur.execute("INSERT INTO blocks (name) VALUES (%s) RETURNING id", (name,))
        block_id = cur.fetchone()[0]
        db.commit()
        return jsonify({"message": "Блок успешно добавлен", "id": block_id})
    except Exception as e:
        db.rollback()
        return jsonify({"error": str(e)}), 500

@admin_bp.route('/add-server', methods=['POST'])
@cross_origin()
def add_server():
    data = request.json
    name = data.get('name')
    block_id = data.get('block_id')

    if not name or not block_id:
        return jsonify({"error": "Необходимо указать название сервера и ID блока"}), 400

    db = get_db()
    cur = db.cursor()

    try:
        cur.execute("SELECT 1 FROM blocks WHERE id = %s", (block_id,))
        if not cur.fetchone():
            return jsonify({"error": "Указанный блок не существует"}), 400

        cur.execute("""
            INSERT INTO servers (name, block_id) 
            VALUES (%s, %s) 
            RETURNING id
        """, (name, block_id))
        server_id = cur.fetchone()[0]
        db.commit()
        return jsonify({"message": "Сервер успешно добавлен", "id": server_id})
    except Exception as e:
        db.rollback()
        return jsonify({"error": str(e)}), 500

@admin_bp.route('/delete-server/<int:server_id>', methods=['DELETE'])
@cross_origin()
def delete_server(server_id):
    db = get_db()
    cur = db.cursor()

    try:
        cur.execute("SELECT 1 FROM server_access WHERE server_id = %s", (server_id,))
        if cur.fetchone():
            return jsonify({"error": "Невозможно удалить сервер: есть связанные доступы"}), 400

        cur.execute("DELETE FROM servers WHERE id = %s", (server_id,))
        db.commit()
        return jsonify({"message": "Сервер успешно удален"})
    except Exception as e:
        db.rollback()
        return jsonify({"error": str(e)}), 500

@admin_bp.route('/delete-block/<int:block_id>', methods=['DELETE'])
@cross_origin()
def delete_block(block_id):
    db = get_db()
    cur = db.cursor()

    try:
        cur.execute("SELECT 1 FROM servers WHERE block_id = %s", (block_id,))
        if cur.fetchone():
            return jsonify({"error": "Невозможно удалить блок: есть связанные серверы"}), 400

        cur.execute("DELETE FROM blocks WHERE id = %s", (block_id,))
        db.commit()
        return jsonify({"message": "Блок успешно удален"})
    except Exception as e:
        db.rollback()
        return jsonify({"error": str(e)}), 500