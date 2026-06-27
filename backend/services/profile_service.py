from backend.config.database import supabase

# ==========================================================
# GET PROFILE
# ==========================================================

def get_profile(user_id):

    # ==========================================
    # USER
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
        raise Exception("User tidak ditemukan.")

    user = user_result.data

    # ==========================================
    # TOTAL DESIGN
    # ==========================================

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

    # ==========================================
    # TOTAL FITTING
    # ==========================================

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

    # ==========================================
    # TOTAL DOWNLOAD
    # ==========================================

    # Jika belum ada tabel downloads,
    # sementara gunakan 0

    total_download = 0

    # ==========================================
    # AVATAR
    # ==========================================

    avatar = (
        user.get("avatar")
        or user.get("photo_url")
        or ""
    )

    # ==========================================
    # PROVIDER
    # ==========================================

    provider = (
        user.get("provider")
        or "email"
    )

    # ==========================================
    # CREATED AT
    # ==========================================

    created_at = (
        user.get("created_at")
        or ""
    )

    # ==========================================
    # RESPONSE
    # ==========================================

    return {

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
            avatar,

        "provider":
            provider,

        "created_at":
            created_at,

        "total_design":
            total_design,

        "total_fitting":
            total_fitting,

        "total_download":
            total_download

    }