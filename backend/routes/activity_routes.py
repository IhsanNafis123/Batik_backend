from flask import Blueprint

from backend.controllers.activity_controller import (
    activity_logs
)
from backend.config.database import supabase


activity_bp = Blueprint(
    "activity",
    __name__
)

activity_bp.route(

    "/logs",

    methods=["GET"]

)(activity_logs)

