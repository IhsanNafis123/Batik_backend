from flask import Blueprint, jsonify
from backend.controllers.gallery_controller import get_all_designs
from backend.config.database import supabase
from collections import Counter
from datetime import datetime
import random

# Inisialisasi Blueprint untuk rute galeri
gallery_bp = Blueprint("gallery_bp", __name__)

# Endpoint untuk Halaman Galeri
@gallery_bp.route("/api/gallery", methods=["GET"])
def fetch_gallery():
    return get_all_designs()

# Endpoint untuk Halaman Beranda (Home)
@gallery_bp.route('/api/home-trends', methods=['GET'])
def get_home_trends():
    tiktok_viral = []
    
    # =========================================================
    # 1. AMBIL TREN TIKTOK (VIRAL SEPANJANG MASA)
    # =========================================================
    try:
        # Hapus filter bulan, ambil semua data yang berawalan tiktok_views_
        res = supabase.table("analytics").select("*").like("metric_name", "tiktok_views_%").execute()
        
        if res.data:
            # Urutkan dari views terbesar ke terkecil
            sorted_tiktok = sorted(res.data, key=lambda x: int(x['metric_value']), reverse=True)
            
            # Gunakan 'set' agar jika ada motif yang sama di bulan 5 dan 6, tidak muncul dua kali
            seen_motifs = set()
            
            for row in sorted_tiktok:
                nama_motif = row['metric_name'].replace('tiktok_views_', '').title()
                
                # Jika motif belum masuk ke daftar, masukkan!
                if nama_motif not in seen_motifs:
                    seen_motifs.add(nama_motif)
                    views = int(row['metric_value'])
                    
                    if views >= 1000000:
                        views_text = f"{views / 1000000:.1f}M Views"
                    elif views >= 1000:
                        views_text = f"{views / 1000:.1f}K Views"
                    else:
                        views_text = f"{views} Views"

                    tiktok_viral.append({
                        "motif": nama_motif,
                        "views": views_text
                    })
                
                # Batasi hanya 3 motif teratas
                if len(tiktok_viral) == 3:
                    break
    except Exception as e:
        print(f"Error TikTok Viral: {e}")

    # =========================================================
    # 2. AMBIL DATA KOMUNITAS, MOTIF, DAN ARTIKEL (DESAIN)
    # =========================================================
    try:
        # A. TREN KOMUNITAS (5 Desain Terbaru)
        community_response = supabase.table('designs').select('*, users(name, avatar)').order('created_at', desc=True).limit(5).execute()
        community_data = []
        if community_response.data:
            for row in community_response.data:
                community_data.append({
                    'title': row.get('motif_name', 'Batik Tanpa Nama'),
                    'creator': row['users']['name'] if row.get('users') else 'Anonim',
                    'image': row.get('image_url', ''),
                    'likes': str(random.randint(50, 300)) 
                })

        # B. TOP 5 MOTIF (Tren)
        motifs_response = supabase.table('designs').select('motif_name').execute()
        trending_motifs_data = []
        if motifs_response.data:
            semua_motif = [r['motif_name'] for r in motifs_response.data if r.get('motif_name')]
            motif_counter = Counter(semua_motif)
            top_5 = motif_counter.most_common(5)
            for motif, count in top_5:
                trending_motifs_data.append({
                    'name': motif,
                    'origin': 'Batikfly', 
                    'image': 'assets/batik_pattern.png'
                })

        # C. ARTIKEL (MENGGUNAKAN TABEL DESIGNS)
        designs_response = supabase.table('designs').select('*').order('created_at', desc=True).limit(5).execute()
        articles_data = []
        if designs_response.data:
            for row in designs_response.data:
                articles_data.append({
                    "title": row.get("motif_name", "Batik AI"),
                    "philosophy": row.get("prompt", "Hasil karya desain batik dari pengguna BatikFly..."),
                    "image_url": row.get("image_url", "")
                })

        # =========================================================
        # 3. KEMBALIKAN DATA KE FLUTTER (Ini yang sebelumnya hilang)
        # =========================================================
        return jsonify({
            "success": True,
            "data": {
                "community": community_data,
                "motifs": trending_motifs_data,
                "articles": articles_data,
                "tiktok_viral": tiktok_viral
            }
        }), 200

    except Exception as e:
        print("============= ERROR DI HOME TRENDS =============")
        print(str(e))
        print("================================================")
        return jsonify({"success": False, "message": str(e)}), 500