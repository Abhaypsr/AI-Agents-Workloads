from openai import OpenAI
from azure.identity import DefaultAzureCredential, get_bearer_token_provider

endpoint = "https://createchatbot-resource.openai.azure.com/openai/v1"
deployment_name = "gpt-5-mini"


def create_client() -> OpenAI:
    token_provider = get_bearer_token_provider(
        DefaultAzureCredential(),
        "https://ai.azure.com/.default",
    )
    return OpenAI(base_url=endpoint, api_key=token_provider)

system_prompt = ""

def generate_response(prompt: str) -> str:
    client = create_client()
    response = client.responses.create(
        model=deployment_name,
        input=prompt,
    )
    return response.output_text


if __name__ == "__main__":
    print(f"response: {generate_response('What is the capital of France?')}")
