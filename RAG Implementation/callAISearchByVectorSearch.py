from dotenv import load_dotenv
import os
from typing import Any, Dict, List
from azure.core.credentials import AzureKeyCredential
from azure.identity import DefaultAzureCredential
from azure.search.documents import SearchClient
from azure.search.documents.models import VectorizedQuery
from search_helpers import parse_search_results

SEARCH_ENDPOINT_DEFAULT = "https://shopnowaisearch.search.windows.net"
INDEX_NAME_DEFAULT = "rag-1784302951511"
VECTOR_FIELD_NAME = "text_vector"  # This should match the vector field name in your Azure Search index schema.


def build_search_client() -> SearchClient:
    load_dotenv()
    search_endpoint = os.getenv("SEARCH_ENDPOINT", SEARCH_ENDPOINT_DEFAULT)
    query_key = os.getenv("QUERY_KEY")
    use_aad = os.getenv("USE_AZURE_AD", "false").lower() == "true"
    index_name = os.getenv("INDEX_NAME", INDEX_NAME_DEFAULT)

    if query_key:
        credential = AzureKeyCredential(query_key)
    elif use_aad:
        credential = DefaultAzureCredential()
    else:
        raise ValueError(
            "Missing QUERY_KEY environment variable. "
            "Set QUERY_KEY in .env or environment, OR set USE_AZURE_AD=true "
            "and configure Azure AD access for your Search service."
        )

    print(f"Building SearchClient with endpoint={search_endpoint}, index={index_name}")
    return SearchClient(search_endpoint, index_name, credential)


def getAISearchResultByVector(query: List[float], top: int = 5) -> List[Dict[str, Any]]:
    """Perform a vector search using an embedding vector."""
    print(f"Running vector search with query length={len(query)} and top={top}")
    search_client = build_search_client()
    vector_query = VectorizedQuery(
        vector=query,
        fields=VECTOR_FIELD_NAME,
        k_nearest_neighbors=top,
    )
    search_results = search_client.search(
        search_text="*",
        vector_queries=[vector_query],
        include_total_count=True,
    )
    parsed_results = parse_search_results(search_results)
    print(f"Vector search returned {len(parsed_results)} documents")
    return parsed_results


if __name__ == "__main__":
    print("This file performs vector search using getAISearchResultByVector(query).")
