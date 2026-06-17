import jwt
from datetime import datetime, timedelta

SECRET_KEY = "SECRET123"

def generate_token(user):
    payload = {
        "user_id": str(user["id"]),
        "name": user["name"],
        "email": user["email"],
        "iat": datetime.utcnow(),
        "exp": datetime.utcnow() + timedelta(hours=1)
    }

    return jwt.encode(
        payload,
        SECRET_KEY,
        algorithm="HS256"
    )


def verify_token(token):
    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=["HS256"]
        )

        return payload

    except jwt.ExpiredSignatureError:
        raise Exception("Token expired")

    except jwt.InvalidTokenError:
        raise Exception("Token invalid")