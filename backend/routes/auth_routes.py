from flask import Blueprint
from backend.controllers.auth_controller import (
    request_otp_register,
    verify_otp_register,
    login,
    google_login,
    get_profile,
    update_profile,
    forgot_password_controller,
    reset_password_controller,
)

auth_bp = Blueprint(
    "auth",
    __name__
)

auth_bp.route(
    "/register/request-otp",
    methods=["POST"]
)(request_otp_register)

auth_bp.route(
    "/register/verify-otp",
    methods=["POST"]
)(verify_otp_register)

auth_bp.route(
    "/login",
    methods=["POST"]
)(login)

auth_bp.route(
    "/google",
    methods=["POST"]
)(google_login)

auth_bp.route(
    "/profile",
    methods=["GET"]
)(get_profile)
auth_bp.route(
    "/profile",
    methods=["PUT"]
)(update_profile)

auth_bp.route(
    "/forgot-password",
    methods=["POST"]
)(forgot_password_controller)

# ==========================
# RESET PASSWORD
# ==========================

auth_bp.route(
    "/reset-password",
    methods=["POST"]
)(reset_password_controller)