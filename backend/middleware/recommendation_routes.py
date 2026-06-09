from flask import Blueprint, jsonify

recommendation_bp = Blueprint('recommendation', __name__)


@recommendation_bp.route('/recommendation', methods=['POST'])
def recommendation():
    return jsonify({
        "batik": "Batik Kawung Modern"
    })