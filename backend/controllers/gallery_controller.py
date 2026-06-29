from flask import jsonify
# Gunakan koneksi database utama Anda
from backend.config.database import supabase 

def get_all_designs():
    try:
        # Melakukan query ke tabel 'designs' dan JOIN dengan tabel 'users' 
        # (Supabase akan membaca foreign key 'user_id' secara otomatis)
        response = supabase.table('designs') \
            .select('*, users(name, avatar)') \
            .order('created_at', desc=True) \
            .execute()
        
        return jsonify({
            "success": True,
            "message": "Berhasil mengambil referensi desain",
            "data": response.data
        }), 200
        
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Error: {str(e)}"
        }), 500