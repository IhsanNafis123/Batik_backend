import os
import pickle
import torch

from transformers import CLIPModel, CLIPProcessor
from sklearn.metrics.pairwise import cosine_similarity

# =====================================================
# CONFIG
# =====================================================

CACHE_PATH = "backend/dataset/clip_embeddings.pkl"

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

print(f"CLIP Running on : {DEVICE}")

# =====================================================
# LOAD MODEL
# =====================================================

processor = CLIPProcessor.from_pretrained(
    "openai/clip-vit-base-patch32"
)

model = CLIPModel.from_pretrained(
    "openai/clip-vit-base-patch32"
).to(DEVICE)

model.eval()

# =====================================================
# CACHE
# =====================================================

embedding_cache = {}

# =====================================================
# LOAD CACHE
# =====================================================

def load_embedding_cache():

    global embedding_cache

    if not os.path.exists(CACHE_PATH):

        raise Exception(
            "clip_embeddings.pkl belum dibuat.\n"
            "Jalankan build_clip_embedding.py terlebih dahulu."
        )

    with open(CACHE_PATH, "rb") as f:

        embedding_cache = pickle.load(f)

    print("=" * 60)
    print("CLIP Cache Loaded")
    print(f"Motif  : {len(embedding_cache)}")

    total = sum(

        len(v)

        for v in embedding_cache.values()

    )

    print(f"Gambar : {total}")
    print("=" * 60)

# =====================================================
# NORMALIZE
# =====================================================

def normalize_motif_name(name):

    return name.strip().replace(" ", "_")

# =====================================================
# TEXT EMBEDDING
# =====================================================

def encode_text(text):

    inputs = processor(

        text=[text],

        return_tensors="pt",

        padding=True,

        truncation=True

    )

    inputs = {

        k: v.to(DEVICE)

        for k, v

        in inputs.items()

    }

    with torch.no_grad():

        embedding = model.get_text_features(

            **inputs

        )

        embedding = torch.nn.functional.normalize(

            embedding,

            p=2,

            dim=-1

        )

    return embedding.squeeze().cpu().numpy()

# =====================================================
# SEARCH
# =====================================================

def search_reference_images(

    motif_name,

    prompt,

    top_k=3

):

    motif_name = normalize_motif_name(

        motif_name

    )

    if motif_name not in embedding_cache:

        return []

    query = f"""

    Indonesian Batik

    Motif :

    {motif_name}

    User Request :

    {prompt}

    """

    text_embedding = encode_text(

        query

    )

    results = []

    for item in embedding_cache[motif_name]:

        score = cosine_similarity(

            [text_embedding],

            [item["embedding"]]

        )[0][0]

        results.append({

            "path": item["path"],

            "score": float(score)

        })

    results.sort(

        key=lambda x: x["score"],

        reverse=True

    )

    return results[:top_k]

# =====================================================
# PATH ONLY
# =====================================================

def get_top_reference_paths(

    motif_name,

    prompt,

    top_k=3

):

    result = search_reference_images(

        motif_name,

        prompt,

        top_k

    )

    return [

        item["path"]

        for item in result

    ]

# =====================================================
# CACHE INFO
# =====================================================

def cache_info():

    total = sum(

        len(v)

        for v

        in embedding_cache.values()

    )

    return {

        "motif": len(

            embedding_cache

        ),

        "images": total

    }