from flask import Blueprint
# Pastikan Anda mengimpor kedua fungsi ini dari controller
from backend.controllers.fitting_controller import generate_vton, simpan_fitting
from backend.controllers.fitting_controller import (
    upload_motif,
    generate_vton,
    simpan_fitting,
)

fitting_bp = Blueprint('fitting_bp', __name__)

@fitting_bp.route('/api/fitting/upload', methods=['POST'])
def upload_route():
    print("DEBUG: Request masuk ke /api/fitting/upload!") # Tambahkan ini
    return upload_motif()
def upload_route():
    return upload_motif()
@fitting_bp.route('/api/fitting/generate-vton', methods=['POST'])
def generate_vton_route():
    return generate_vton()

@fitting_bp.route('/api/fitting/save', methods=['POST'])
def save_fitting_route():
    print("DEBUG: Request masuk ke /api/fitting/save!") # Tambahkan ini
    return simpan_fitting()