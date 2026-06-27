import glob

from openai import OpenAI
from azure.identity import DefaultAzureCredential, get_bearer_token_provider

endpoint = "https://aifoundrytoollearning-resource.services.ai.azure.com/openai/v1"
deployment_name = "gpt-4.1-mini"

token_provider = get_bearer_token_provider(
    DefaultAzureCredential(),
    "https://ai.azure.com/.default"
)

client = OpenAI(
    base_url=endpoint,
    api_key=token_provider
)

def create_vector_store_and_upload_files():
    print("Creating vector store and uploading files...")

    vector_store = client.vector_stores.create(
        name="travel-brochures"
    )

    file_streams = [open(f, "rb") for f in glob.glob("brochures/*.pdf")]

    if not file_streams:
        print("No PDF files found in brochures folder!")
        return None

    file_batch = client.vector_stores.file_batches.upload_and_poll(
        vector_store_id=vector_store.id,
        files=file_streams
    )

    for f in file_streams:
        f.close()

    print(
        f"Vector store created with "
        f"{file_batch.file_counts.completed} files."
    )

    return vector_store.id


vector_store_id = create_vector_store_and_upload_files()

if not vector_store_id:
    exit()

response = client.responses.create(
    model=deployment_name,
    instructions="""
    You are a travel assistant that provides information on travel services available from Margie's Travel.
    Answer questions about services offered by Margie's Travel using the provided travel brochures.
    Search the web for general information about destinations or current travel advice.
    """,
    input="What travel packages are available for Europe?",
    tools=[
        {
            "type": "file_search",
            "vector_store_ids": [vector_store_id]
        },
        {
            "type": "web_search"
        }
    ]
)

print(response.output_text)