from flask import Flask
from flask_cors import CORS
from flask_restful import Api
from CreateResources.db import db
from CreateResources.jwt import jwt
from CreateResources.api import api
from Models.models import User  # Ensure model is imported so db.create_all() sees it

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your_jwt_secret_key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
    CORS(app, resources={r"/*": {"origins": "http://localhost:5173"}})

    db.init_app(app)
    jwt.init_app(app)
    api = Api(app)
    with app.app_context():
        db.create_all()

    from Resources.user import UserRegistration, UserLogin
    from Resources.protected import ProtectedResource

    api.add_resource(UserRegistration, '/register')
    api.add_resource(UserLogin, '/login')
    api.add_resource(ProtectedResource, '/secure')

    print("✅ All resources registered!")
    print(f"endpoints:{api.endpoints}")

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
