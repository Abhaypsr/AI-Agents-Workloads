from azure.identity import DefaultAzureCredential
from azure.ai.textanalytics import TextAnalyticsClient

# Use the Foundry Resource endpoint, not the Project endpoint.
# Create client
credential = DefaultAzureCredential()
client = TextAnalyticsClient(
    endpoint="https://textanalyticsservice-resource.services.ai.azure.com/",
    credential=credential
)

# input
documents = [
    "Satya Nadella visited London on Monday."
]

response = client.recognize_entities(documents)

for doc in response:
    for entity in doc.entities:
        print(entity.text)
        print(entity.category)
        print(entity.confidence_score)
        print()