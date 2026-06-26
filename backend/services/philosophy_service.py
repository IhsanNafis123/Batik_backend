import os
import google.generativeai as genai

# ==========================================
# GEMINI CONFIG
# ==========================================

genai.configure(
    api_key=os.getenv("GEMINI_API_KEY")
)

model = genai.GenerativeModel(
    "gemini-2.5-flash"
)

# ==========================================
# GENERATE PHILOSOPHY
# ==========================================

def generate_philosophy(
    mode,
    motif_name,
    prompt
):

    try:

        if mode == "prompt":

            instruction = f"""
            Kamu adalah ahli budaya batik Indonesia.

            Pengguna membuat desain batik menggunakan AI.

            Deskripsi desain:
            {prompt}

            Tugasmu:

            Buat filosofi batik berdasarkan desain tersebut.

            Aturan:

            - Bahasa Indonesia.
            - Maksimal 100 kata.
            - Satu paragraf.
            - Jangan menggunakan markdown.
            - Jangan menggunakan bullet point.
            - Jangan menggunakan tanda kutip.
            - Fokus pada nilai budaya, estetika, kreativitas, dan makna simbolik desain.
            """

        else:

            instruction = f"""
            Kamu adalah ahli budaya batik Indonesia.

            Motif dasar batik:

            {motif_name}

            Keinginan pengguna:

            {prompt}

            Tugasmu:

            Buat filosofi batik yang menjelaskan perpaduan antara karakteristik motif {motif_name} dengan desain modern dari pengguna.

            Aturan:

            - Bahasa Indonesia.
            - Maksimal 100 kata.
            - Satu paragraf.
            - Jangan menggunakan markdown.
            - Jangan menggunakan bullet point.
            - Jangan menggunakan tanda kutip.
            - Jelaskan makna budaya motif batik.
            - Jelaskan hubungan antara motif tradisional dengan inovasi desain pengguna.
            """

        response = model.generate_content(
            instruction
        )

        philosophy = response.text.strip()

        philosophy = philosophy.replace("**", "")
        philosophy = philosophy.replace('"', "")
        philosophy = philosophy.replace("\n", " ")

        return philosophy

    except Exception as e:

        print(
            "Gemini Error:",
            e
        )

        return (
            "Filosofi tidak dapat dibuat karena terjadi kesalahan pada layanan AI."
        )