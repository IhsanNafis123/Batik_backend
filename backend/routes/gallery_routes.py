from flask import Blueprint
from backend.controllers.gallery_controller import get_all_designs

# Inisialisasi Blueprint untuk rute galeri
gallery_bp = Blueprint("gallery_bp", __name__)

# Membuat endpoint API dengan metode GET
@gallery_bp.route("/api/gallery", methods=["GET"])
def fetch_gallery():
    return get_all_designs()