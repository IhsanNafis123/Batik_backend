import os
import random

DATASET_PATH = "backend/dataset/train"


def get_all_motifs():

    return sorted([

        folder

        for folder in os.listdir(
            DATASET_PATH
        )

        if os.path.isdir(
            os.path.join(
                DATASET_PATH,
                folder
            )
        )
    ])


def get_random_reference(
    motif_name
):

    folder = os.path.join(

        DATASET_PATH,

        motif_name
    )

    images = [

        os.path.join(
            folder,
            img
        )

        for img in os.listdir(folder)

        if img.lower().endswith(
            (
                ".jpg",
                ".jpeg",
                ".png"
            )
        )
    ]

    if not images:
        return None

    return random.choice(images)