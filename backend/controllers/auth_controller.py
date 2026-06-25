from flask import request, jsonify
from backend.config.database import supabase
from backend.utils.password_helper import (
    hash_password,
    check_password
)
from backend.utils.jwt_helper import generate_token
from backend.services.email_service import send_otp_email

from google.oauth2 import id_token
from google.auth.transport import requests as google_requests
from backend.utils.jwt_helper import verify_token

import random


# ==========================================
# REGISTER REQUEST OTP
# ==========================================

def request_otp_register():

    data = request.json

    name = data.get("name")
    email = data.get("email")
    password = data.get("password")

    if not name or not email or not password:
        return jsonify({
            "message": "Data tidak lengkap"
        }), 400

    if len(password) < 8 or len(password) > 12:
        return jsonify({
            "message":
            "Password harus 8-12 karakter"
        }), 400

    response = (
        supabase
        .table("users")
        .select("*")
        .eq("email", email)
        .execute()
    )

    user_exists = response.data

    otp_code = str(
        random.randint(
            100000,
            999999
        )
    )

    hashed_pw = hash_password(password)

    if user_exists:

        user = user_exists[0]

        if user.get("is_verified"):

            return jsonify({
                "message":
                "Email sudah terdaftar"
            }), 400

        (
            supabase
            .table("users")
            .update({
                "name": name,
                "password": hashed_pw,
                "otp_code": otp_code
            })
            .eq("email", email)
            .execute()
        )

    else:

        (
            supabase
            .table("users")
            .insert({
                "name": name,
                "email": email,
                "password": hashed_pw,
                "otp_code": otp_code,
                "is_verified": False,
                "provider": "local"
            })
            .execute()
        )

    email_sent = send_otp_email(
        email,
        otp_code
    )

    if not email_sent:
        return jsonify({
            "message":
            "Gagal mengirim OTP"
        }), 500

    return jsonify({
        "message":
        "Kode OTP telah dikirim ke email"
    }), 200


# ==========================================
# VERIFY OTP
# ==========================================

def verify_otp_register():

    data = request.json

    email = data.get("email")
    otp_input = data.get("otp")

    response = (
        supabase
        .table("users")
        .select("*")
        .eq("email", email)
        .execute()
    )

    if not response.data:

        return jsonify({
            "message":
            "User tidak ditemukan"
        }), 404

    user = response.data[0]

    if user.get("is_verified"):

        return jsonify({
            "message":
            "Akun sudah diverifikasi"
        }), 400

    if user.get("otp_code") != str(otp_input):

        return jsonify({
            "message":
            "Kode OTP salah"
        }), 401

    (
        supabase
        .table("users")
        .update({
            "is_verified": True,
            "otp_code": None
        })
        .eq("email", email)
        .execute()
    )

    return jsonify({
        "message":
        "Registrasi berhasil"
    }), 201


# ==========================================
# LOGIN EMAIL
# ==========================================

def login():

    data = request.json

    email = data.get("email")
    password = data.get("password")

    response = (
        supabase
        .table("users")
        .select("*")
        .eq("email", email)
        .execute()
    )

    if not response.data:

        return jsonify({
            "message":
            "User tidak ditemukan"
        }), 404

    user = response.data[0]

    if (
        user.get("provider") == "local"
        and
        not user.get("is_verified")
    ):

        return jsonify({
            "message":
            "Akun belum diverifikasi"
        }), 403

    if not user.get("password"):

        return jsonify({
            "message":
            "Silakan login menggunakan Google"
        }), 401

    if not check_password(
        password,
        user["password"]
    ):

        return jsonify({
            "message":
            "Password salah"
        }), 401

    token = generate_token(user)

    (
        supabase
        .table("users")
        .update({
            "jwt_token": token
        })
        .eq("id", user["id"])
        .execute()
    )

    return jsonify({

        "message":
        "Login berhasil",

        "token":
        token,

        "user": {
            "id":
            user["id"],

            "name":
            user["name"],

            "email":
            user["email"],

            "avatar":
            user.get(
                "avatar",
                ""
            ),

            "provider":
            user.get(
                "provider",
                "local"
            )
        }

    }), 200


# ==========================================
# LOGIN GOOGLE
# ==========================================

def google_login():

    data = request.json

    google_token = data.get(
        "id_token"
    )

    if not google_token:

        return jsonify({
            "message":
            "Google token tidak ditemukan"
        }), 400

    try:

        user_info = (
            id_token
            .verify_oauth2_token(
                google_token,
                google_requests.Request()
            )
        )

        email = user_info["email"]

        name = user_info.get(
            "name",
            ""
        )

        picture = user_info.get(
            "picture",
            ""
        )

        response = (
            supabase
            .table("users")
            .select("*")
            .eq("email", email)
            .execute()
        )

        if response.data:

            user = response.data[0]

        else:

            insert_result = (
                supabase
                .table("users")
                .insert({

                    "name":
                    name,

                    "email":
                    email,

                    "avatar":
                    picture,

                    "password":
                    None,

                    "provider":
                    "google",

                    "is_verified":
                    True

                })
                .execute()
            )

            user = insert_result.data[0]

        token = generate_token(user)

        (
            supabase
            .table("users")
            .update({
                "jwt_token":
                token
            })
            .eq(
                "id",
                user["id"]
            )
            .execute()
        )

        return jsonify({

            "message":
            "Login Google berhasil",

            "token":
            token,

            "user": {
                "id":
                user["id"],

                "name":
                user["name"],

                "email":
                user["email"],

                "avatar":
                user.get(
                    "avatar",
                    ""
                ),

                "provider":
                user.get(
                    "provider",
                    "google"
                )
            }

        }), 200
        

    except Exception as e:

        print(
            "GOOGLE LOGIN ERROR:",
            str(e)
        )

        return jsonify({
            "message":
            str(e)
        }), 401
        
# ==========================================
# GET PROFILE
# ==========================================

def get_profile():

    auth_header = request.headers.get(
        "Authorization"
    )

    if not auth_header:

        return jsonify({
            "message":
            "Token tidak ditemukan"
        }), 401

    try:

        token = auth_header.split(
            " "
        )[1]

        payload = verify_token(
            token
        )

        response = (
            supabase
            .table("users")
            .select("*")
            .eq(
                "id",
                payload["user_id"]
            )
            .execute()
        )

        if not response.data:

            return jsonify({
                "message":
                "User tidak ditemukan"
            }), 404

        user = response.data[0]

        return jsonify({

            "id":
            user["id"],

            "name":
            user["name"],

            "email":
            user["email"],

            "avatar":
            user.get(
                "avatar",
                ""
            ),

            "provider":
            user.get(
                "provider",
                ""
            )

        }), 200

    except Exception as e:

        return jsonify({
            "message":
            str(e)
        }), 401