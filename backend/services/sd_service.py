import base64
import fal_client

def get_base64_data_uri(image_path):
    """Mengubah gambar dataset lokal menjadi format yang bisa dibaca oleh API Fal.ai"""
    try:
        with open(image_path, "rb") as img_file:
            encoded_string = base64.b64encode(img_file.read()).decode('utf-8')
            
        mime_type = "image/jpeg"
        if image_path.lower().endswith(".png"):
            mime_type = "image/png"
            
        return f"data:{mime_type};base64,{encoded_string}"
    except Exception as e:
        raise Exception(f"Gagal membaca gambar referensi lokal: {str(e)}")


def generate_sd_hybrid_image(prompt, image_path):
    """
    Fungsi untuk menjalankan Stable Diffusion Image-to-Image
    """
    try:
        # 1. Ubah gambar dataset lokal ke Data URI
        image_data_uri = get_base64_data_uri(image_path)
        
        # 2. Tembak endpoint Stable Diffusion XL Image-to-Image di Fal.ai
        result = fal_client.subscribe(
            "fal-ai/fast-sdxl/image-to-image",
            arguments={
                # Modifikasi prompt agar lebih ramah SDXL:
                "prompt": f"masterpiece, highly detailed indonesian batik textile pattern, {prompt}", 
                "image_url": image_data_uri,
                "strength": 0.60, # 👈 Turunkan jadi 0.60
                "image_size": "square_hd"
            },
            with_logs=True
        )
        
        return result.get('images')[0]['url']
        
    except Exception as e:
        raise Exception(f"Gagal generate gambar dari Stable Diffusion: {str(e)}")