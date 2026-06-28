from flask import request, jsonify

from backend.utils.jwt_helper import verify_token

from backend.services.dataset_service import (
    get_all_motifs,
    motif_exists
)

from backend.services.vision_service import (
    extract_average_features
)

from backend.services.flux_service import (
    build_flux_prompt,
    generate_flux_image
)

from backend.services.clip_service import get_top_reference_paths

from backend.services.philosophy_service import (
    generate_philosophy
)

from backend.services.supabase_service_motif import (
    save_design
)

from backend.services.activity_log_service import (
    save_activity
)


# ===================================================
# GET MOTIF
# ===================================================

def get_motifs():

    return jsonify({

        "success": True,

        "data": get_all_motifs()

    })


# ===================================================
# GENERATE DESIGN
# ===================================================

def generate_design():

    try:

        data = request.get_json() or {}

        mode = data.get(
            "mode",
            "prompt"
        ).lower()

        prompt = data.get(
            "prompt",
            ""
        ).strip()

        base_motif = data.get(
            "base_motif",
            ""
        ).strip()

        if prompt == "":

            return jsonify({

                "success": False,

                "message":
                "Prompt wajib diisi"

            }),400


        # ==========================================
        # PROMPT ONLY
        # ==========================================

        if mode == "prompt":

            final_prompt = build_flux_prompt(

                mode="prompt",

                prompt=prompt

            )

            philosophy = generate_philosophy(

                "prompt",

                "",

                prompt

            )

            motif_result = ""


        # ==========================================
        # HYBRID
        # ==========================================

        else:

            if base_motif == "":

                return jsonify({

                    "success": False,

                    "message":
                    "Silakan pilih motif batik."

                }),400


            if not motif_exists(base_motif):

                return jsonify({

                    "success": False,

                    "message":
                    "Motif tidak ditemukan."

                }),404


            # ======================================
            # CLIP SEARCH
            # ======================================

            reference_images = get_top_reference_paths(
                motif_name=base_motif,
                prompt=prompt,
                top_k=3
            )
            if len(reference_images) == 0:

                return jsonify({

                    "success": False,

                    "message": "Referensi gambar tidak ditemukan."

                }), 404
                print("=" * 60)
                print(reference_images)
                print(type(reference_images))

                if len(reference_images) > 0:
                    print(type(reference_images[0]))
                    print(reference_images[0])

                print("=" * 60)
            _ = extract_average_features(reference_images)


            clean_name = base_motif.replace(
                "_",
                " "
            ).title()


            final_prompt = build_flux_prompt(

                mode="hybrid",

                prompt=prompt,

                motif_name=clean_name

            )


            philosophy = generate_philosophy(

                "hybrid",

                clean_name,

                prompt

            )


            motif_result = clean_name


        # ==========================================
        # FLUX GENERATION
        # ==========================================

        image_url = generate_flux_image(
            final_prompt
        )


        print("="*70)
        print("MODE :", mode)
        print("MOTIF :", motif_result)
        print("PROMPT :", prompt)
        print("IMAGE :", image_url)
        print("="*70)


        return jsonify({

            "success": True,

            "data":{

                "mode": mode,

                "motif": motif_result,

                "image": image_url,

                "philosophy": philosophy,

                "density": "98%"

            }

        })


    except Exception as e:

        print(e)

        return jsonify({

            "success": False,

            "message": str(e)

        }),500


# ===================================================
# SAVE DESIGN
# ===================================================

def save_generated_design():

    try:

        auth_header = request.headers.get(
            "Authorization"
        )

        if not auth_header:

            return jsonify({

                "success": False,

                "message":
                "Token tidak ditemukan"

            }),401


        token = auth_header.split(" ")[1]

        payload = verify_token(token)

        user_id = payload["user_id"]

        data = request.get_json()


        save_design(

            user_id=user_id,

            mode=data["mode"],

            motif_name=data["motif_name"],

            prompt=data["prompt"],

            image_url=data["image_url"],

            philosophy=data["philosophy"],

            density=data["density"]

        )
        save_activity(

            user_id=user_id,

            activity="GENERATE_DESIGN",

            description=f"Membuat desain batik {data['motif_name']}"

        )


        return jsonify({

            "success": True,

            "message":
            "Design berhasil disimpan"

        })


    except Exception as e:

        return jsonify({

            "success": False,

            "message":
            str(e)

        }),500