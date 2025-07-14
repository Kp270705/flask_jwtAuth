from flask import Flask, request, jsonify
import jwt
import datetime
from functools import wraps
from passlib.hash import bcrypt

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_jwt_secret_key'

# Mock user database
users_db = {
    "kunal": bcrypt.hash("password123"),
    "admin": bcrypt.hash("adminpass")
}

# JWT Token Decorator
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')

        if not token:
            return jsonify({'message': 'Token is missing!'}), 401

        try:
            token = token.split(" ")[1]  # "Bearer <token>"
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user = data['user']
        except Exception as e:
            return jsonify({'message': 'Token is invalid!', 'error': str(e)}), 401

        return f(current_user, *args, **kwargs)

    return decorated

# Login Endpoint
@app.route('/login', methods=['POST'])
def login():
    auth = request.get_json()

    if not auth or not auth.get('username') or not auth.get('password'):
        return jsonify({'message': 'Username and password required'}), 400

    username = auth['username']
    password = auth['password']

    if username in users_db and bcrypt.verify(password, users_db[username]):
        token = jwt.encode({
            'user': username,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
        }, app.config['SECRET_KEY'], algorithm="HS256")

        return jsonify({'token': token})

    return jsonify({'message': 'Invalid credentials'}), 401

# Protected Endpoint
@app.route('/protected', methods=['GET'])
@token_required
def protected(current_user):
    return jsonify({'message': f'Hello, {current_user}! This is protected data.'})

if __name__ == '__main__':
    app.run(debug=True)
