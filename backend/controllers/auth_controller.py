from flask import request, jsonify
from backend.config.database import supabase # Import supabase client
from backend.utils.password_helper import hash_password, check_password
from backend.utils.jwt_helper import generate_token
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests

def register():
    data = request.json
    
    # 1. Cek apakah email sudah ada di tabel 'users'
    response = supabase.table('users').select("*").eq("email", data["email"]).execute()
    
    if response.data: # Jika ada data yang kembali, berarti email sudah dipakai
        return jsonify({
            "message": "Email sudah digunakan"
        }), 400

    # 2. Persiapkan data user baru
    user_data = {
        "name": data["name"],
        "email": data["email"],
        "password": hash_password(data["password"])
    }

    # 3. Insert ke tabel 'users'
    supabase.table('users').insert(user_data).execute()

    return jsonify({
        "message": "Register berhasil"
    }), 201


def login():
    data = request.json

    # 1. Cari user berdasarkan email
    response = supabase.table('users').select("*").eq("email", data["email"]).execute()
    
    if not response.data:
        return jsonify({
            "message": "User tidak ditemukan"
        }), 404
        
    user = response.data[0] # Ambil objek user pertama dari hasil query

    # 2. Cek password
    if not check_password(data["password"], user["password"]):
        return jsonify({
            "message": "Password salah"
        }), 401

    # 3. Generate token (pastikan fungsi generate_token menerima dictionary user)
    token = generate_token(user)
    supabase.table("users").update({"jwt_token": token}).eq("id", user["id"]).execute()
    return jsonify({
        "token": token,
        "message": "Login berhasil"
    }), 200
    
def google_login():
    data = request.json

    google_token = data.get("id_token")

    if not google_token:
        return jsonify({
            "message": "Google token tidak ditemukan"
        }), 400

    try:
        user_info = id_token.verify_oauth2_token(
            google_token,
            google_requests.Request()
        )

        email = user_info["email"]
        name = user_info.get("name", "")
        picture = user_info.get("picture", "")

        # cek user
        response = (
            supabase.table("users")
            .select("*")
            .eq("email", email)
            .execute()
        )

        if response.data:
            user = response.data[0]

        else:
            new_user = {
                "name": name,
                "email": email,
                "avatar": picture,
                "password": None,
                "provider": "google"
            }

            insert_result = (
                supabase.table("users")
                .insert(new_user)
                .execute()
            )

            user = insert_result.data[0]

        token = generate_token(user)
        supabase.table("users").update({"jwt_token": token}).eq("id", user["id"]).execute()
        return jsonify({
            "message": "Login Google berhasil",
            "token": token,
            "user": user
        }), 200

    except Exception as e:
        return jsonify({
            "message": str(e)
        }), 401