import numpy as np

from tensorflow.keras.applications import EfficientNetB0
from tensorflow.keras.applications.efficientnet import preprocess_input
from tensorflow.keras.preprocessing import image

# ==========================================
# LOAD MODEL SEKALI
# ==========================================

model = EfficientNetB0(
    weights="imagenet",
    include_top=False,
    pooling="avg"
)

# ==========================================
# EXTRACT FEATURE SATU GAMBAR
# ==========================================

def extract_features(img_path):

    img = image.load_img(
        img_path,
        target_size=(224, 224)
    )

    img_array = image.img_to_array(img)

    img_array = np.expand_dims(
        img_array,
        axis=0
    )

    img_array = preprocess_input(
        img_array
    )

    features = model.predict(
        img_array,
        verbose=0
    )

    return features.flatten()


# ==========================================
# EXTRACT FEATURE BANYAK GAMBAR
# ==========================================

def extract_average_features(image_paths):

    if len(image_paths) == 0:
        return ""

    feature_list = []

    for img_path in image_paths:

        try:

            feature = extract_features(
                img_path
            )

            feature_list.append(
                feature
            )

        except Exception as e:

            print(
                f"Gagal membaca {img_path}: {e}"
            )

    if len(feature_list) == 0:
        return ""

    average_feature = np.mean(
        feature_list,
        axis=0
    )

    return average_feature


# ==========================================
# FEATURE -> STRING
# ==========================================

def feature_to_prompt(
    feature_vector,
    length=30
):

    if isinstance(feature_vector, str):
        return ""

    values = feature_vector[:length]

    return ", ".join(
        [f"{x:.4f}" for x in values]
    )