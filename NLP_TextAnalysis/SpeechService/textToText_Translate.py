from azure.identity import DefaultAzureCredential
from azure.ai.translation.text import TextTranslationClient

# Foundry Resource endpoint
endpoint = "https://<your-foundry-resource>.services.ai.azure.com/"

# Authenticate
credential = DefaultAzureCredential()

# Create Translation Client
client = TextTranslationClient(
    endpoint=endpoint,
    credential=credential
)

# Input Text
text = ["Hello, welcome to Azure AI!"]

# Translate English -> Hindi
response = client.translate(
    body=text,
    to_language=["hi"]
)

# Display Result
for document in response:
    for translation in document.translations:
        print("Detected Language :", document.detected_language.language)
        print("Translated Text   :", translation.text)
        print("Target Language   :", translation.to)