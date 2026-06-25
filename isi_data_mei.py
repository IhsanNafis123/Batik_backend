import os
import random
from supabase import create_client, Client

# PASTIKAN ANDA MENGGANTI INI DENGAN URL DAN KEY SUPABASE ANDA
SUPABASE_URL = "https://cibyndvalwemevzqydxu.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImNpYnluZHZhbHdlbWV2enF5ZHh1Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODE0MzM4NDgsImV4cCI6MjA5NzAwOTg0OH0.APcsJDVMlyzjqWylcXRtoFFbnMKTcR1hvzu57A3ja3k"

try:
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
    motif_list = ["parang", "kawung", "mega mendung", "lasem", "truntum", "pekalongan", "solo", "jogja"]
    
    print("Mulai mengirim data historis Bulan Mei 2026...")
    
    for motif in motif_list:
        # Generate angka acak untuk views (antara 1 juta - 9 juta)
        views = random.randint(1000000, 9500000)
        
        # Kirim ke Supabase
        supabase.table("analytics").insert({
            "metric_name": f"tiktok_views_{motif}",
            "metric_value": str(views),
            "month": 5,
            "year": 2026
        }).execute()
        print(f"✅ Berhasil input {motif} ({views} views)")
        
    print("\n🎉 Selesai! Silakan refresh halaman Analytics web Anda.")

except Exception as e:
    print(f"❌ Terjadi kesalahan: {e}")