from flask import Flask, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

# Load ENV
load_dotenv()
import os
print("FAL_KEY =", os.getenv("FAL_KEY"))
print("GEMINI_API_KEY =", os.getenv("GEMINI_API_KEY"))
print("SUPABASE_URL =", os.getenv("SUPABASE_URL"))

# Blueprint Routes
from backend.routes.auth_routes import auth_bp
from backend.routes.design_routes import design_bp
from backend.routes.fitting_routes import fitting_bp

# Middleware Routes
from backend.middleware.recommendation_routes import recommendation_bp
from backend.middleware.gallery_routes import gallery_bp


app = Flask(__name__)

CORS(app)

# Register Blueprint
app.register_blueprint(auth_bp)
app.register_blueprint(design_bp)
app.register_blueprint(fitting_bp)
app.register_blueprint(recommendation_bp)
app.register_blueprint(gallery_bp)

@app.route("/", methods=["GET"])
def index():

    return jsonify({
        "status": "success",
        "message": "Backend BatikFly API berjalan!"
    }), 200


if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )