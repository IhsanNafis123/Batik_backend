import os
import fal_client

# ==========================================================
# FAL CONFIG
# ==========================================================

FAL_KEY = os.getenv("FAL_KEY")

if not FAL_KEY:
    raise ValueError("FAL_KEY tidak ditemukan pada file .env")

os.environ["FAL_KEY"] = FAL_KEY

# ==========================================================
# BUILD PROMPT
# ==========================================================

def build_flux_prompt(mode, prompt, motif_name=""):
    
    if mode == "prompt":
        return (
            f"A creative and artistic reimagining of {prompt}. "
            f"The entire shape and structure is intricately crafted and completely filled with {motif_name} batik pattern. "
            f"Deeply inspired by Indonesian cultural art, seamless layout, luxury textile texture, zxcv_batik."
        )

    # ======================================================
    # MODE AUTHENTIC
    # ======================================================
    return (
        f"zxcv_batik, pure authentic {motif_name} traditional batik. "
        f"The background MUST strictly use the exact {motif_name} pattern from the training dataset. "
        f"ONLY draw {prompt} using a flat 2D textile style. "
        f"CRITICAL: Do not add water, do not add leaves, do not add generic floral environments. "
        f"Focus entirely on the authentic {motif_name} structural lines, highly detailed fabric masterpiece."
    )

# ==========================================================
# GENERATE IMAGE
# ==========================================================

def generate_flux_image(prompt, reference_image_url=None):
    try:
        payload_arguments = {
            "prompt": prompt,
            "image_size": "square_hd",
            "num_inference_steps": 28,
            "guidance_scale": 3.5, # Menggunakan standar default FLUX
            "loras": [
                {
                    "path": "https://v3b.fal.media/files/b/0aa0acd9/4q94o1AB9BItvN6H72ChJ_pytorch_lora_weights.safetensors",
                    "scale": 1.0 # Dikembalikan ke 1.0 agar tekstur tidak gosong/rusak
                }
            ]
        }

        if reference_image_url and reference_image_url.strip() != "":
            # MENGGUNAKAN EASYCONTROLS UNTUK FLUX-GENERAL
            payload_arguments["easycontrols"] = [
                {
                    "control_method_url": "canny",
                    "image_url": reference_image_url,
                    "image_control_type": "spatial",
                    "scale": 0.4 # DITURUNKAN DRASTIS! Agar AI masih punya ruang untuk mewarnai ikan
                }
            ]
            endpoint = "fal-ai/flux-general" # Endpoint yang mendukung semua kombinasi
        else:
            endpoint = "fal-ai/flux-lora"

        result = fal_client.subscribe(
            endpoint,
            arguments=payload_arguments,
        )
        
        return result['images'][0]['url']
        
    except Exception as e:
        print(f"Error dari fal.ai: {e}")
        raise Exception("Gagal menghasilkan gambar dari server AI.")

# ==========================================================
# DEBUG PROMPT
# ==========================================================

def preview_prompt(mode, prompt, motif_name=""):
    final_prompt = build_flux_prompt(mode=mode, prompt=prompt, motif_name=motif_name)
    print("=" * 80)
    print("FINAL PROMPT\n", final_prompt)
    print("=" * 80)
    return final_prompt
