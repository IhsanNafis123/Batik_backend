from flask import request, jsonify

from backend.utils.jwt_helper import verify_token
from backend.services.flux_service import generate_flux_image
from backend.services.philosophy_service import generate_philosophy
from backend.services.dataset_service import get_all_motifs, get_random_reference
from backend.services.vision_service import extract_features
from backend.services.supabase_service_motif import (save_design)


def get_motifs():
    motifs = get_all_motifs()
    return jsonify({
        "success": True,
        "data": motifs
    })


def generate_design():
    try:
        # 1. Ambil data dari request json
        data = request.get_json() or {}
        mode = data.get("mode", "prompt")
        prompt = data.get("prompt", "")
        base_motif = data.get("base_motif", "")

        # 2. Validasi input (Sekarang sudah masuk ke dalam blok try dengan benar)
        if prompt.strip() == "":
            return jsonify({
                "success": False,
                "message": "Prompt wajib diisi"
            }), 400

        # ==========================
        # PROMPT ONLY
        # ==========================
        if mode == "prompt":
            final_prompt = f"""
            Indonesian Batik Pattern
            {prompt}
            traditional batik
            seamless textile
            luxury ornament
            highly detailed
            premium fabric pattern
            symmetrical composition
            """

            philosophy = generate_philosophy("Custom Batik", prompt)
            motif_result = ""

        # ==========================
        # HYBRID + COMPUTER VISION
        # ==========================
        else:
            reference_image = get_random_reference(base_motif)
            visual_signature = ""

            if reference_image:
                features = extract_features(reference_image)
                visual_signature = str(features[:20])

            clean_motif_name = base_motif.replace("_", " ").strip().title()

            final_prompt = f"""
            Indonesian Batik Pattern
            Inspired by:
            {clean_motif_name}
            User Style:
            {prompt}
            Visual Characteristics:
            {visual_signature}
            preserve traditional
            batik identity
            seamless textile
            highly detailed
            premium ornament
            luxury pattern
            """

            philosophy = generate_philosophy(clean_motif_name, prompt)
            motif_result = clean_motif_name

        # 3. Generate Image memakai Flux
        image_url = generate_flux_image(final_prompt)

        # Logging ke konsol untuk kebutuhan debug
        print("=" * 60)
        print("MODE      :", mode)
        print("MOTIF     :", motif_result)
        print("PROMPT    :", prompt)
        print("IMAGE URL :", image_url)
        print("=" * 60)

        return jsonify({
            "success": True,
            "data": {
                "mode": mode,
                "motif": motif_result,
                "image": image_url,
                "philosophy": philosophy,
                "density": "98%"
            }
        })

    except Exception as e:
        print(f"Error pada generate_design: {str(e)}")
        return jsonify({
            "success": False,
            "message": str(e)
        }), 500
        
def save_generated_design():

    try:

        auth_header = request.headers.get("Authorization")

        if not auth_header:
            return jsonify({
                "success": False,
                "message": "Token tidak ditemukan"
            }), 401

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

        }), 500