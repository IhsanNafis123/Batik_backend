from flask import request, jsonify

from backend.services.flux_service import generate_flux_image
from backend.services.philosophy_service import generate_philosophy
from backend.services.dataset_service import get_all_motifs, get_random_reference
from backend.services.vision_service import extract_features


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