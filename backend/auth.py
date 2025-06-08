from flask import Blueprint, request, jsonify, session
from db import get_db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    role = data.get('role')
    
    if role not in ['admin', 'user']:
        return jsonify({'msg': 'Роль должна быть admin или user'}), 400

    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT id FROM users WHERE username = %s", (username,))
    if cursor.fetchone():
        return jsonify({'msg': 'Пользователь уже существует'}), 409

    password_hash = generate_password_hash(password)
    
    cursor.execute(
        "INSERT INTO users (username, password_hash, role) VALUES (%s, %s, %s) RETURNING id",
        (username, password_hash, role)
    )
    user_id = cursor.fetchone()[0]
    db.commit()

    return jsonify({'msg': 'Пользователь зарегистрирован'}), 200

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT id, password_hash, role FROM users WHERE username = %s", (username,))
    user = cursor.fetchone()

    if not user:
        return jsonify({'msg': 'Неверные учетные данные'}), 401

    user_id, password_hash, role = user
    
    if not check_password_hash(password_hash, password):
        return jsonify({'msg': 'Неверные учетные данные'}), 401

    session.clear()
    session['user_id'] = user_id
    session['user_role'] = role
    session.permanent = True

    return jsonify({
        'msg': 'Успешный вход',
        'user_id': user_id,
        'role': role
    }), 200

@auth_bp.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({'msg': 'Успешный выход'}), 200

@auth_bp.route('/check-auth', methods=['GET'])
def check_auth():
    if 'user_id' in session:
        return jsonify({
            'isAuthenticated': True,
            'user_id': session['user_id'],
            'role': session['user_role']
        }), 200
    return jsonify({'isAuthenticated': False}), 200