from flask import (
    render_template,
    redirect,
    flash,
    session
)

from backend.config.database import supabase


# ==========================
# GALLERY USER
# ==========================

def user_designs(user_id):

    if "admin" not in session:
        return redirect("/admin/login")

    try:

        user_result = (
            supabase
            .table("users")
            .select("*")
            .eq("id", user_id)
            .execute()
        )

        if not user_result.data:

            flash(
                "User tidak ditemukan",
                "error"
            )

            return redirect("/dashboard")

        user = user_result.data[0]

        designs_result = (
            supabase
            .table("designs")
            .select("*")
            .eq("user_id", user_id)
            .order(
                "created_at",
                desc=True
            )
            .execute()
        )

        return render_template(
            "admin_designs.html",
            user=user,
            designs=designs_result.data
        )

    except Exception as e:

        flash(
            str(e),
            "error"
        )

        return redirect("/dashboard")


# ==========================
# DETAIL DESIGN
# ==========================

def detail_design(design_id):

    if "admin" not in session:
        return redirect("/admin/login")

    result = (
        supabase
        .table("designs")
        .select("*")
        .eq("id", design_id)
        .execute()
    )

    if not result.data:

        flash(
            "Design tidak ditemukan",
            "error"
        )

        return redirect("/dashboard")

    design = result.data[0]

    return render_template(
        "design_detail.html",
        design=design
    )


# ==========================
# HAPUS DESIGN
# ==========================

def delete_design(design_id):

    if "admin" not in session:
        return redirect("/admin/login")

    (
        supabase
        .table("designs")
        .delete()
        .eq("id", design_id)
        .execute()
    )

    flash(
        "Design berhasil dihapus",
        "success"
    )

    return redirect("/dashboard")