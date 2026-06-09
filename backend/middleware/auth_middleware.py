from flask import request, jsonify
from functools import wraps
import jwt

SECRET_KEY = "SECRET123"

def token_required(f):

    @wraps(f)
    def decorator(*args, **kwargs):

        auth_header = request.headers.get("Authorization")

        if not auth_header:
            return jsonify({
                "message": "Token missing"
            }), 401

        try:
            token = auth_header.replace("Bearer ", "")

            decoded = jwt.decode(
                token,
                SECRET_KEY,
                algorithms=["HS256"]
            )

            request.user = decoded

        except jwt.ExpiredSignatureError:
            return jsonify({
                "message": "Token expired"
            }), 401

        except jwt.InvalidTokenError:
            return jsonify({
                "message": "Token invalid"
            }), 401

        return f(*args, **kwargs)

    return decorator