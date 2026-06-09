from flask import request, jsonify
from backend.config.database import supabase
import fal_client
import os

def generate_vton():
    try:
        data = request.json
        print("Data diterima:", data) 
        
        user_photo_url = data.get('user_photo_url')
        batik_motif_url = data.get('motif_url')
        
        if not user_photo_url or not batik_motif_url:
            return jsonify({"error": "Data kosong"}), 400

        print("Memanggil Fal.ai...") 
        handler = fal_client.submit(
            "fal-ai/idm-vton",
            arguments={
                "human_image_url": user_photo_url,
                "garment_image_url": batik_motif_url,
                "category": "upper_body",
                "description": "A stylish shirt with Indonesian batik pattern" # <-- INI SOLUSINYA
            }
        )
        result = handler.get()
        return jsonify({"status": "success", "result_url": result['image']['url']})

    except Exception as e:
        print("ERROR LENGKAP:", str(e)) 
        return jsonify({"error": str(e)}), 500

def simpan_fitting():
    try:
        data = request.json
        print("Data yang diterima:", data)
        
        user_id = data.get('user_id')
        motif_url = data.get('motif_url')
        size = data.get('size')

        if not motif_url or not size:
            return jsonify({"error": "Data tidak lengkap"}), 400

        # MENCEGAH ERROR UUID: 
        # Jika Flutter mengirim "anonymous" (karena user belum login), kita ubah menjadi None (NULL)
        # karena Supabase akan menolak teks biasa masuk ke kolom UUID.
        if user_id == "anonymous":
            user_id = None

        # MENYIMPAN KE DATABASE (Nama kolom Disesuaikan dengan Gambar ke-3)
        supabase.table('fittings').insert({
            "user_id": user_id,
            "batik_motif_url": motif_url,  # <-- Menggunakan batik_motif_url
            "size": size
            # shirt_3d_url tidak perlu diisi (otomatis NULL)
        }).execute()
        
        print("Data berhasil divalidasi dan disimpan!")
        return jsonify({"status": "success", "message": "Berhasil disimpan"}), 200

    except Exception as e:
        print("ERROR SAVE FITTING:", str(e)) 
        return jsonify({"error": str(e)}), 500