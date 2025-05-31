from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask import Flask
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from config import Config
from db import close_db
from auth import auth_bp
from admin import admin_bp
from user import user_bp
from flask import Flask, request, jsonify
from datetime import timedelta


app = Flask(__name__)
app.config.from_object(Config)

app.config["JWT_TOKEN_LOCATION"] = ["headers"]
app.config["JWT_HEADER_NAME"] = "Authorization"
app.config["JWT_HEADER_TYPE"] = "Bearer"
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)

CORS(app, resources={
    r"/api/*": {
        "origins": "*",
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"],
        "supports_credentials": True,
        "expose_headers": ["Authorization"] 
    }
})

@app.before_request
def handle_options():
    if request.method == "OPTIONS":
        resp = jsonify({"status": "ok"})
        resp.headers['Access-Control-Max-Age'] = 3600
        return resp

jwt = JWTManager(app)

app.register_blueprint(auth_bp, url_prefix="/api/auth")
app.register_blueprint(admin_bp, url_prefix="/api/admin")
app.register_blueprint(user_bp, url_prefix="/api/user")

app.teardown_appcontext(close_db)

if __name__ == "__main__":
    app.run(debug=True)