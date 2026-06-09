from flask import request, jsonify
from backend.config.database import supabase # Import supabase client
from backend.utils.password_helper import hash_password, check_password
from backend.utils.jwt_helper import generate_token

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

    return jsonify({
        "token": token,
        "message": "Login berhasil"
    }), 200