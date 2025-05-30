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
app.config['JWT_TOKEN_LOCATION'] = ['cookies']
app.config['JWT_COOKIE_SECURE'] = False
app.config['JWT_COOKIE_CSRF_PROTECT'] = False 
app.config['JWT_SECRET_KEY'] = 'your-secret-key' 
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = False 

CORS(app, 
     supports_credentials=True,
     resources={
         r"/api/*": {
             "origins": ["http://localhost:8080", "http://127.0.0.1:8080"],
             "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
             "allow_headers": ["Content-Type", "Authorization"],
             "expose_headers": ["Content-Type"],
             "max_age": 86400
         }
     })

jwt = JWTManager(app)

app.register_blueprint(auth_bp, url_prefix="/api/auth")
app.register_blueprint(admin_bp, url_prefix="/api/admin")
app.register_blueprint(user_bp, url_prefix="/api/user")

app.teardown_appcontext(close_db)

if __name__ == "__main__":
    app.run(debug=True)