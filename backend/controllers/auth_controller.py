from flask import request, jsonify
from backend.config.database import supabase
from backend.utils.password_helper import hash_password, check_password
from backend.utils.jwt_helper import generate_token
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests
from backend.services.email_service import send_otp_email 
import random

def request_otp_register():
    data = request.json
    name = data.get("name")
    email = data.get("email")
    password = data.get("password")

    # Validasi panjang password
    if not password or len(password) < 8 or len(password) > 12:
        return jsonify({"message": "Password harus memiliki panjang 8 hingga 12 karakter"}), 400

    # 1. Cek apakah user sudah ada di database
    response = supabase.table('users').select("*").eq("email", email).execute()
    user_exists = response.data

    # Generate 6 digit OTP
    otp_code = str(random.randint(100000, 999999))
    hashed_pw = hash_password(password)

    if user_exists:
        user = user_exists[0]
        if user.get("is_verified"):
            return jsonify({"message": "Email sudah terdaftar dan aktif. Silakan login."}), 400
        else:
            # Jika user ada tapi belum verified, perbarui data dan OTP-nya
            supabase.table('users').update({
                "name": name,
                "password": hashed_pw,
                "otp_code": otp_code
            }).eq("email", email).execute()
    else:
        # 2. Jika belum ada, masukkan ke tabel users dengan is_verified = False
        user_data = {
            "name": name,
            "email": email,
            "password": hashed_pw,
            "is_verified": False,
            "otp_code": otp_code,
            "provider": "local"
        }
        supabase.table('users').insert(user_data).execute()

    # 3. Kirim OTP ke Email
    email_sent = send_otp_email(email, otp_code)
    
    if email_sent:
        return jsonify({"message": "Kode OTP telah dikirim ke email Anda"}), 200
    else:
        return jsonify({"message": "Gagal mengirim email verifikasi, pastikan email valid"}), 500

def verify_otp_register():
    data = request.json
    email = data.get("email")
    otp_input = data.get("otp")

    response = supabase.table('users').select("*").eq("email", email).execute()
    if not response.data:
        return jsonify({"message": "Sesi tidak ditemukan. Silakan daftar ulang."}), 404

    user = response.data[0]

    if user.get("is_verified"):
        return jsonify({"message": "Akun sudah terverifikasi sebelumnya."}), 400

    if user.get("otp_code") != str(otp_input):
        return jsonify({"message": "Kode OTP salah"}), 401

    # 4. Jika OTP benar, ubah is_verified menjadi True dan hapus otp_code
    supabase.table('users').update({
        "is_verified": True,
        "otp_code": None
    }).eq("email", email).execute()

    return jsonify({"message": "Registrasi BatikFly berhasil diverifikasi!"}), 201

def login():
    data = request.json
    response = supabase.table('users').select("*").eq("email", data["email"]).execute()
    
    if not response.data:
        return jsonify({"message": "User tidak ditemukan"}), 404
        
    user = response.data[0]
    
    # Mencegah user login jika belum memverifikasi OTP
    if user.get("provider") == "local" and not user.get("is_verified"):
        return jsonify({"message": "Akun belum diverifikasi. Silakan daftar ulang untuk meminta OTP."}), 403

    if not user.get("password"):
        return jsonify({"message": "Akun didaftarkan via Google. Silakan login dengan Google."}), 401

    if not check_password(data["password"], user["password"]):
        return jsonify({"message": "Password salah"}), 401

    token = generate_token(user)
    supabase.table("users").update({"jwt_token": token}).eq("id", user["id"]).execute()
    return jsonify({"token": token, "message": "Login berhasil"}), 200

def google_login():
    data = request.json
    google_token = data.get("id_token")

    if not google_token:
        return jsonify({"message": "Google token tidak ditemukan"}), 400

    try:
        user_info = id_token.verify_oauth2_token(google_token, google_requests.Request())
        email = user_info["email"]
        name = user_info.get("name", "")
        picture = user_info.get("picture", "")

        response = supabase.table("users").select("*").eq("email", email).execute()
        if response.data:
            user = response.data[0]
        else:
            new_user = {
                "name": name, 
                "email": email, 
                "avatar": picture, 
                "password": None, 
                "provider": "google",
                "is_verified": True # User google otomatis verified
            }
            insert_result = supabase.table("users").insert(new_user).execute()
            user = insert_result.data[0]

        token = generate_token(user)
        supabase.table("users").update({"jwt_token": token}).eq("id", user["id"]).execute()
        return jsonify({"message": "Login Google berhasil", "token": token, "user": user}), 200

    except Exception as e:
        return jsonify({"message": str(e)}), 401