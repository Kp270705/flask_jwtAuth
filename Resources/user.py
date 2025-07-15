
from flask_restful import Resource, request
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token

from Models.models import User
from CreateResources.db import db

class UserRegistration(Resource):
    def post(self):
        print(f"\nIn post")
        data = request.get_json()
        username = data['username']
        password = data['password']
        hashed_password = generate_password_hash(password)
        print(f"\nUsername: {username}, Password: {password}, Hashed: {hashed_password}")

        if not username or not password:
            return {'message': "Username or password missing"}, 400
        
        if User.query.filter_by(username=username).first():
            return {'message':"User already exists"}, 400
        
        newUser = User(username=username, password=hashed_password)
        db.session.add(newUser)
        db.session.commit()
        return {'message': "User registered successfully"}, 201


class UserLogin(Resource):
    def post(self):
        print(f"\nIn User Login")
        data = request.get_json()
        username = data['username']
        password = data['password']

        user  = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            access_token = create_access_token(identity=str(user.id))
            print(f"\nUser: {user.username}")
            
            print(f"Access token: {access_token}")
            return {'access_token': f"{access_token}"}, 200
        return {'message': "Invalid credentials"}, 401
    
print("✅ Resources.user loaded")
