# Before running the sample:
#    pip install azure-ai-projects>=2.1.0

from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient

endpoint = "https://createchatbot-resource.services.ai.azure.com/api/projects/CreateChatBot"

project_client = AIProjectClient(
    endpoint=endpoint,
    credential=DefaultAzureCredential(),
)

my_agent = "ShopNowAIAssistant"
my_version = "6"
 # Get the OpenAI client from the project clien
openai_client = project_client.get_openai_client()
conversation = openai_client.conversations.create()

def generate_response_from_agents(prompt: str) -> str:
    # Reference the agent to get a response
    response = openai_client.responses.create(
        input = [{"role": "user", "content": prompt}],
        conversation = conversation.id,
        extra_body = {"agent_reference": {"name": my_agent, "version": my_version, "type": "agent_reference"}},
    )
    print(type(conversation))
    print(conversation)
    return response.output_text
    