from flask import request, jsonify

from backend.utils.jwt_helper import verify_token
from backend.services.activity_log_service import (
    get_activity_logs
)


# ==========================================================
# GET ACTIVITY LOGS
# ==========================================================

def activity_logs():

    auth_header = request.headers.get(
        "Authorization"
    )

    if not auth_header:

        return jsonify({

            "success": False,

            "message":
            "Token tidak ditemukan"

        }), 401

    try:

        token = auth_header.split(" ")[1]

        payload = verify_token(
            token
        )

        activities = get_activity_logs(
            payload["user_id"]
        )

        return jsonify({

            "success": True,

            "data": activities

        }), 200

    except Exception as e:

        return jsonify({

            "success": False,

            "message": str(e)

        }), 401