from flask import Flask
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from config import Config
from db import close_db
from auth import auth_bp
from admin import admin_bp
from user import user_bp

app = Flask(__name__)
app.config.from_object(Config)
app.config['SECRET_KEY'] = 'your-secret-key-here' 
app.config['SESSION_COOKIE_SECURE'] = False
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax' 
app.config['PERMANENT_SESSION_LIFETIME'] = 3600 

CORS(app,
    supports_credentials=True,
    resources={
        r"/api/*": {
            "origins": ["http://localhost:*", "http://127.0.0.1:*"],
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"],
            "expose_headers": ["Content-Type"]
        }
    })

app.register_blueprint(auth_bp, url_prefix="/api/auth")
app.register_blueprint(admin_bp, url_prefix="/api/admin")
app.register_blueprint(user_bp, url_prefix="/api/user")

app.teardown_appcontext(close_db)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)