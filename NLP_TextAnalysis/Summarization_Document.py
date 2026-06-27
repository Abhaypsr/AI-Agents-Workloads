from azure.identity import DefaultAzureCredential
from azure.ai.textanalytics import TextAnalyticsClient

# Create client
credential = DefaultAzureCredential()

client = TextAnalyticsClient(
    endpoint="https://textanalyticsservice-resource.services.ai.azure.com/",
    credential=credential
)

# Input document
documents = [
    """
    Azure AI Foundry is a unified platform for building AI applications.
    It provides access to models, tools, and AI services such as Language,
    Vision, and Speech. Developers can build, evaluate, and deploy AI
    solutions efficiently. Azure AI Language offers NLP capabilities such
    as sentiment analysis, entity recognition, language detection, and
    summarization.
    """
]

# Extractive Summarization
poller = client.begin_extract_summary(documents)

result = poller.result()

for doc in result:
    print("Summary:\n")

    for sentence in doc.sentences:
        print(f"- {sentence.text}")
        print(f"  Rank Score : {sentence.rank_score:.2f}")
        print(f"  Offset     : {sentence.offset}")
        print(f"  Length     : {sentence.length}")
        print()