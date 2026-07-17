import importlib.util
import os
import pathlib
import sys

from ModelDeployment import create_client

# Load the helper module directly by path because this workspace is not a package.
root_dir = pathlib.Path(__file__).resolve().parent.parent
search_module_path = root_dir / "RAG Implementation" / "callAISearchQuery.py"
if not search_module_path.exists():
    raise FileNotFoundError(f"Could not find search module at {search_module_path}")

sys.path.append(str(search_module_path.parent))

from callAISearchQuery import (
    getAISearchResultByKeyword,
    getAISearchResultByVector
    # getAISearchResultHydride as getAISearchResultHybrid,
)

enableKeywordSearch = False
enableVectorSearch = True
enableHybridSearch = False


def create_openai_client() -> OpenAI:
    endpoint = os.getenv(
        "OPENAI_ENDPOINT",
        "https://shopnowaimodel-resource.services.ai.azure.com/api/projects/shopnowaimodel",
    )
    token_provider = get_bearer_token_provider(
        DefaultAzureCredential(),
        "https://ai.azure.com/.default",
    )
    return OpenAI(base_url=endpoint, api_key=token_provider)


def get_text_embedding(text: str) -> list[float]:
    client = create_client()
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=text,
    )
    if not response.data or len(response.data) == 0:
        raise ValueError("Embedding service returned no data")
    print(f"Query embedding length: {len(response.data[0].embedding)}")
    return response.data[0].embedding


def getRelevantContentFromAISearch(query: str) -> list[dict]:
    if enableKeywordSearch:
        try:
            keyword_results = getAISearchResultByKeyword(query)
        except Exception as exc:
            print(f"Keyword search failed for query={query!r}: {exc}")
            return []

        if isinstance(keyword_results, list) and keyword_results:
            simplified = []
            for doc in keyword_results:
                simplified.append({
                    "title": doc.get("title"),
                    "chunk": doc.get("chunk"),
                })
            return simplified

    if enableVectorSearch:
        try:
            query_embedding = get_text_embedding(query)
            print(f"Query embedding length: {len(query_embedding)}")
            vector_results = getAISearchResultByVector(query_embedding)
        except Exception as exc:
            print(f"Vector search failed for query={query!r}: {exc}")
            return []

        if isinstance(vector_results, list) and vector_results:
            simplified = []
            for doc in vector_results:
                simplified.append({
                    "title": doc.get("title"),
                    "chunk": doc.get("chunk"),
                })
            return simplified

    # if enableHybridSearch:
    #     hybrid_results = getAISearchResultHybrid(query)
    #     if hybrid_results:
    #         return f"Hybrid Search Results: {hybrid_results}"
    return []