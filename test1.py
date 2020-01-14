from flask import Flask,jsonify, request, current_app
from flask.json import JSONEncoder
from sqlalchemy import create_engine,text

class CustomJSONEncoder(JSONEncoder):
    def default(self,obj):
        if isinstance(obj):
            return list(obj)
        return JSONEncoder.default(self,obj)

def get_user(user_id):
    user = current_app.database.execute(text("""
        SELECT
            id,
            name,
            email,
            profile,
        FROM users
        WHERE id = :user_id
        """),{
            'user_id':user_id
            }).fetchone()
    return {
            'id':user['id'],
            'name':user['name'],
            'email':user['email'],
            'profile':user['profile']
            } if user else None

def insert_user(user):
    return current_app.database.execute(text("""
        INSERT INTO (
            name,
            email,
            profile,
            hashed_password
        ) VALUES(
            :name,
            :email,
            :profile,
            :password
        )
        """),user).lastrowid

def create_app(test_config=None):
    app=Flask(__name__)
    
    app.json_encoder = CustomJSONEncoder

    if test_config is None:
        app.config.from_pyfile("config.py")
    else:
        app.config.update("test_config")

    database = create_engine(app.config['DB_URL'], encoding='utf-8',max_overflow=0)
    app.database = database
    
    @app.route("/sign-up",methods=['POST'])
    def sign_up():
        new_user        = request.json
        new_user_id     = app.database.execute(text("""
                INSERT INTO users(
                    name,
                    email,
                    profile,
                    hashed_password
                    ) VALUES(
                        :name,
                        :email,
                        :profile,
                        :password
                    )
                    """),new_user).lastrowid
        
        row = current_app.database.execute(text("""
                SELECT 
                    id,
                    name,
                    email,
                    profile
                FROM users
                WHERE id=:user_id
                """),{
                    'user_id':new_user_id
                }).fetchone()
        
        created_user = {
                'id'    : row['id'],
                'name'  : row['name'],
                'email' : row['email'],
                'profile':row['profile']
                } if row else None

        return jsonify(new_user)
            
    return app

