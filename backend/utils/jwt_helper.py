import os
import jwt

from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()

# ==========================================
# SECRET KEY
# ==========================================

SECRET_KEY = os.getenv(
    "JWT_SECRET",
    "SECRET123"
)

# ==========================================
# GENERATE TOKEN
# ==========================================

def generate_token(user):

    payload = {

        "user_id": str(
            user["user_id"]
        ),

        "name":
            user["name"],

        "email":
            user["email"],

        "iat":
            datetime.utcnow(),

        "exp":
            datetime.utcnow()
            + timedelta(days=7)

    }

    return jwt.encode(

        payload,

        SECRET_KEY,

        algorithm="HS256"

    )

# ==========================================
# VERIFY TOKEN
# ==========================================

def verify_token(token):

    try:

        payload = jwt.decode(

            token,

            SECRET_KEY,

            algorithms=["HS256"]

        )

        return payload

    except jwt.ExpiredSignatureError:

        raise Exception(
            "Token expired"
        )

    except jwt.InvalidTokenError:

        raise Exception(
            "Token invalid"
        )