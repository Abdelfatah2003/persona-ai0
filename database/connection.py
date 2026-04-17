from pymongo import MongoClient
import os
from flask import current_app

_client = None
_db = None

def get_client():
    global _client
    if _client is None:
        try:
            mongo_uri = current_app.config.get('MONGO_URI', 'mongodb://localhost:27017/')
        except RuntimeError:
            mongo_uri = os.environ.get('MONGO_URI', 'mongodb://localhost:27017/')
        _client = MongoClient(mongo_uri)
    return _client

def get_db():
    global _db
    if _db is None:
        client = get_client()
        try:
            db_name = current_app.config.get('MONGO_DB_NAME', 'persona_ai')
        except RuntimeError:
            db_name = os.environ.get('MONGO_DB_NAME', 'persona_ai')
        _db = client[db_name]
    return _db

def init_db():
    db = get_db()
    
    db.users.create_index('email', unique=True)
    db.personalities.create_index('user_id')
    db.recommendations.create_index('user_id')
    
    print("Database initialized successfully")

def close_db():
    global _client, _db
    if _client:
        _client.close()
        _client = None
        _db = None
