from flask import Blueprint, jsonify
from backend.config.database import supabase

# Kita beri nama blueprint 'gallery'
gallery_bp = Blueprint('gallery', __name__)

@gallery_bp.route('/api/gallery', methods=['GET'])
# CATATAN: @token_required sengaja DIHAPUS agar semua user bisa melihat galeri referensi ini
def get_public_gallery():
    try:
        # Mengambil SEMUA data dari tabel designs (tanpa difilter eq user_id)
        # Serta melakukan JOIN ke tabel users untuk mengambil name dan avatar pembuatnya
        response = (
            supabase
            .table("designs")
            .select("*, users(name, avatar)")
            .order("created_at", desc=True)
            .execute()
        )
        
        # Mengirimkan data dengan format yang sesuai dengan tangkapan Flutter
        return jsonify({
            "success": True,
            "message": "Berhasil mengambil galeri referensi",
            "data": response.data if response.data else []
        }), 200

    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Terjadi kesalahan di server: {str(e)}"
        }), 500