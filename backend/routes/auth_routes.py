from flask import Blueprint

from backend.controllers.auth_controller import (register,login,google_login)

auth_bp = Blueprint('auth', __name__)

auth_bp.route('/register', methods=['POST'])(register)
auth_bp.route('/login', methods=['POST'])(login)
auth_bp.route('/google', methods=['POST'])(google_login)