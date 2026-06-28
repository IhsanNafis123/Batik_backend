import os
import random
import string
import uuid

from flask import (
    Flask,
    jsonify,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    session
)
from backend.routes.design_admin_routes import (
    design_admin_bp
)

from backend.routes.analytics_routes import analytics_bp
from flask_cors import CORS
from dotenv import load_dotenv
from supabase import create_client, Client

# ==========================================
# IMPORT ROUTES
# ==========================================

from backend.services.email_service import send_otp_email

from backend.routes.auth_routes import auth_bp
from backend.routes.design_routes import design_bp
from backend.routes.fitting_routes import fitting_bp
from backend.routes.admin_routes import admin_bp
from backend.services.clip_service import load_embedding_cache
from backend.middleware.recommendation_routes import recommendation_bp
from backend.middleware.gallery_routes import gallery_bp
from backend.routes.activity_routes import activity_bp

load_dotenv()

app = Flask(__name__)
CORS(app)

app.secret_key = "batikflyy_super_secret"

supabase: Client = create_client(
    os.environ.get("SUPABASE_URL"),
    os.environ.get("SUPABASE_KEY")
)

# ==========================================
# REGISTER BLUEPRINTS
# ==========================================

app.register_blueprint(
    auth_bp,
    url_prefix="/auth"
)

app.register_blueprint(
    activity_bp,
    url_prefix="/activity"
)

app.register_blueprint(
    design_bp
)

app.register_blueprint(
    fitting_bp
)

app.register_blueprint(
    recommendation_bp
)

app.register_blueprint(
    gallery_bp
)

app.register_blueprint(
    admin_bp
)
app.register_blueprint(
    design_admin_bp
)

app.register_blueprint(
    analytics_bp
)
# ==========================================

# ==========================================
# DASHBOARD ADMIN
# ==========================================

@app.route("/dashboard")
def dashboard():

    if "admin" not in session:

        return redirect(
            "/admin/login"
        )

    response = (
        supabase
        .table("users")
        .select("*")
        .order(
            "created_at",
            desc=True
        )
        .execute()
    )

    return render_template(
        "index.html",
        users=response.data
    )

# ==========================================
# TAMBAH USER
# ==========================================

@app.route(
    "/tambah-user",
    methods=["POST"]
)
def tambah_user():

    name = request.form.get(
        "name"
    )

    email = request.form.get(
        "email"
    )

    password = request.form.get(
        "password"
    )

    otp = ''.join(
        random.choices(
            string.digits,
            k=6
        )
    )

    new_user_id = str(
        uuid.uuid4()
    )

    if send_otp_email(
        email,
        otp
    ):

        try:

            (
                supabase
                .table("users")
                .insert({

                    "user_id":
                    new_user_id,

                    "name":
                    name,

                    "email":
                    email,

                    "password":
                    password,

                    "otp_code":
                    otp,

                    "is_verified":
                    False
                })
                .execute()
            )

            return redirect(
                url_for(
                    "verifikasi_halaman",
                    email=email
                )
            )

        except Exception as e:

            flash(
                f"Error Database: {str(e)}",
                "error"
            )

    else:

        flash(
            "Gagal kirim email OTP.",
            "error"
        )

    return redirect(
        url_for(
            "dashboard"
        )
    )
    
@app.route("/edit-user/<id>", methods=["GET", "POST"])
def edit_user(id):

    if "admin" not in session:
        return redirect("/admin/login")

    # ambil user
    result = (
        supabase
        .table("users")
        .select("*")
        .eq("id", id)
        .execute()
    )

    if not result.data:
        flash("User tidak ditemukan", "error")
        return redirect("/dashboard")

    user = result.data[0]

    # submit edit
    if request.method == "POST":

        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")

        update_data = {
            "name": name,
            "email": email
        }

        if password:
            update_data["password"] = password

        (
            supabase
            .table("users")
            .update(update_data)
            .eq("id", id)
            .execute()
        )

        flash(
            "Data user berhasil diperbarui",
            "success"
        )

        return redirect("/dashboard")

    return render_template(
        "edit.html",
        user=user
    )

# ==========================================
# VERIFIKASI OTP
# ==========================================

@app.route(
    "/verifikasi/<email>",
    methods=[
        "GET",
        "POST"
    ]
)
def verifikasi_halaman(email):

    if request.method == "POST":

        user_otp = request.form.get(
            "otp"
        )

        user = (
            supabase
            .table("users")
            .select("*")
            .eq(
                "email",
                email
            )
            .eq(
                "otp_code",
                user_otp
            )
            .execute()
        )

        if user.data:

            (
                supabase
                .table("users")
                .update({

                    "is_verified":
                    True,

                    "otp_code":
                    None
                })
                .eq(
                    "email",
                    email
                )
                .execute()
            )

            flash(
                "Akun berhasil diverifikasi!",
                "success"
            )

            return redirect(
                url_for(
                    "dashboard"
                )
            )

        flash(
            "Kode OTP salah!",
            "error"
        )

    return render_template(
        "otp.html",
        email=email
    )

# ==========================================
# HAPUS USER
# ==========================================

@app.route(
    "/hapus-user/<int:id>"
)
def hapus_user(id):

    (
        supabase
        .table("users")
        .delete()
        .eq(
            "id",
            id
        )
        .execute()
    )

    return redirect(
        url_for(
            "dashboard"
        )
    )

# ==========================================
# LOGOUT ADMIN
# ==========================================

@app.route("/logout")
def logout():

    session.clear()

    return redirect(
        "/admin/login"
    )

# ==========================================
# API STATUS
# ==========================================

@app.route(
    "/api/status",
    methods=["GET"]
)
def api_status():

    return jsonify({

        "status":
        "success",

        "message":
        "Backend BatikFly API berjalan!"
    }), 200

# ==========================================
# RUN APP
# ==========================================

@app.route("/admin/gallery/<user_id>")
def admin_user_gallery(user_id):
    # Pastikan admin sudah login
    if "admin" not in session:
        return redirect("/admin/login")

    try:
        # 1. Ambil info user
        user_result = supabase.table("users").select("name, email").eq("user_id", user_id).execute()
        user_info = user_result.data[0] if user_result.data else {"name": "Unknown", "email": ""}

        # 2. Ambil desain milik user ini
        designs_result = (
            supabase
            .table("designs")
            .select("*")
            .eq("user_id", user_id)
            .order("created_at", desc=True)
            .execute()
        )

        # 3. Ambil fitting milik user ini
        fittings_result = (
            supabase
            .table("fittings")
            .select("*")
            .eq("user_id", user_id)
            .order("created_at", desc=True)
            .execute()
        )

        # Return ke template HTML (misal: admin_gallery.html)
        return render_template(
            "admin_gallery.html",
            user=user_info,
            designs=designs_result.data,
            fittings=fittings_result.data
        )

    except Exception as e:
        flash(f"Error fetching gallery: {str(e)}", "error")
        return redirect("/dashboard")

if __name__ == "__main__":

    app.debug = True

    if os.environ.get("WERKZEUG_RUN_MAIN") == "true" or not app.debug:

        print("=" * 60)
        print("Loading CLIP Cache...")

        load_embedding_cache()

        print("CLIP Cache Ready!")
        print("=" * 60)

    print(app.url_map)

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )