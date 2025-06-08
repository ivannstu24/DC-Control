from flask import Blueprint, request, jsonify, session
from datetime import datetime
from db import get_db

admin_bp = Blueprint('admin', __name__)

def log_admin_action(action, details, user_id=None):
    db = get_db()
    cur = db.cursor()
    try:
        cur.execute("""
            INSERT INTO admin_logs (action, details, user_id, action_time)
            VALUES (%s, %s, %s, NOW())
        """, (action, details, user_id))
        db.commit()
    except Exception as e:
        db.rollback()
        print(f"Failed to log admin action: {e}")

def check_admin_auth():
    if 'user_id' not in session or session.get('user_role') != 'admin':
        return False
    return True

@admin_bp.route('/employees', methods=['GET'])
def get_employees():
    if not check_admin_auth():
        return jsonify({"error": "Unauthorized"}), 401

    db = get_db()
    cur = db.cursor()

    try:
        cur.execute("SELECT id, username FROM users")
        employees = [{"id": row[0], "username": row[1]} for row in cur.fetchall()]
        return jsonify(employees)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@admin_bp.route('/servers', methods=['GET'])
def get_servers():
    if not check_admin_auth():
        return jsonify({"error": "Unauthorized"}), 401

    db = get_db()
    cur = db.cursor()

    try:
        cur.execute("""
            SELECT s.id, s.name, b.name as block 
            FROM servers s
            JOIN blocks b ON s.block_id = b.id
        """)
        servers = [{"id": row[0], "name": row[1], "block": row[2]} for row in cur.fetchall()]
        return jsonify(servers)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@admin_bp.route('/accesses', methods=['GET'])
def get_accesses():
    if not check_admin_auth():
        return jsonify({"error": "Unauthorized"}), 401

    db = get_db()
    cur = db.cursor()

    try:
        cur.execute("""
            SELECT sa.id, u.username, s.name, sa.granted_at, sa.valid_from, sa.valid_to 
            FROM server_access sa
            JOIN users u ON sa.employee_id = u.id
            JOIN servers s ON sa.server_id = s.id
        """)
        accesses = [{
            "id": row[0],
            "username": row[1],
            "server": row[2],
            "granted_at": row[3].strftime('%Y-%m-%d %H:%M:%S'),
            "valid_from": row[4].strftime('%Y-%m-%d %H:%M:%S') if row[4] else None,
            "valid_to": row[5].strftime('%Y-%m-%d %H:%M:%S') if row[5] else None
        } for row in cur.fetchall()]
        return jsonify(accesses)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@admin_bp.route('/grant-access', methods=['POST'])
def grant_access():
    if not check_admin_auth():
        return jsonify({"error": "Unauthorized"}), 401

    data = request.get_json()
    required_fields = ['employee_id', 'server_id', 'valid_from', 'valid_to']
    
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing required fields"}), 400

    db = get_db()
    cur = db.cursor()

    try:
        # Проверяем существование пользователя и сервера
        cur.execute("SELECT 1 FROM users WHERE id = %s", (data['employee_id'],))
        if not cur.fetchone():
            return jsonify({"error": "User not found"}), 404

        cur.execute("SELECT 1 FROM servers WHERE id = %s", (data['server_id'],))
        if not cur.fetchone():
            return jsonify({"error": "Server not found"}), 404

        # Проверяем, нет ли уже такого доступа
        cur.execute("""
            SELECT 1 FROM server_access 
            WHERE employee_id = %s AND server_id = %s
        """, (data['employee_id'], data['server_id']))
        
        if cur.fetchone():
            return jsonify({"error": "Access already exists"}), 400

        # Создаем новый доступ
        cur.execute("""
            INSERT INTO server_access 
            (employee_id, server_id, granted_at, valid_from, valid_to) 
            VALUES (%s, %s, NOW(), %s, %s)
            RETURNING id
        """, (data['employee_id'], data['server_id'], data['valid_from'], data['valid_to']))
        
        access_id = cur.fetchone()[0]
        db.commit()
        
        log_admin_action(
            "grant_access",
            f"Granted access to server {data['server_id']} for employee {data['employee_id']}",
            data['employee_id']
        )
        
        return jsonify({"message": "Access granted successfully", "access_id": access_id}), 200
    except Exception as e:
        db.rollback()
        return jsonify({"error": str(e)}), 500

@admin_bp.route('/revoke-access/<int:access_id>', methods=['DELETE'])
def revoke_access(access_id):
    if not check_admin_auth():
        return jsonify({"error": "Unauthorized"}), 401

    db = get_db()
    cur = db.cursor()

    try:
        cur.execute("""
            SELECT employee_id, server_id FROM server_access WHERE id = %s
        """, (access_id,))
        access = cur.fetchone()
        
        if not access:
            return jsonify({"error": "Access not found"}), 404

        employee_id, server_id = access

        cur.execute("DELETE FROM server_access WHERE id = %s", (access_id,))
        db.commit()
        
        log_admin_action(
            "revoke_access",
            f"Revoked access {access_id} (server {server_id} for employee {employee_id})",
            employee_id
        )
        
        return jsonify({"message": "Access revoked successfully"}), 200
    except Exception as e:
        db.rollback()
        return jsonify({"error": str(e)}), 500

@admin_bp.route('/access-requests', methods=['GET'])
def get_access_requests():
    if not check_admin_auth():
        return jsonify({"error": "Unauthorized"}), 401

    db = get_db()
    cur = db.cursor()

    try:
        cur.execute("""
            SELECT ar.id, u.username, s.name, ar.created_at 
            FROM access_requests ar
            JOIN users u ON ar.employee_id = u.id
            JOIN servers s ON ar.server_id = s.id
            WHERE ar.status = 'pending'
        """)
        requests = [{
            "id": row[0],
            "username": row[1],
            "server": row[2],
            "created_at": row[3].strftime('%Y-%m-%d %H:%M:%S')
        } for row in cur.fetchall()]
        return jsonify(requests)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@admin_bp.route('/approve-request/<int:request_id>', methods=['POST'])
def approve_request(request_id):
    if not check_admin_auth():
        return jsonify({"error": "Unauthorized"}), 401

    data = request.get_json()
    required_fields = ['valid_from', 'valid_to']
    
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing required fields"}), 400

    db = get_db()
    cur = db.cursor()

    try:
        cur.execute("""
            SELECT employee_id, server_id FROM access_requests 
            WHERE id = %s AND status = 'pending'
        """, (request_id,))
        req = cur.fetchone()
        
        if not req:
            return jsonify({"error": "Request not found or already processed"}), 404

        employee_id, server_id = req

        cur.execute("""
            SELECT 1 FROM server_access 
            WHERE employee_id = %s AND server_id = %s
        """, (employee_id, server_id))
        
        if cur.fetchone():
            return jsonify({"error": "Access already exists"}), 400

        cur.execute("""
            INSERT INTO server_access 
            (employee_id, server_id, granted_at, valid_from, valid_to) 
            VALUES (%s, %s, NOW(), %s, %s)
        """, (employee_id, server_id, data['valid_from'], data['valid_to']))

        cur.execute("""
            UPDATE access_requests 
            SET status = 'approved', processed_at = NOW() 
            WHERE id = %s
        """, (request_id,))

        db.commit()

        log_admin_action(
            "approve_request",
            f"Approved request {request_id} for server {server_id}, employee {employee_id}",
            employee_id
        )

        return jsonify({"message": "Request approved successfully"}), 200
    except Exception as e:
        db.rollback()
        return jsonify({"error": str(e)}), 500

@admin_bp.route('/reject-request/<int:request_id>', methods=['POST'])
def reject_request(request_id):
    if not check_admin_auth():
        return jsonify({"error": "Unauthorized"}), 401

    db = get_db()
    cur = db.cursor()

    try:
        cur.execute("""
            SELECT employee_id, server_id FROM access_requests 
            WHERE id = %s AND status = 'pending'
        """, (request_id,))
        req = cur.fetchone()
        
        if not req:
            return jsonify({"error": "Request not found or already processed"}), 404

        employee_id, server_id = req

        cur.execute("""
            UPDATE access_requests 
            SET status = 'rejected', processed_at = NOW() 
            WHERE id = %s
        """, (request_id,))

        db.commit()
        
        log_admin_action(
            "reject_request",
            f"Rejected request {request_id} for server {server_id}, employee {employee_id}",
            employee_id
        )
        
        return jsonify({"message": "Request rejected successfully"}), 200
    except Exception as e:
        db.rollback()
        return jsonify({"error": str(e)}), 500

