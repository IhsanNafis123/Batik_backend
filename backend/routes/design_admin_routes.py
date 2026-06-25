from flask import Blueprint

from backend.controllers.design_admin_controller import (
    user_designs,
    detail_design,
    delete_design
)

design_admin_bp = Blueprint(
    "design_admin_bp",
    __name__
)


@design_admin_bp.route(
    "/admin/designs/<user_id>"
)
def admin_designs(user_id):

    return user_designs(user_id)


@design_admin_bp.route(
    "/admin/design-detail/<design_id>"
)
def admin_design_detail(design_id):

    return detail_design(design_id)


@design_admin_bp.route(
    "/admin/delete-design/<design_id>"
)
def admin_delete_design(design_id):

    return delete_design(design_id)