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
    "The hotel staff was friendly, but the room was dirty."
]

# Analyze sentiment
response = client.analyze_sentiment(documents=documents)

# Display results
for doc in response:
    print(f"Overall Sentiment: {doc.sentiment}")
    print("Confidence Scores:")
    print(f"  Positive: {doc.confidence_scores.positive}")
    print(f"  Neutral : {doc.confidence_scores.neutral}")
    print(f"  Negative: {doc.confidence_scores.negative}")