import os
import fal_client

FAL_KEY = os.getenv("FAL_KEY")

if not FAL_KEY:
    raise ValueError(
        "FAL_KEY tidak ditemukan di file .env"
    )


def generate_flux_image(
    prompt
):

    handler = fal_client.submit(

        "fal-ai/flux/dev",

        arguments={

            "prompt":
            prompt
        }
    )

    result = handler.get()

    return result["images"][0]["url"]