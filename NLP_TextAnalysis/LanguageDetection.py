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
    "Hello everyone.",
    "Bonjour le monde.",
    "Hola amigos.",
    "नमस्ते दोस्तों",
    "snakjjxksn"
]

response = client.detect_language(documents)

for doc in response:
    print(doc.primary_language.name)
    print(doc.primary_language.iso6391_name)
    print(doc.primary_language.confidence_score)
    print()




# output:
# English
# en
# 1.0

# French
# fr
# 1.0

# Spanish
# es
# 1.0

# Hindi
# hi
# 1.0

# English
# en
# 0.94