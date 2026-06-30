import os
from datetime import datetime
from collections import Counter
from flask import render_template, session, redirect, jsonify
from supabase import create_client, Client
from flask import jsonify
# --- Setup Supabase ---
supabase_url = os.environ.get("SUPABASE_URL")
supabase_key = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(supabase_url, supabase_key)

# Fungsi bantuan untuk menerjemahkan angka bulan ke nama bulan Indonesia
def get_nama_bulan(angka_bulan, tahun):
    bulan_indo = ["", "Januari", "Februari", "Maret", "April", "Mei", "Juni", 
                  "Juli", "Agustus", "September", "Oktober", "November", "Desember"]
    return f"{bulan_indo[angka_bulan]} {tahun}"

def get_mobile_analytics():
    # =========================================================
    # KUMPULKAN SEMUA DATA SEPERTI DI DASHBOARD WEB
    # =========================================================
    
    # 1. Total Data
    try:
        total_users = supabase.table("users").select("*", count="exact").execute().count or 0
        total_designs = supabase.table("designs").select("*", count="exact").execute().count or 0
        total_fittings = supabase.table("fittings").select("*", count="exact").execute().count or 0
    except:
        total_users, total_designs, total_fittings = 0, 0, 0

    # 2. Tren Motif (Top 5)
    trending_motifs = []
    top_motif_name = "Belum Ada"
    try:
        motifs_data = supabase.table("designs").select("motif_name").execute()
        if motifs_data.data:
            semua_motif = [row['motif_name'] for row in motifs_data.data if row.get('motif_name')]
            motif_counter = Counter(semua_motif)
            top_5 = motif_counter.most_common(5)
            
            # Format ulang untuk JSON Flutter (List of Dictionaries)
            for motif, count in top_5:
                trending_motifs.append({"name": motif, "count": count})
            
            if top_5:
                top_motif_name = top_5[0][0]
    except Exception as e:
        pass

    # 3. Data TikTok (Bulan Ini Saja Sebagai Contoh)
    today = datetime.today()
    labels_current, values_current = [], []
    try:
        res = supabase.table("analytics").select("*").eq("month", today.month).eq("year", today.year).like("metric_name", "tiktok_views_%").execute()
        for row in res.data:
            labels_current.append(row['metric_name'].replace('tiktok_views_', '').title())
            values_current.append(int(row['metric_value']))
    except:
        pass

    # =========================================================
    # KEMBALIKAN SEBAGAI JSON
    # =========================================================
    return jsonify({
        "success": True,
        "data": {
            "summary": {
                "total_users": total_users,
                "total_designs": total_designs,
                "total_fittings": total_fittings,
                "top_motif": top_motif_name
            },
            "trending_motifs": trending_motifs,
            "tiktok_stats": {
                "labels": labels_current,
                "values": values_current
            }
        }
    }), 200


def analytics_dashboard():
    # 1. Pastikan Admin sudah login
    if "admin" not in session:
        return redirect("/admin/login")
    
     # =========================================================
    # BAGIAN BARU: MENGHITUNG TREN MOTIF (TOP 5)
    # =========================================================
    trending_motifs = []
    top_motif_name = "Belum Ada"

    try:
        # Ambil semua data motif_name dari tabel designs
        motifs_data = supabase.table("designs").select("motif_name").execute()
        
        if motifs_data.data:
            # Kumpulkan semua nama motif ke dalam satu list
            semua_motif = [row['motif_name'] for row in motifs_data.data if row.get('motif_name')]
            
            # Hitung frekuensi masing-masing motif menggunakan Counter
            motif_counter = Counter(semua_motif)
            
            # Ambil 5 motif paling sering muncul (Hasilnya list of tuples: [('Megamendung', 10), ('Parang', 8), ...])
            trending_motifs = motif_counter.most_common(5)
            
            # Ambil juara 1 untuk ditampilkan di kotak statistik paling atas
            if trending_motifs:
                top_motif_name = trending_motifs[0][0]

    except Exception as e:
        print(f"Error saat menghitung tren motif: {e}")

    # =========================================================
    # BAGIAN 1: DATA EKSISTING (TOTAL KOTAK)
    # =========================================================
    try:
        total_users = supabase.table("users").select("*", count="exact").execute().count or 0
    except:
        total_users = 0

    try:
        total_designs = supabase.table("designs").select("*", count="exact").execute().count or 0
    except:
        total_designs = 0

    try:
        total_fittings = supabase.table("fittings").select("*", count="exact").execute().count or 0
    except:
        total_fittings = 0

    # =========================================================
    # BAGIAN BARU: MENGAMBIL DATA ASLI UNTUK GRAFIK DESIGN
    # =========================================================
    design_labels = []
    design_values = []
    
    try:
        # Ambil tanggal pembuatan dari tabel designs
        designs_data = supabase.table("designs").select("created_at").execute()
        
        # Hitung jumlah per bulan
        bulan_counts = Counter()
        for row in designs_data.data:
            # Mengambil bagian tanggal saja (contoh: "2026-06-25")
            date_str = row['created_at'].split('T')[0] 
            date_obj = datetime.strptime(date_str, "%Y-%m-%d")
            
            # Buat kunci dengan format "Tahun-Bulan" (contoh: "2026-06")
            kunci_bulan = f"{date_obj.year}-{date_obj.month:02d}"
            bulan_counts[kunci_bulan] += 1
            
        # Urutkan dari bulan terlama ke terbaru
        sorted_months = sorted(bulan_counts.keys())
        
        bulan_singkat = ["", "Jan", "Feb", "Mar", "Apr", "Mei", "Jun", "Jul", "Ags", "Sep", "Okt", "Nov", "Des"]
        
        for bm in sorted_months:
            tahun, bulan = bm.split('-')
            nama_bln = f"{bulan_singkat[int(bulan)]} {tahun}"
            design_labels.append(nama_bln)
            design_values.append(bulan_counts[bm])
            
        # Jika belum ada data sama sekali di tabel designs
        if not design_labels:
            design_labels = ["Belum ada data"]
            design_values = [0]
            
    except Exception as e:
        print(f"Error mengambil grafik design: {e}")
        design_labels = ["Data Kosong"]
        design_values = [0]

    # Gabungkan ke analytics_data
    analytics_data = {
        "total_users": total_users,
        "total_designs": total_designs,
        "total_fittings": total_fittings,
        "top_motif": top_motif_name, # Sekarang ini dinamis, bukan hardcode lagi
        "trending_motifs": trending_motifs, # Mengirim data Top 5 ke HTML
        "monthly_chart": {
            "labels": design_labels,
            "values": design_values 
        }
    }

    # =========================================================
    # BAGIAN 2: LOGIKA 2 BULAN UNTUK TIKTOK
    # =========================================================
    today = datetime.today()
    
    current_month = today.month
    current_year = today.year
    title_current = get_nama_bulan(current_month, current_year)

    if current_month == 1:
        prev_month = 12
        prev_year = current_year - 1
    else:
        prev_month = current_month - 1
        prev_year = current_year
    title_prev = get_nama_bulan(prev_month, prev_year)

    def get_tiktok_data(m, y):
        try:
            res = supabase.table("analytics").select("*").eq("month", m).eq("year", y).like("metric_name", "tiktok_views_%").execute()
            labels, values = [], []
            for row in res.data:
                labels.append(row['metric_name'].replace('tiktok_views_', '').title())
                values.append(int(row['metric_value']))
            return labels, values
        except:
            return [], []

    labels_prev, values_prev = get_tiktok_data(prev_month, prev_year)
    labels_current, values_current = get_tiktok_data(current_month, current_year)

   

    # =========================================================
    # BAGIAN 3: RENDER KE HTML
    # =========================================================
    return render_template(
        "analytics.html", 
        analytics=analytics_data,
        title_prev=title_prev,
        labels_prev=labels_prev,
        values_prev=values_prev,
        title_current=title_current,
        labels_current=labels_current,
        values_current=values_current
    )