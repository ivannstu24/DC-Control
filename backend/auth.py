from flask import Blueprint, request, jsonify, current_app
from db import get_db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
import psycopg2


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
    except psycopg2.Error as e:
        current_app.logger.error(f"Ошибка при логировании: {e}")
        db.rollback()
    except Exception as e:
        current_app.logger.error(f"Неожиданная ошибка: {e}")
        db.rollback()

def log_user_action(user_id, action_type, status, ip_address=None, user_agent=None):
    db = get_db()
    cursor = db.cursor()
    try:
        cursor.execute(
            """INSERT INTO user_auth 
            (user_id, action_type, ip_address, user_agent, status, timestamp) 
            VALUES (%s, %s, %s, %s, %s, %s)""",
            (user_id, action_type, ip_address, user_agent, status, datetime.utcnow())
        )
        db.commit()
    except Exception as e:
        current_app.logger.error(f"Ошибка при логировании действия пользователя: {e}")
        db.rollback()

@auth_bp.route('/register', methods=['POST', 'OPTIONS'])
def register():
    if request.method == "OPTIONS":
        return jsonify({"status": "ok"}), 200
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
    
    ip_address = request.remote_addr
    user_agent = request.headers.get('User-Agent')

    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT id, password_hash, role FROM users WHERE username = %s", (username,))
    user = cursor.fetchone()

    if not user:
        log_user_action(None, 'login', 'failed: user not found', ip_address, user_agent)
        return jsonify({'msg': 'Неверные учетные данные'}), 401

    user_id, password_hash, role = user
    
    if not check_password_hash(password_hash, password):
        log_user_action(user_id, 'login', 'failed: wrong password', ip_address, user_agent)
        return jsonify({'msg': 'Неверные учетные данные'}), 401

    access_token = create_access_token(identity={'id': user_id, 'role': role})
    
    log_user_action(user_id, 'login', 'success', ip_address, user_agent)

    return jsonify({
        'access_token': access_token,
        'user': {
            'id': user_id,
            'role': role,
            'username': username
        }
    }), 200

@auth_bp.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200
