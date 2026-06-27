from azure.identity import DefaultAzureCredential
from azure.ai.textanalytics import TextAnalyticsClient

# Use the Foundry Resource endpoint, not the Project endpoint.
# Create client
credential = DefaultAzureCredential()
client = TextAnalyticsClient(
    endpoint="https://textanalyticsservice-resource.services.ai.azure.com/",
    credential=credential
)

# Input text
documents = [
    "My name is Abhay. My phone number is 9876543210 and my email is abhay@gmail.com."
]

# Analyze sentiment
response = client.recognize_pii_entities(documents=documents)

# Display results
for doc in response:
    print("Original Text:")
    print(documents[0])

    print("\nRedacted Text:")
    print(doc.redacted_text)

    print("\nDetected PII:")

    for entity in doc.entities:
        print(f"Text      : {entity.text}")
        print(f"Category  : {entity.category}")
        print(f"Confidence: {entity.confidence_score:.2f}")
        print()