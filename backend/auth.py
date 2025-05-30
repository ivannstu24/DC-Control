from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import create_access_token, set_access_cookies, jwt_required, get_jwt_identity
from db import get_db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')

def log_user_action(user_id, action_type, status, ip_address=None, user_agent=None):
    db = get_db()
    cursor = db.cursor()
    try:
        cursor.execute("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE table_name = 'user_auth'
            )
        """)
        table_exists = cursor.fetchone()[0]
        
        if not table_exists:
            current_app.logger.error("Таблица user_auth не существует!")
            return

        cursor.execute(
            """INSERT INTO user_auth 
            (user_id, action_type, ip_address, user_agent, status, timestamp) 
            VALUES (%s, %s, %s, %s, %s, %s)""",
            (user_id, action_type, ip_address, user_agent, status, datetime.utcnow())
        )
        db.commit()
        current_app.logger.info(f"Успешно записано действие {action_type} для пользователя {user_id}")
    except Exception as e:
        current_app.logger.error(f"Ошибка при логировании: {e}")
        db.rollback()

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    role = data.get('role')
    
    ip_address = request.remote_addr
    user_agent = request.headers.get('User-Agent')

    if role not in ['admin', 'user']:
        log_user_action(None, 'register', 'failed: invalid role', ip_address, user_agent)
        return jsonify({'msg': 'Роль должна быть admin или user'}), 400

    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT id FROM users WHERE username = %s", (username,))
    if cursor.fetchone():
        log_user_action(None, 'register', 'failed: user exists', ip_address, user_agent)
        return jsonify({'msg': 'Пользователь уже существует'}), 409

    password_hash = generate_password_hash(password)
    
    cursor.execute(
        "INSERT INTO users (username, password_hash, role) VALUES (%s, %s, %s) RETURNING id",
        (username, password_hash, role)
    )
    user_id = cursor.fetchone()[0]
    db.commit()

    log_user_action(user_id, 'register', 'success', ip_address, user_agent)

    return jsonify({'msg': 'Пользователь зарегистрирован'}), 200

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    if not username or not password:
        return jsonify({'msg': 'Необходимо указать логин и пароль'}), 400

    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT id, password_hash, role FROM users WHERE username = %s", (username,))
    user = cursor.fetchone()

    if not user:
        return jsonify({'msg': 'Неверные учетные данные'}), 401

    user_id, password_hash, role = user
    
    if not check_password_hash(password_hash, password):
        return jsonify({'msg': 'Неверные учетные данные'}), 401

    access_token = create_access_token(identity={
        'id': user_id,
        'role': role,
        'username': username
    })
    
    response = jsonify({
        'id': user_id,
        'role': role,
        'username': username,
        'msg': 'Успешный вход'
    })
    
    set_access_cookies(response, access_token)
    return response, 200

@auth_bp.route('/logout', methods=['POST'])
def logout():
    response = jsonify({'msg': 'Успешный выход из системы'})
    response.delete_cookie('access_token_cookie')
    return response, 200

@auth_bp.route('/check-auth', methods=['GET'])
@jwt_required()
def check_auth():
    current_user = get_jwt_identity()
    return jsonify(current_user), 200