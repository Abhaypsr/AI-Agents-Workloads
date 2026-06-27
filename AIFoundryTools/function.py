from openai import OpenAI
from azure.identity import DefaultAzureCredential, get_bearer_token_provider
from datetime import datetime

endpoint = "https://aifoundrytoollearning-resource.services.ai.azure.com/openai/v1"
deployment_name = "gpt-4.1-mini"
token_provider = get_bearer_token_provider(DefaultAzureCredential(), "https://ai.azure.com/.default")

def get_current_time():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


client = OpenAI(
    base_url=endpoint,
    api_key=token_provider
)

response = client.responses.create(
    model=deployment_name,
    input="What is the time right now in IST?",
    tools=[
        {
            "type": "function",
            "name": "get_current_time",
            "description": "Returns the current date and time."   ,
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }    
        }
    ]
)

tool_call = response.output[0]

# if tool_call.type == "function_call":
#     result = get_current_time()
#     print(result)

print(f"answer: {response.output[0]}")
# type='function_call', id='fc_0a4cd5bc394e7490006a3571748bf88195bd4db5ca78e2759a', namespace=None, status='completed')
# Function tools don't execute automatically. The model only requests the function call;
# the application must execute the function and send the result back to the model.
# Function tools require app-side execution. MCP/Agents can automate this flow but still execute outside the model.

# Function calling is a 2-step process: model requests the function,
# app executes it and returns the output.

tool_call = response.output[0]

if tool_call.type == "function_call":
    result = get_current_time()

    response2 = client.responses.create(
        model=deployment_name,
        previous_response_id=response.id,
        input=[
            {
                "type": "function_call_output",
                "call_id": tool_call.call_id,
                "output": result
            }
        ]
    )

print(response2.output_text)