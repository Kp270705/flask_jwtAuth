from flask_restful import Resource, request
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity


class ProtectedResource(Resource):
    @jwt_required()
    def get(self):
        current_user_id = get_jwt_identity()
        print(f"\nId get...")
        return{"message": f"You accessed protected resource", "user_id": f"User-id: {current_user_id}"}, 200

print("✅ Resources.protected loaded")
