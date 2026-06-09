from flask import Blueprint

from backend.controllers.design_controller import generate_design
from backend.controllers.design_controller import (generate_design,get_motifs)
design_bp = Blueprint(
    "design_bp",
    __name__
)

@design_bp.route(
    "/design/generate",
    methods=["POST"]
)
def generate():
    return generate_design()
@design_bp.route(
    "/motifs",
    methods=["GET"]
)
def motifs():
    return get_motifs()