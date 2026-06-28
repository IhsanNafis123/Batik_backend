from flask import request, jsonify
from backend.config.database import supabase
from backend.services.upload_service import upload_image_to_supabase
import fal_client
import os

def upload_motif():
    try:
        if "image" not in request.files:
            return jsonify({"success": False, "message": "File tidak ditemukan"}), 400

        image = request.files["image"]
        folder = request.form.get("folder", "motifs")

        success, url, error = upload_image_to_supabase(image, folder=folder)

        if not success:
            return jsonify({"success": False, "message": error}), 500

        return jsonify({"success": True, "motif_url": url})

    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500
        
def generate_vton():
    try:
        data = request.get_json()
        print("DEBUG: Data VTON diterima:", data)

        user_id = data.get("user_id") 
        user_photo_url = data.get("user_photo_url")
        motif_url = data.get("batik_motif_url") 

        if not user_photo_url:
            return jsonify({"success": False, "message": "user_photo_url tidak ditemukan"}), 400

        if not motif_url:
            return jsonify({"success": False, "message": "batik_motif_url tidak ditemukan"}), 400

        print("========== MEMANGGIL FAL AI ==========")
        result = fal_client.subscribe(
            "fal-ai/idm-vton",
            arguments={
                "human_image_url": user_photo_url,
                "garment_image_url": motif_url,
                "description": "Traditional Indonesian batik shirt",
                "garment_des": "Traditional Indonesian batik fabric"
            },
            with_logs=True
        )

        result_url = None
        if "image" in result:
            result_url = result["image"]["url"]
        elif "images" in result:
            if len(result["images"]) > 0:
                result_url = result["images"][0]["url"]

        if result_url is None:
            return jsonify({"success": False, "message": "Fal AI gagal", "result": result}), 500

        try:
            supabase.table("fittings").insert({
                "user_id": user_id,
                "user_photo_url": user_photo_url,
                "motif_url": motif_url,
                "result_url": result_url,
                "model": "VTON",
                "size": "-",
                "material": "-",
                "fabric_length": 0,
                "fitting_type": "VTON"
            }).execute()
        except Exception as db_error:
            print("DATABASE ERROR:", db_error)

        return jsonify({"success": True, "message": "Virtual Try-On berhasil", "result_url": result_url})

    except Exception as e:
        print("========== ERROR VTON ==========", e)
        return jsonify({"success": False, "message": str(e)}), 500

def simpan_fitting():
    print("DEBUG: Function simpan_fitting dipanggil!")
    try:
        data = request.json
        user_id = data.get('user_id')
        motif_url = data.get('motif_url')
        size = data.get('size')
        model = data.get("model")

        if not motif_url or not size or not model:
            return jsonify({"error": "Data tidak lengkap."}), 400

        if user_id == "anonymous" or not user_id:
            user_id = None

        supabase.table("fittings").insert({
            "user_id": user_id,
            "motif_url": motif_url,
            "model": model,
            "size": size,
            "material": "Katun Primissima",
            "fabric_length": 2.0,
            "fitting_type": "3D"
        }).execute()
                
        return jsonify({
            "success": True,
            "message": "Data fitting berhasil disimpan",
            "data_render": {
                "model_url": model,
                "motif_url": motif_url
            },
            "fabric": 2.0,
            "material": "Katun Primissima"
        })

    except Exception as e:
        print("ERROR LENGKAP:", str(e)) 
        return jsonify({"error": str(e)}), 500