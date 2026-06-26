import os

DATASET_PATH = "backend/dataset/train"


# ==========================================
# GET SEMUA NAMA MOTIF
# ==========================================

def get_all_motifs():

    if not os.path.exists(DATASET_PATH):
        return []

    motifs = []

    for folder in os.listdir(DATASET_PATH):

        folder_path = os.path.join(
            DATASET_PATH,
            folder
        )

        if os.path.isdir(folder_path):
            motifs.append(folder)

    return sorted(motifs)


# ==========================================
# GET SEMUA GAMBAR DARI MOTIF
# ==========================================

def get_reference_images(motif_name):

    folder = os.path.join(
        DATASET_PATH,
        motif_name
    )

    if not os.path.exists(folder):
        return []

    image_list = []

    for img in os.listdir(folder):

        if img.lower().endswith(
            (
                ".jpg",
                ".jpeg",
                ".png",
                ".webp"
            )
        ):

            image_list.append(

                os.path.join(
                    folder,
                    img
                )

            )

    return sorted(image_list)


# ==========================================
# VALIDASI MOTIF
# ==========================================

def motif_exists(motif_name):

    folder = os.path.join(
        DATASET_PATH,
        motif_name
    )

    return os.path.isdir(folder)


# ==========================================
# TOTAL GAMBAR DALAM MOTIF
# ==========================================

def count_images(motif_name):

    return len(
        get_reference_images(
            motif_name
        )
    )