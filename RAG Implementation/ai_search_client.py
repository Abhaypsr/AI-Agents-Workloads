from dotenv import load_dotenv
import os
from typing import Any, Dict, List, Optional
from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient

SEARCH_ENDPOINT_DEFAULT = "https://shopnowaisearch.search.windows.net"
INDEX_NAME_DEFAULT = "rag-1784302951511"
VECTOR_FIELD_NAME = "text_vector"  # Update this if your index uses a different vector field name.


def build_search_client() -> SearchClient:
    """Build an Azure Search client for the ShopNow AI Search endpoint."""
    load_dotenv()
    search_endpoint = os.getenv("SEARCH_ENDPOINT", SEARCH_ENDPOINT_DEFAULT)
    query_key = os.getenv("QUERY_KEY")
    index_name = os.getenv("INDEX_NAME", INDEX_NAME_DEFAULT)

    if not query_key:
        raise ValueError("Missing QUERY_KEY environment variable. Set it in your .env or environment.")

    return SearchClient(search_endpoint, index_name, AzureKeyCredential(query_key))


def is_vector_field(key: str, value: Any) -> bool:
    """Detect whether a field is a vector field so we can omit it from LLM context."""
    if not isinstance(key, str):
        return False
    if "vector" not in key.lower():
        return False
    if not isinstance(value, list):
        return False
    return all(isinstance(item, (int, float)) for item in value[:10])


def normalize_search_key(key: str) -> str:
    """Normalize search result keys for more readable output."""
    if key == "@search.score":
        return "search_score"
    if key == "@search.rerankerScore":
        return "reranker_score"
    if key == "@search.answers":
        return "search_answers"
    return key.lstrip("@") if key.startswith("@") else key


def clean_search_document(document: Any, omit_vector: bool = True) -> Dict[str, Any]:
    """Convert a search document to a plain dict and optionally remove vectors."""
    cleaned: Dict[str, Any] = {}
    for key in document.keys():
        value = document.get(key)
        if omit_vector and is_vector_field(key, value):
            continue
        cleaned[normalize_search_key(key)] = value
    return cleaned


def parse_search_results(search_results, omit_vector: bool = True) -> List[Dict[str, Any]]:
    """Parse Azure Search results into a list of documents for downstream use."""
    return [clean_search_document(document, omit_vector=omit_vector) for document in search_results]


def get_azure_search_results(
    search_text: Optional[str] = None,
    vector: Optional[List[float]] = None,
    top: int = 5,
) -> List[Dict[str, Any]]:
    """Perform keyword, vector, or hybrid search against the ShopNow AI Search index."""
    if search_text is None and vector is None:
        raise ValueError("Either search_text or vector must be provided.")

    search_client = build_search_client()

    if search_text is None:
        search_text = "*"

    search_kwargs = {
        "top": top,
        "include_total_count": True,
    }

    if vector is not None:
        search_kwargs["vector"] = vector
        search_kwargs["vector_fields"] = VECTOR_FIELD_NAME

    search_results = search_client.search(
        search_text=search_text,
        **search_kwargs,
    )

    return parse_search_results(search_results)


def getAISearchResultByKeyword(query: str, top: int = 5) -> List[Dict[str, Any]]:
    """
    Perform a keyword search using simple words.
    query is supposed to be simple words for the keyword search.
    """
    return get_azure_search_results(search_text=query, top=top)


def getAISearchResultByVector(query: List[float], top: int = 5) -> List[Dict[str, Any]]:
    """
    Perform a vector search using an embedding vector.
    query is supposed to be an embedding vector here.
    """
    return get_azure_search_results(search_text="*", vector=query, top=top)


def getAISearchResultHydride(query: str, query_embedding: Optional[List[float]] = None, top: int = 5) -> List[Dict[str, Any]]:
    """
    Perform a hybrid search combining text and optional vector embedding.
    query is supposed to be simple words, and query_embedding is supposed to be an embedding vector.
    """
    if query_embedding is None:
        return getAISearchResultByKeyword(query, top=top)
    return get_azure_search_results(search_text=query, vector=query_embedding, top=top)


if __name__ == "__main__":
    print("This module contains the actual Azure AI Search helpers.")
    print("Use getAISearchResultByKeyword(), getAISearchResultByVector(), or getAISearchResultHydride().")
