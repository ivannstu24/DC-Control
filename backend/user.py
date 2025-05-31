from flask import Blueprint, jsonify, request
from db import get_db
from datetime import datetime
from flask_jwt_extended import jwt_required, get_jwt_identity

user_bp = Blueprint('user_bp_unique', __name__, url_prefix='/api/user')

@user_bp.route('/servers/<int:user_id>', methods=['GET'])
@jwt_required()
def get_servers(user_id):
    current_user = get_jwt_identity()
    if current_user['id'] != user_id and current_user['role'] != 'admin':
        return jsonify({"error": "Доступ запрещен"}), 403

    conn = get_db()
    cur = conn.cursor()

    cur.execute("SELECT username FROM users WHERE id = %s", (user_id,))
    username = cur.fetchone()[0]

    cur.execute("""
        SELECT servers.id, servers.name, blocks.name AS block_name
        FROM servers
        JOIN blocks ON servers.block_id = blocks.id
    """)
    servers = [
        {"id": row[0], "name": row[1], "block": row[2]} 
        for row in cur.fetchall()
    ]

    cur.execute("""
        SELECT sa.server_id, s.name, b.name, sa.granted_at, sa.valid_from, sa.valid_to
        FROM server_access sa
        JOIN servers s ON sa.server_id = s.id
        JOIN blocks b ON s.block_id = b.id
        WHERE sa.employee_id = %s AND (sa.valid_to IS NULL OR sa.valid_to > NOW())
    """, (user_id,))
    accesses = [
        {
            "server_id": row[0], 
            "server": row[1], 
            "block": row[2], 
            "granted_at": row[3].strftime('%Y-%m-%d %H:%M:%S'),
            "valid_from": row[4].strftime('%Y-%m-%d %H:%M:%S') if row[4] else None,
            "valid_to": row[5].strftime('%Y-%m-%d %H:%M:%S') if row[5] else None
        } 
        for row in cur.fetchall()
    ]

    cur.execute("""
        SELECT server_id, status 
        FROM server_statuses 
        WHERE user_id = %s
    """, (user_id,))
    statuses = {row[0]: row[1] for row in cur.fetchall()}

    return jsonify({
        "username": username,
        "servers": servers,
        "accesses": accesses,
        "statuses": statuses
    })

@user_bp.route('/request-access', methods=['POST'])
@jwt_required()
def request_access():
    current_user = get_jwt_identity()
    if current_user['id'] != user_id and current_user['role'] != 'admin':
        return jsonify({"error": "Доступ запрещен"}), 403

    data = request.get_json()
    print("Полученные данные:", data)
    
    employee_id = data.get('employee_id')
    server_id = data.get('server_id')

    if not employee_id or not server_id:
        print("Ошибка: отсутствуют обязательные поля")
        return jsonify({"error": "Требуются employee_id и server_id"}), 400

    conn = get_db()
    cur = conn.cursor()

    cur.execute("SELECT 1 FROM users WHERE id = %s", (employee_id,))
    if not cur.fetchone():
        return jsonify({"error": "Пользователь не найден"}), 404

    cur.execute("SELECT 1 FROM servers WHERE id = %s", (server_id,))
    if not cur.fetchone():
        return jsonify({"error": "Сервер не найден"}), 404

    cur.execute("""
        SELECT id FROM access_requests 
        WHERE employee_id = %s AND server_id = %s AND status = 'pending'
    """, (employee_id, server_id))
    
    if cur.fetchone():
        return jsonify({"error": "Запрос уже существует"}), 400

    cur.execute("""
        INSERT INTO access_requests (employee_id, server_id, status, created_at)
        VALUES (%s, %s, 'pending', %s)
    """, (employee_id, server_id, datetime.utcnow()))
    
    conn.commit()
    return jsonify({"message": "Запрос создан", "request_id": cur.lastrowid}), 200

@user_bp.route('/update-server-status', methods=['POST'])
@jwt_required()
def update_server_status():
    current_user = get_jwt_identity()
    if current_user['id'] != user_id and current_user['role'] != 'admin':
        return jsonify({"error": "Доступ запрещен"}), 403

    data = request.get_json()
    user_id = data.get('user_id')
    server_id = data.get('server_id')
    status = data.get('status')

    if not all([user_id, server_id, status]):
        return jsonify({"error": "Необходимы user_id, server_id и status"}), 400

    if status not in ['running', 'paused', 'stopped', 'restarting']:
        return jsonify({"error": "Недопустимый статус сервера"}), 400

    conn = get_db()
    cur = conn.cursor()

    try:
        cur.execute("""
            SELECT 1 FROM server_access 
            WHERE employee_id = %s AND server_id = %s 
            AND (valid_to IS NULL OR valid_to > NOW())
        """, (user_id, server_id))
        
        if not cur.fetchone():
            return jsonify({"error": "У пользователя нет активного доступа к этому серверу"}), 403

        cur.execute("""
            INSERT INTO server_statuses (server_id, user_id, status)
            VALUES (%s, %s, %s)
            ON CONFLICT (server_id, user_id) 
            DO UPDATE SET status = EXCLUDED.status, last_updated = CURRENT_TIMESTAMP
            RETURNING status
        """, (server_id, user_id, status))
        
        new_status = cur.fetchone()[0]
        conn.commit()
        
        return jsonify({
            "message": "Статус сервера обновлен",
            "server_id": server_id,
            "status": new_status
        }), 200
        
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500