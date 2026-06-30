from flask import Blueprint

from backend.controllers.analytics_controller import (
    analytics_dashboard,
    get_mobile_analytics
)

analytics_bp = Blueprint(
    "analytics_bp",
    __name__
)

@analytics_bp.route(
    "/admin/analytics"
)
def analytics():

    return analytics_dashboard()

@analytics_bp.route("/api/analytics", methods=["GET"])
def mobile_analytics():
    return get_mobile_analytics()