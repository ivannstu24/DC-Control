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

CORS(app)
JWTManager(app)


app.register_blueprint(auth_bp, url_prefix="/api/auth")
app.register_blueprint(admin_bp, url_prefix="/api/admin")
app.register_blueprint(user_bp, url_prefix="/api/user")

app.teardown_appcontext(close_db)

if __name__ == "__main__":
    app.run(debug=True)
