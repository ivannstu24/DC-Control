import os

class Config:
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'super-secret')
    DB_NAME = os.environ.get('DB_NAME', 'DCC')
    DB_USER = os.environ.get('DB_USER', 'ivanmerzov')
    DB_PASS = os.environ.get('DB_PASS', 'Vania_505')
    DB_HOST = os.environ.get('DB_HOST', 'localhost')
    DB_PORT = os.environ.get('DB_PORT', '5432')
