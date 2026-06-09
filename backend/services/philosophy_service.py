import os
import google.generativeai as genai

# Konfigurasi API Key Gemini
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Inisialisasi Model
model = genai.GenerativeModel("gemini-2.5-flash")

def generate_philosophy(motif_name, prompt):
    try:
        # Prompt untuk AI
        instruction = f"""
        Kamu adalah ahli filosofi dan budaya batik Indonesia.

        Motif Dasar:
        {motif_name}

        Desain Batik:
        {prompt}

        Tugas:
        - Buat filosofi batik dalam bahasa Indonesia.
        - Maksimal 100 kata.
        - Jangan gunakan markdown.
        - Jangan gunakan tanda **.
        - Jangan gunakan tanda kutip.
        - Jangan menggunakan bullet point.
        - Tulis dalam satu paragraf yang rapi.
        - Fokus pada makna budaya, estetika, dan nilai yang terkandung dalam desain.
        """
        
        response = model.generate_content(instruction)
        philosophy = response.text

        # Pembersihan teks dari karakter yang tidak diinginkan
        philosophy = philosophy.replace("**", "")
        philosophy = philosophy.replace('"', "")
        philosophy = philosophy.strip()

        return philosophy

    except Exception as e:
        print(f"Error pada generate_philosophy: {str(e)}")
        return "Filosofi tidak dapat digenerate karena terjadi kesalahan teknis."