from backend.config.database import supabase


# ==========================================================
# GET PROFILE
# ==========================================================

def get_profile(user_id):

    # ==========================================
    # GET USER
    # ==========================================

    user_result = (
        supabase
        .table("users")
        .select("*")
        .eq("user_id", user_id)
        .single()
        .execute()
    )

    if not user_result.data:
        raise Exception("User tidak ditemukan")

    user = user_result.data

    # ==========================================
    # TOTAL DESIGN
    # ==========================================

    try:

        design_result = (
            supabase
            .table("designs")
            .select(
                "id",
                count="exact"
            )
            .eq(
                "user_id",
                user_id
            )
            .execute()
        )

        total_design = (
            design_result.count
            if design_result.count
            else 0
        )

    except Exception:

        total_design = 0

    # ==========================================
    # TOTAL FITTING
    # ==========================================

    try:

        fitting_result = (
            supabase
            .table("fittings")
            .select(
                "id",
                count="exact"
            )
            .eq(
                "user_id",
                user_id
            )
            .execute()
        )

        total_fitting = (
            fitting_result.count
            if fitting_result.count
            else 0
        )

    except Exception:

        total_fitting = 0

    # ==========================================
    # TOTAL DOWNLOAD
    # ==========================================

    try:

        download_result = (
            supabase
            .table("downloads")
            .select(
                "id",
                count="exact"
            )
            .eq(
                "user_id",
                user_id
            )
            .execute()
        )

        total_download = (
            download_result.count
            if download_result.count
            else 0
        )

    except Exception:

        # Jika tabel downloads belum dibuat
        total_download = 0

    # ==========================================
    # RESPONSE
    # ==========================================

    return {

        "user_id":
            user.get(
                "user_id",
                ""
            ),

        "name":
            user.get(
                "name",
                ""
            ),

        "email":
            user.get(
                "email",
                ""
            ),

        "avatar":
            user.get(
                "avatar",
                ""
            ),

        "provider":
            user.get(
                "provider",
                "local"
            ),

        "created_at":
            user.get(
                "created_at",
                ""
            ),

        "total_design":
            total_design,

        "total_fitting":
            total_fitting,

        "total_download":
            total_download

    }