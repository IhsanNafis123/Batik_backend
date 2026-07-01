import uuid
from flask import request, jsonify
from backend.config.database import supabase
from backend.utils.password_helper import (
    hash_password,
    check_password
)
from datetime import datetime, timezone
from backend.utils.jwt_helper import generate_token
from backend.services.profile_service import get_profile as get_profile_service
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests
from backend.utils.jwt_helper import verify_token
from backend.services.activity_log_service import save_activity
from backend.utils.token_helper import (
    generate_reset_token,
    generate_reset_token_expired
)
from backend.services.email_service import (
    send_otp_email,
    send_reset_password_email
)
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
        new_user_id = str(uuid.uuid4())
        (
            supabase
            .table("users")
            .insert({
                "user_id": new_user_id,
                "name": name,
                "email": email,
                "password": hashed_pw,
                "otp_code": otp_code,
                "provider": "local",
                "is_verified": False
            })
            .execute()
        )
        save_activity(

            user_id=new_user_id,

            activity="REGISTER",

            description="Membuat akun baru"

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
    
    save_activity(

        user_id=user["user_id"],

        activity="LOGIN",

        description="Login menggunakan Email"

    )

    (
        supabase
        .table("users")
        .update({
            "jwt_token": token
        })
        .eq("user_id", user["user_id"])
        .execute()
    )

    return jsonify({

        "message":
        "Login berhasil",

        "token":
        token,

        "user": {
            "id":
            user["user_id"],

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
                    "user_id": str(uuid.uuid4()),
                    "name": name,
                    "email": email,
                    "avatar": picture,
                    "password": None,
                    "provider": "google",
                    "is_verified": True
                })
                .execute()
            )

            user = insert_result.data[0]

        token = generate_token(user)
        save_activity(

            user_id=user["user_id"],

            activity="GOOGLE_LOGIN",

            description="Login menggunakan Google"

        )

        (
            supabase
            .table("users")
            .update({
                "jwt_token":
                token
            })
            .eq(
                "user_id",
                user["user_id"]
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
                user["user_id"],

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

            "success": False,

            "message":
            "Token tidak ditemukan"

        }), 401

    try:

        token = auth_header.split(" ")[1]

        payload = verify_token(token)

        profile = get_profile_service(
            payload["user_id"]
        )

        return jsonify({

            "success": True,

            "data": profile

        }), 200

    except Exception as e:

        return jsonify({

            "success": False,

            "message": str(e)

        }), 401
        
# ==========================================
# UPDATE PROFILE
# ==========================================

def update_profile():

    auth_header = request.headers.get("Authorization")

    if not auth_header:

        return jsonify({

            "success": False,
            "message": "Token tidak ditemukan"

        }), 401

    try:

        token = auth_header.split(" ")[1]

        payload = verify_token(token)

        response = (
            supabase
            .table("users")
            .select("*")
            .eq("user_id", payload["user_id"])
            .execute()
        )

        if not response.data:

            return jsonify({

                "success": False,
                "message": "User tidak ditemukan"

            }), 404

        user = response.data[0]

        name = request.form.get("name")
        email = request.form.get("email")
        old_password = request.form.get("old_password")
        new_password = request.form.get("new_password")

        update_data = {}
        avatar = request.files.get("avatar")
        # ==========================
        # USERNAME
        # ==========================

        if name:
            update_data["name"] = name

        if avatar:

            from backend.services.storage_service import upload_avatar

            avatar_url = upload_avatar(
                avatar,
                user["user_id"]
            )
            if not avatar_url:

                return jsonify({

                    "success": False,

                    "message": "Upload avatar gagal"

                }), 500

            update_data["avatar"] = avatar_url
            
        # ==========================
        # GOOGLE ACCOUNT
        # ==========================

        if user["provider"] == "google":

            (
                supabase
                .table("users")
                .update(update_data)
                .eq("user_id", user["user_id"])
                .execute()
            )
            save_activity(

                user_id=user["user_id"],

                activity="EDIT_PROFILE",

                description="Mengubah informasi profil"

            )
            return jsonify({

                "success": True,
                "message": "Profile berhasil diperbarui"

            }), 200

        # ==========================
        # EMAIL
        # ==========================

        if email and email != user["email"]:

            email_check = (
                supabase
                .table("users")
                .select("user_id")
                .eq("email", email)
                .execute()
            )

            if email_check.data:

                return jsonify({

                    "success": False,
                    "message": "Email sudah digunakan"

                }), 400

            update_data["email"] = email

        # ==========================
        # PASSWORD
        # ==========================

        if new_password:

            if not old_password:

                return jsonify({

                    "success": False,
                    "message": "Password lama wajib diisi"

                }), 400

            if not check_password(
                old_password,
                user["password"]
            ):

                return jsonify({

                    "success": False,
                    "message": "Password lama salah"

                }), 400

            update_data["password"] = hash_password(
                new_password
            )

        # ==========================
        # UPDATE DATABASE
        # ==========================
        if not update_data:

            return jsonify({

                "success": False,

                "message": "Tidak ada data yang diubah"

            }), 400

        (
            supabase
            .table("users")
            .update(update_data)
            .eq("user_id", user["user_id"])
            .execute()
        )
        save_activity(
            user_id=user["user_id"],
            activity="EDIT_PROFILE",
            description="Mengubah informasi profil"
        )
        
        return jsonify({

            "success": True,

            "message": "Profile berhasil diperbarui"

        }), 200

    except Exception as e:

        return jsonify({

            "success": False,

            "message": str(e)

        }), 500
        
def forgot_password_controller():

    data = request.get_json()

    email = data.get("email")

    if not email:
        return jsonify({
            "message": "Email wajib diisi"
        }), 400

    response = (
        supabase
        .table("users")
        .select("*")
        .eq("email", email)
        .execute()
    )

    if not response.data:
        return jsonify({
            "message": "Email tidak ditemukan"
        }), 404

    user = response.data[0]

    # Generate token reset password
    token = generate_reset_token()

    # Waktu kedaluwarsa token (15 menit)
    expired_at = generate_reset_token_expired()

    # Simpan ke database
    (
        supabase
        .table("users")
        .update({
            "reset_token": token,
            "reset_token_expired_at": expired_at
        })
        .eq("user_id", user["user_id"])
        .execute()
    )

    email_sent = send_reset_password_email(email, token)

    if not email_sent:
        return jsonify({
            "message": "Gagal mengirim email reset password."
        }), 500

    return jsonify({
        "message": "Token reset password berhasil dikirim ke email."
    }), 200
        # ==========================================
# RESET PASSWORD
# ==========================================

def reset_password_controller():

    data = request.get_json()

    token = data.get("token")
    new_password = data.get("password")

    if not token or not new_password:
        return jsonify({
            "message": "Token dan password wajib diisi."
        }), 400

    if len(new_password) < 8 or len(new_password) > 12:
        return jsonify({
            "message": "Password harus 8-12 karakter."
        }), 400

    response = (
        supabase
        .table("users")
        .select("*")
        .eq("reset_token", token)
        .execute()
    )

    if not response.data:
        return jsonify({
            "message": "Token reset password tidak valid."
        }), 404

    user = response.data[0]

    expired_at = user.get("reset_token_expired_at")

    if expired_at:

        # Ubah "Z" menjadi offset UTC yang dikenali Python
        expired_time = datetime.fromisoformat(
            expired_at.replace("Z", "+00:00")
        )

        # Bandingkan dengan waktu UTC yang juga timezone-aware
        if datetime.now(timezone.utc) > expired_time:

            return jsonify({
                "message": "Token reset password telah kedaluwarsa."
            }), 400

    hashed_password = hash_password(new_password)

    (
        supabase
        .table("users")
        .update({
            "password": hashed_password,
            "reset_token": None,
            "reset_token_expired_at": None
        })
        .eq("user_id", user["user_id"])
        .execute()
    )

    save_activity(
        user_id=user["user_id"],
        activity="RESET_PASSWORD",
        description="Mengubah password melalui fitur lupa password"
    )

    return jsonify({
        "message": "Password berhasil diperbarui."
    }), 200