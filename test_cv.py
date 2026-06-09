from backend.services.dataset_service import (
    get_random_reference
)

from backend.services.vision_service import (
    extract_features
)

img = get_random_reference(
    "Jawa_Barat_Megamendung"
)

print("IMAGE:", img)

features = extract_features(img)

print("FEATURE SHAPE:", features.shape)