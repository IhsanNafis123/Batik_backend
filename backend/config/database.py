import os
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")

if not url or not key:
    raise ValueError("SUPABASE_URL atau SUPABASE_KEY tidak ditemukan di file .env")

supabase = create_client(url, key)
print("Supabase terhubung dengan sukses!")

# Hapus atau ubah baris yang mendefinisikan users_collection jika tidak ada