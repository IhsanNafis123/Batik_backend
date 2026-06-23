
from flask import Blueprint

from backend.controllers.admin_controller import (
    login_page,
    login_admin,
    edit_user
)

admin_bp = Blueprint(
    "admin_bp",
    __name__
)

# ==========================
# LOGIN ADMIN
# ==========================

@admin_bp.route(
    "/admin/login",
    methods=["GET"]
)
def home():

    return login_page()


@admin_bp.route(
    "/admin/login",
    methods=["POST"]
)
def login():

    return login_admin()


# ==========================
# EDIT USER
# ==========================

@admin_bp.route(
    "/edit-user/<id>",
    methods=["GET", "POST"]
)
def edit_user_route(id):

    return edit_user(id)

