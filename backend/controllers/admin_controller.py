from flask import (
    request,
    session,
    redirect,
    render_template,
    flash
)

from backend.config.database import (
    supabase
)


# ==========================
# LOGIN PAGE
# ==========================

def login_page():

    return render_template(
        "login.html"
    )


# ==========================
# LOGIN ADMIN
# ==========================

def login_admin():

    username = request.form.get(
        "username"
    )

    password = request.form.get(
        "password"
    )

    result = (
        supabase
        .table("admins")
        .select("*")
        .eq("username", username)
        .eq("password", password)
        .execute()
    )

    if result.data:

        session["admin"] = username

        return redirect(
            "/dashboard"
        )

    flash(
        "Username atau password salah",
        "error"
    )

    return redirect(
        "/admin/login"
    )


# ==========================
# EDIT USER
# ==========================

def edit_user(id):

    if "admin" not in session:

        return redirect(
            "/admin/login"
        )

    result = (
        supabase
        .table("users")
        .select("*")
        .eq("id", id)
        .execute()
    )

    if not result.data:

        flash(
            "User tidak ditemukan",
            "error"
        )

        return redirect(
            "/dashboard"
        )

    user = result.data[0]

    if request.method == "POST":

        name = request.form.get(
            "name"
        )

        email = request.form.get(
            "email"
        )

        password = request.form.get(
            "password"
        )

        update_data = {

            "name": name,
            "email": email
        }

        if password:

            update_data[
                "password"
            ] = password

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

        return redirect(
            "/dashboard"
        )

    return render_template(
        "edit.html",
        user=user
    )
