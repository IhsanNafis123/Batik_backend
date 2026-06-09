import jwt
from datetime import datetime, timedelta

SECRET_KEY = "SECRET123"

def generate_token(user):
    payload = {
        "user_id": str(user["_id"]),
        "name": user["name"],
        "email": user["email"],
        "exp": datetime.utcnow() + timedelta(hours=24)
    }

    token = jwt.encode(
        payload,
        SECRET_KEY,
        algorithm="HS256"
    )

    return token