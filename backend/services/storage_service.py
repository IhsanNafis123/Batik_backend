import base64
import uuid

from backend.config.database import supabase


def upload_base64_image(base64_string):

    if "," in base64_string:
        base64_string = base64_string.split(",")[1]

    image_bytes = base64.b64decode(base64_string)

    filename = f"{uuid.uuid4()}.jpg"

    path = f"designs/{filename}"

    supabase.storage.from_("generated-designs").upload(
        path=path,
        file=image_bytes,
        file_options={
            "content-type": "image/jpeg"
        }
    )

    public_url = supabase.storage.from_("generated-designs").get_public_url(path)

    return public_url