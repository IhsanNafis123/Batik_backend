from flask import Blueprint, jsonify

gallery_bp = Blueprint('gallery', __name__)


@gallery_bp.route('/gallery', methods=['GET'])
def gallery():
    return jsonify({
        "message": "Gallery Batik"
    })