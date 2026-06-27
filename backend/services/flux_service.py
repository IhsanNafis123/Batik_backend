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

        return f"""
You are an expert Indonesian batik designer.

Create a completely original premium batik textile.

User Request:
{prompt}

Requirements:

- Traditional Indonesian batik
- Elegant ornament
- Luxury textile
- Highly detailed
- Seamless repeating pattern
- Premium fabric quality
- Symmetrical composition
- Rich Indonesian cultural aesthetics
- Professional textile design
"""


    # ======================================================
    # HYBRID
    # ======================================================

    return f"""
You are an expert Indonesian batik designer.

Reference Motif:
{motif_name}

The generated design MUST preserve the identity
of the {motif_name} motif.

Maintain the traditional characteristics of
{motif_name} while combining them with the
user's creativity.

User Request:
{prompt}

Design Requirements:

- Preserve the original {motif_name} identity
- Traditional Indonesian batik
- Luxury textile
- Elegant ornament
- Premium fabric
- Highly detailed
- Seamless repeating pattern
- Symmetrical composition
- Harmonious color palette
- Professional textile illustration
"""


# ==========================================================
# GENERATE IMAGE
# ==========================================================

def generate_flux_image(prompt):
    print("===== generate_flux_image() DIPANGGIL =====")
    try:

        handler = fal_client.submit(

            "fal-ai/flux/dev",

            arguments={

                "prompt": prompt,

                "image_size": "square_hd",

                "num_images": 1,

                "enable_safety_checker": True,

                "sync_mode": True

            }

        )

        result = handler.get()

        if "images" not in result:

            raise Exception(
                "Flux gagal menghasilkan gambar."
            )

        image_result = result["images"][0]["url"]

        # Jika FAL mengembalikan Base64
        if image_result.startswith("data:image"):

            public_url = upload_base64_image(image_result)

            return public_url

        # Jika FAL sudah mengembalikan URL
        return image_result

    except Exception as e:

        print("=" * 60)
        print("FLUX ERROR")
        print(e)
        print("=" * 60)

        raise Exception(
            f"Generate Flux gagal : {e}"
        )


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