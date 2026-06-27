import os
import pickle
import torch

from PIL import Image
from transformers import CLIPModel, CLIPProcessor

# =====================================================
# CONFIG
# =====================================================

DATASET_PATH = "backend/dataset/train"

OUTPUT_FILE = "backend/dataset/clip_embeddings.pkl"

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

print(f"Running on : {DEVICE}")

# =====================================================
# LOAD CLIP
# =====================================================

processor = CLIPProcessor.from_pretrained(
    "openai/clip-vit-base-patch32"
)

model = CLIPModel.from_pretrained(
    "openai/clip-vit-base-patch32"
).to(DEVICE)

model.eval()

# =====================================================
# ENCODE IMAGE
# =====================================================

def encode_image(image_path):

    image = Image.open(image_path).convert("RGB")

    inputs = processor(
        images=image,
        return_tensors="pt"
    )

    inputs = {
        k: v.to(DEVICE)
        for k, v in inputs.items()
    }

    with torch.no_grad():

        embedding = model.get_image_features(
            **inputs
        )

        embedding = torch.nn.functional.normalize(
            embedding,
            p=2,
            dim=-1
        )

    return embedding.squeeze().cpu().numpy()

# =====================================================
# BUILD EMBEDDING
# =====================================================

def build():

    cache = {}

    total_image = 0

    print("=" * 60)
    print("BUILD CLIP EMBEDDING")
    print("=" * 60)

    for motif in sorted(os.listdir(DATASET_PATH)):

        motif_folder = os.path.join(
            DATASET_PATH,
            motif
        )

        if not os.path.isdir(motif_folder):
            continue

        print(f"Loading {motif}")

        cache[motif] = []

        for file in sorted(os.listdir(motif_folder)):

            if not file.lower().endswith(
                (
                    ".jpg",
                    ".jpeg",
                    ".png",
                    ".webp"
                )
            ):
                continue

            image_path = os.path.join(
                motif_folder,
                file
            )

            try:

                embedding = encode_image(
                    image_path
                )

                cache[motif].append({

                    "path": image_path,

                    "embedding": embedding

                })

                total_image += 1

            except Exception as e:

                print(f"Gagal : {image_path}")

                print(e)

        print(
            f"{motif} : {len(cache[motif])} gambar"
        )

    # ===========================
    # SIMPAN
    # ===========================

    with open(
        OUTPUT_FILE,
        "wb"
    ) as f:

        pickle.dump(
            cache,
            f
        )

    print("=" * 60)
    print("Embedding berhasil disimpan")
    print(f"File   : {OUTPUT_FILE}")
    print(f"Motif  : {len(cache)}")
    print(f"Gambar : {total_image}")
    print("=" * 60)


if __name__ == "__main__":

    build()