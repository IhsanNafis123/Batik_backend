import os
import fal_client
from backend.services.storage_service import upload_base64_image

# ==========================================================
# FAL CONFIG
# ==========================================================

FAL_KEY = os.getenv("FAL_KEY")

if not FAL_KEY:
    raise ValueError(
        "FAL_KEY tidak ditemukan pada file .env"
    )

os.environ["FAL_KEY"] = FAL_KEY


# ==========================================================
# BUILD PROMPT
# ==========================================================

def build_flux_prompt(
    mode,
    prompt,
    motif_name=""
):

    # ======================================================
    # PROMPT ONLY
    # ======================================================
    if mode == "prompt":
        return (
            f"A creative and artistic reimagining of {prompt}. "
            f"The entire shape and structure of {prompt} is completely made out of zxcv_batik fabric pattern. "
            f"Intricate traditional Indonesian batik art forming the object. "
            f"Elegant ornament, luxury textile texture, premium fabric quality, highly detailed."
        )

    return (
        f"A creative and artistic reimagining of {prompt}. "
        f"The entire shape and structure of {prompt} is intricately crafted and filled with a seamless blend of zxcv_batik pattern and traditional {motif_name} motif. "
        f"It looks like a masterpiece of Indonesian batik art perfectly molded into the shape of {prompt}. "
        f"Elegant ornament, luxury textile texture, highly detailed."
    )


# ==========================================================
# GENERATE IMAGE
# ==========================================================

def generate_flux_image(prompt):
    """
    Fungsi untuk memanggil FLUX LoRA di fal.ai menggunakan model dataset sendiri
    """
    try:
        result = fal_client.subscribe(
            "fal-ai/flux-lora",
            arguments={
                "prompt": prompt,
                "image_size": "square_hd", # Bisa diganti "landscape_4_3" atau "portrait_4_3"
                "loras": [
                    {
                        # URL safetensors dari hasil training Anda
                        "path": "https://v3b.fal.media/files/b/0aa0acd9/4q94o1AB9BItvN6H72ChJ_pytorch_lora_weights.safetensors",
                        "scale": 1.2 # Kekuatan motif batik (bisa dinaikkan max 1.2 jika kurang kuat)
                    }
                ]
            },
        )
        
        # Ambil URL gambar hasil dari fal.ai
        image_url = result['images'][0]['url']
        return image_url
        
    except Exception as e:
        print(f"Error dari fal.ai: {e}")
        raise Exception("Gagal menghasilkan gambar dari server AI.")


# ==========================================================
# DEBUG PROMPT
# ==========================================================

def preview_prompt(
    mode,
    prompt,
    motif_name=""
):

    final_prompt = build_flux_prompt(
        mode=mode,
        prompt=prompt,
        motif_name=motif_name
    )

    print("=" * 80)
    print("FINAL PROMPT")
    print("=" * 80)
    print(final_prompt)
    print("=" * 80)

    return final_prompt