"""
Run this model in Python

pip install anthropic azure-identity
"""

from anthropic import AnthropicFoundry
from azure.identity import DefaultAzureCredential, get_bearer_token_provider
import os

token_provider = get_bearer_token_provider(
    DefaultAzureCredential(),
    "https://cognitiveservices.azure.com/.default"
)

client = AnthropicFoundry(
    azure_ad_token_provider=token_provider,
    base_url="https://ailearningbyabhay-resource.services.ai.azure.com/anthropic",
)

tools = []

messages = [
    {
        "role": "user",
        "content": [
            {
                "type": "text",
                "text": "INSERT_INPUT_HERE",
            },
        ],
    },
]

while True:
    message = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=20000,
        temperature=1,
        messages=messages,
        tools=tools,
    )

    print(f"[Model Response] {message.content}")

    should_continue = False

    messages.append(
        {
            "role": "assistant",
            "content": message.content,
        }
    )

    content = []

    for content_block in message.content:
        if content_block.type == "tool_use":
            should_continue = True

            content.append(
                {
                    "type": "tool_result",
                    "tool_use_id": content_block.id,
                    "content": locals()[content_block.name](),
                }
            )

    if should_continue:
        messages.append(
            {
                "role": "user",
                "content": content,
            }
        )
    else:
        break