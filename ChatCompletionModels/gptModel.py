from openai import OpenAI
from azure.identity import DefaultAzureCredential, get_bearer_token_provider

endpoint = "https://ailearningbyabhay-resource.services.ai.azure.com/openai/v1"
deployment_name = "gpt-4.1"
token_provider = get_bearer_token_provider(DefaultAzureCredential(), "https://ai.azure.com/.default")

client = OpenAI(
    base_url=endpoint,
    api_key=token_provider
)

response = client.responses.create(
    model=deployment_name,
    input="What is the capital of France?",
)

print(f"answer: {response.output[0]}")
print(f"Response: {response.output_text}")
print(f"Response ID: {response.id}")
print(f"Tokens used: {response.usage.total_tokens}")
print(f"Status: {response.status}")
