from openai import AzureOpenAI
from azure.identity import DefaultAzureCredential, get_bearer_token_provider
import base64
from pathlib import Path

endpoint = "https://testaivisionmodeldeployment-resource.openai.azure.com/"
deployment = "gpt-5-mini"

token_provider = get_bearer_token_provider(
    DefaultAzureCredential(),
    "https://cognitiveservices.azure.com/.default"
)

client = AzureOpenAI(
    azure_endpoint=endpoint,
    azure_ad_token_provider=token_provider,
    api_version="2025-04-01-preview"   # or the API version supported by your resource
)

system_message = """
You have to analyze the image and find two random objects.
Return:
{
    name,
    color,
    size,
    position,
    description,
    isHuman
}
"""

prompt = "Analyze this image."

image_path = Path(__file__).parent / "sampleImages" / "images.jpg"

with open(image_path, "rb") as image_file:
    base64_image = base64.b64encode(image_file.read()).decode("utf-8")

image_data_url = f"data:image/jpeg;base64,{base64_image}"

response = client.responses.create(
    model=deployment,
    input=[
        {
            "role": "developer",
            "content": system_message
        },
        {
            "role": "user",
            "content": [
                {
                    "type": "input_text",
                    "text": prompt
                },
                {
                    "type": "input_image",
                    "image_url": image_data_url
                }
            ]
        }
    ]
)

print(response.output_text)