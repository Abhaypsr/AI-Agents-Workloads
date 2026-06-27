#Case1: With web_Search tools enabled:
# My Prompt:
# Hi is there any protest in delhi tommarow? are you check the web pages? latest news?

# Copilot said:
# I don't have the ability to browse the web or check real-time news updates. For the latest information on protests in Delhi tomorrow, I recommend checking reliable news websites, official government announcements, or traffic updates from local authorities. You can also look at social media platforms or news apps for real-time updates. If you want, I can help guide you on where to find the most reliable sources!

#Case2: With web_Search tools enabled:
# My Prompt:
# Hi is there any protest in delhi tommarow? are you check the web pages? latest news?

# Copilot said:
# Yes, there is a protest planned in Delhi tomorrow, June 20, 2026. The youth-led Cockroach Janta Party (CJP) has organized a protest at Jantar Mantar to demand the resignation of Union Education Minister Dharmendra Pradhan over alleged examination irregularities and paper leaks, particularly concerning the NEET exam. The protest has received permission from the Delhi Police and is expected to be peaceful. Supporters have been asked to bring plates and spoons as a symbolic gesture reminiscent of previous national movements. The protest is scheduled to start at 1 PM.

# Would you like details on how to attend or follow the event?

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
    input="Hi is there any protest in delhi tommarow? are you check the web pages? latest news?",
    tools=[
    {"type": "web_search"}
]
)

print(f"answer: {response.output[0]}")

