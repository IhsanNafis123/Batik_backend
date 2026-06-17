from backend.config.database import supabase

def save_design(
    user_id,
    mode,
    motif_name,
    prompt,
    image_url,
    philosophy,
    density
):

    result = (
        supabase
        .table("designs")
        .insert({
            "user_id": user_id,
            "mode": mode,
            "motif_name": motif_name,
            "prompt": prompt,
            "image_url": image_url,
            "philosophy": philosophy,
            "density": density
        })
        .execute()
    )

    return result