@admin_bp.route('/blocks', methods=['GET'])
def get_blocks():
    if not check_admin_auth():
        return jsonify({"error": "Unauthorized"}), 401

    db = get_db()
    cur = db.cursor()

    try:
        cur.execute("SELECT id, name FROM blocks")
        blocks = [{"id": row[0], "name": row[1]} for row in cur.fetchall()]
        return jsonify(blocks)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@admin_bp.route('/add-block', methods=['POST'])
def add_block():
    if not check_admin_auth():
        return jsonify({"error": "Unauthorized"}), 401

    data = request.get_json()
    name = data.get('name')

    if not name:
        return jsonify({"error": "Block name is required"}), 400

    db = get_db()
    cur = db.cursor()

    try:
        cur.execute("""
            INSERT INTO blocks (name) 
            VALUES (%s) 
            RETURNING id
        """, (name,))
        
        block_id = cur.fetchone()[0]
        db.commit()
        
        log_admin_action("add_block", f"Added new block with ID {block_id}")
        
        return jsonify({
            "message": "Block added successfully",
            "block_id": block_id
        }), 201
    except Exception as e:
        db.rollback()
        return jsonify({"error": str(e)}), 500

@admin_bp.route('/add-server', methods=['POST'])
def add_server():
    if not check_admin_auth():
        return jsonify({"error": "Unauthorized"}), 401

    data = request.get_json()
    name = data.get('name')
    block_id = data.get('block_id')

    if not name or not block_id:
        return jsonify({"error": "Server name and block ID are required"}), 400

    db = get_db()
    cur = db.cursor()

    try:
        cur.execute("SELECT 1 FROM blocks WHERE id = %s", (block_id,))
        if not cur.fetchone():
            return jsonify({"error": "Block not found"}), 404

        cur.execute("""
            INSERT INTO servers (name, block_id) 
            VALUES (%s, %s) 
            RETURNING id
        """, (name, block_id))
        
        server_id = cur.fetchone()[0]
        db.commit()
        
        log_admin_action(
            "add_server",
            f"Added new server with ID {server_id} to block {block_id}"
        )
        
        return jsonify({
            "message": "Server added successfully",
            "server_id": server_id
        }), 201
    except Exception as e:
        db.rollback()
        return jsonify({"error": str(e)}), 500

@admin_bp.route('/delete-server/<int:server_id>', methods=['DELETE'])
def delete_server(server_id):
    if not check_admin_auth():
        return jsonify({"error": "Unauthorized"}), 401

    db = get_db()
    cur = db.cursor()

    try:
        cur.execute("""
            SELECT name, block_id FROM servers WHERE id = %s
        """, (server_id,))
        server = cur.fetchone()
        
        if not server:
            return jsonify({"error": "Server not found"}), 404

        server_name, block_id = server

        cur.execute("""
            SELECT 1 FROM server_access WHERE server_id = %s
        """, (server_id,))
        
        if cur.fetchone():
            return jsonify({
                "error": "Cannot delete server with active accesses"
            }), 400

        cur.execute("DELETE FROM servers WHERE id = %s", (server_id,))
        db.commit()
        
        log_admin_action(
            "delete_server",
            f"Deleted server {server_id} ({server_name}) from block {block_id}"
        )
        
        return jsonify({"message": "Server deleted successfully"}), 200
    except Exception as e:
        db.rollback()
        return jsonify({"error": str(e)}), 500

@admin_bp.route('/delete-block/<int:block_id>', methods=['DELETE'])
def delete_block(block_id):
    if not check_admin_auth():
        return jsonify({"error": "Unauthorized"}), 401

    db = get_db()
    cur = db.cursor()

    try:
        cur.execute("SELECT name FROM blocks WHERE id = %s", (block_id,))
        block = cur.fetchone()
        
        if not block:
            return jsonify({"error": "Block not found"}), 404

        block_name = block[0]

        cur.execute("SELECT 1 FROM servers WHERE block_id = %s", (block_id,))
        
        if cur.fetchone():
            return jsonify({
                "error": "Cannot delete block with servers"
            }), 400

        cur.execute("DELETE FROM blocks WHERE id = %s", (block_id,))
        db.commit()
        
        log_admin_action(
            "delete_block",
            f"Deleted block {block_id} ({block_name})"
        )
        
        return jsonify({"message": "Block deleted successfully"}), 200
    except Exception as e:
        db.rollback()
        return jsonify({"error": str(e)}), 500