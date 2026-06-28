from azure.ai.vision.imageanalysis import ImageAnalysisClient
from azure.ai.vision.imageanalysis.models import VisualFeatures
from azure.identity import DefaultAzureCredential

endpoint = "https://computervisionaiservicetest.cognitiveservices.azure.com/"

client = ImageAnalysisClient(
    endpoint=endpoint,
    credential=DefaultAzureCredential()
)

with open("sampleImages/images.jpg", "rb") as image:
    result = client.analyze(
        image_data=image,
        visual_features=[
            VisualFeatures.OBJECTS
        ]
    )

print("Detected Objects:\n")
print(result.objects.values)

for key, value in result.objects.items():
    print(key)
    print(value)