from flask import Blueprint, jsonify, request
from backend.config.database import supabase
from backend.middleware.auth_middleware import token_required

gallery_bp = Blueprint('gallery', __name__)

@gallery_bp.route('/api/gallery', methods=['GET'])
@token_required # Memastikan hanya user yang login yang bisa mengakses
def get_user_gallery(current_user):
    try:
        user_id = current_user['user_id']

        # Mengambil data desain berdasarkan user_id
        designs_response = (
            supabase
            .table("designs")
            .select("*")
            .eq("user_id", user_id)
            .order("created_at", desc=True)
            .execute()
        )
        
        # Mengambil data fitting berdasarkan user_id
        fittings_response = (
            supabase
            .table("fittings")
            .select("*")
            .eq("user_id", user_id)
            .order("created_at", desc=True)
            .execute()
        )
        
        return jsonify({
            "status": "success",
            "data": {
                "designs": designs_response.data if designs_response.data else [],
                "fittings": fittings_response.data if fittings_response.data else []
            }
        }), 200

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Terjadi kesalahan saat mengambil galeri: {str(e)}"
        }), 500