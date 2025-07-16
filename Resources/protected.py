from flask import jsonify
from flask_restful import Resource, request
from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity,
    JWTManager
)
from CreateResources.jwt import jwt

# ✅ Error handler registration
def register_jwt_error_handlers():
    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return jsonify({
            "message": "⚠️ Token has expired. Please re-login.",
            "error": "token_expired"
        }), 401

    @jwt.invalid_token_loader
    def invalid_token_callback(reason):
        return jsonify({
            "message": "💔 ❌ Invalid token. Please login again.",
            "error": "invalid_token"
        }), 422

    @jwt.unauthorized_loader
    def missing_token_callback(reason):
        return jsonify({
            "message": "Authorization token missing.",
            "error": "authorization_required"
        }), 401


class ProtectedResource(Resource):
    @jwt_required()
    def get(self):
        current_user_id = get_jwt_identity()
        print(f"\nId get...")
        return{"message": f"You accessed protected resource", "user_id": f"User-id: {current_user_id}"}, 200

print("✅ Resources.protected loaded")
