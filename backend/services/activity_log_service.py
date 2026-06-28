from backend.config.database import supabase


# ==========================================================
# GET ACTIVITY LOGS
# ==========================================================

def get_activity_logs(user_id):

    response = (
        supabase
        .table("activity_logs")
        .select("*")
        .eq("user_id", user_id)
        .order(
            "created_at",
            desc=True
        )
        .execute()
    )

    return response.data


# ==========================================================
# SAVE ACTIVITY
# ==========================================================

def save_activity(
    user_id,
    activity,
    description
):

    (
        supabase
        .table("activity_logs")
        .insert({
            "user_id": user_id,
            "activity": activity,
            "description": description
        })
        .execute()
    )