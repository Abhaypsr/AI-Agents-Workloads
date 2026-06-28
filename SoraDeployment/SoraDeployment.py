import os
import time
from dotenv import load_dotenv
from openai import OpenAI
from azure.identity import DefaultAzureCredential, get_bearer_token_provider

# =====================================
# Load Environment Variables
# =====================================

load_dotenv()

endpoint = "https://testaivisionmodeldeployment-resource.openai.azure.com/openai/v1/"
model_deployment = "sora-2"

# =====================================
# Azure Authentication
# =====================================

token_provider = get_bearer_token_provider(
    DefaultAzureCredential(),
    "https://cognitiveservices.azure.com/.default"
)

client = OpenAI(
    base_url=endpoint,
    api_key=token_provider,
)

# =====================================
# Poll Video Status
# =====================================

def poll_video_status(video_id):
    video = client.videos.retrieve(video_id)

    while video.status not in ["completed", "failed", "cancelled"]:
        print(f"Status: {video.status}. Waiting 20 seconds...")
        time.sleep(20)
        video = client.videos.retrieve(video_id)

    if video.status == "completed":
        print("Video successfully completed!")
    else:
        print(f"Video creation ended with status: {video.status}")

    return video

# =====================================
# Download Video
# =====================================

def download_video(video_id, output_file):

    content = client.videos.download_content(
        video_id,
        variant="video"
    )

    content.write_to_file(output_file)

    print(f"Video saved as {output_file}")

# =====================================
# Generate Video From Image
# =====================================

def generate_video_from_image(image_path, prompt, size="1280x720", seconds="4"):

    with open(image_path, "rb") as image:

        video = client.videos.create(
            model=model_deployment,
            prompt=prompt,
            size=size,
            seconds=seconds,
            input_reference=image
        )

    return poll_video_status(video.id)

# =====================================
# Main
# =====================================

def main():

    # -------------------------------
    # Generate video from text prompt
    # -------------------------------

    video = client.videos.create(
        model=model_deployment,
        prompt="A peaceful mountain lake at sunrise with mist rising from the water",
        size="1280x720",
        seconds="4",
    )

    video = poll_video_status(video.id)
    print(f"Video ID: {video.id}")

    if video.status == "completed":
        download_video(video.id, "text_video.mp4")

    # -----------------------------------
    # Generate video from reference image
    # -----------------------------------

    # video = generate_video_from_image(
    #     image_path="reference.png",
    #     prompt="The scene comes to life with gentle movement and ambient lighting",
    #     size="1280x720",
    #     seconds="4"
    # )

    # if video.status == "completed":
    #     download_video(video.id, "image_based_video.mp4")


if __name__ == "__main__":
    main()