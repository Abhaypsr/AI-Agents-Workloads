from openai import OpenAI
from azure.identity import DefaultAzureCredential, get_bearer_token_provider

endpoint = "https://aifoundrytoollearning-resource.services.ai.azure.com/openai/v1"
deployment_name = "gpt-4.1-mini"
token_provider = get_bearer_token_provider(DefaultAzureCredential(), "https://ai.azure.com/.default")

client = OpenAI(
    base_url=endpoint,
    api_key=token_provider
)

response = client.responses.create(
    model=deployment_name,
    input="What is the sum of 123 and 456?",
    tools=[
        {
            "type": "code_interpreter",
            "container": {
                "type": "auto"
            }
        }
    ]
)

print(f"answer: {response.output[0]}")

