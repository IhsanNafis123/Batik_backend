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

def upload_avatar(file, user_id):

    try:

        extension = file.filename.split(".")[-1]

        filename = f"{user_id}.{extension}"

        path = f"avatars/{filename}"

        file.stream.seek(0)

        image_bytes = file.read()

        # Hapus avatar lama jika ada
        try:

            supabase.storage.from_("avatars").remove(
                [path]
            )

        except Exception:
            pass

        # Upload avatar baru
        supabase.storage.from_("avatars").upload(

            path=path,

            file=image_bytes,

            file_options={

                "content-type": file.content_type,

                "upsert": "true"

            }

        )

        public_url = (
            supabase
            .storage
            .from_("avatars")
            .get_public_url(path)
        )

        return public_url

    except Exception as e:

        print("UPLOAD AVATAR ERROR:", e)

        return None