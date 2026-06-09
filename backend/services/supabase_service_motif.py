from backend.config.supabase import supabase

def save_design(
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