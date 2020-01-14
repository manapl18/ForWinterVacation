from flask import Flask, jsonify, request
from sqlalchemy import create_engine, text

def create_app(test_config=None):
    app = Flask(__name__)
    
    if test_config is None:
        app.config.from_pyfile("config.py")
    else:
        app.config.update(test_config)
    database=create_engine(app.config['DB_URL'],encoding='utf-8', max_overflow=0)
    app.database=database
    

    @app.route("/ping",methods=['GET'])
    def ping():
        return "pong"

    @app.route("/sign-up",methods=['POST'])
    def sign_up():
        new_user                = request.json
        new_user_id             = app.database.excute(text("""
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
                         """), new_user). lastrowid
        row = current_app.database.excute(text("""
                    SELECT id,name,eamil,profile
                    FROM users
                    WHERE id = :user_id
                    """),{
                    'user_id':new_user_id
                    }).fetchone()

        created_user = {
                    'id' : row['id'],
                    'name' : row['name'],
                    'email' : row['email'],
                    'profile' : row['profile']
                    } if row else None

        return jsonify(created_user)

    @app.route("/tweet",methods=['POST'])
    def tweet():
        payload     = request.json
        user_id     = int(payload['id'])
        tweet       = payload['tweet']

        if user_id not in app.users:
            return 'user is not existed', 400

        if len(tweet) > 300:
            return 'overload',400

        user_id = int(payload['id'])

        app.tweets.append({
            'user_id'   : user_id,
            'tweet'     : tweet
            })

        return '', 200
    return app
