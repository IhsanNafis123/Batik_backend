import os
import uuid
import mimetypes

from storage3.types import FileOptions

from backend.config.database import supabase


BUCKET = "storage"


def upload_image_to_supabase(file, folder="motifs"):

    try:

        extension = os.path.splitext(file.filename)[1]

        filename = f"{uuid.uuid4().hex}{extension}"

        storage_path = f"{folder}/{filename}"

        content_type = (
            mimetypes.guess_type(file.filename)[0]
            or "image/png"
        )

        file_bytes = file.read()

        supabase.storage.from_(BUCKET).upload(

            path=storage_path,

            file=file_bytes,

            file_options=FileOptions(

                content_type=content_type,

                upsert="true"

            )

        )

        public_url = (
            supabase.storage
            .from_(BUCKET)
            .get_public_url(storage_path)
        )

        return True, public_url, None

    except Exception as e:

        print("UPLOAD ERROR")
        print(e)

        return False, None, str(e)