# from dotenv import load_dotenv
# import os
# from typing import Any, Dict, List, Optional
# from azure.core.credentials import AzureKeyCredential
# from azure.identity import DefaultAzureCredential
# from azure.search.documents import SearchClient
# from azure.search.documents.models import VectorizedQuery

# SEARCH_ENDPOINT_DEFAULT = "https://shopnowaisearch.search.windows.net"
# INDEX_NAME_DEFAULT = "rag-1784302951511"
# VECTOR_FIELD_NAME = "text_vector"


# def build_search_client() -> SearchClient:
#     load_dotenv()
#     search_endpoint = os.getenv("SEARCH_ENDPOINT", SEARCH_ENDPOINT_DEFAULT)
#     query_key = os.getenv("QUERY_KEY")
#     use_aad = os.getenv("USE_AZURE_AD", "false").lower() == "true"
#     index_name = os.getenv("INDEX_NAME", INDEX_NAME_DEFAULT)

#     if query_key:
#         credential = AzureKeyCredential(query_key)
#     elif use_aad:
#         credential = DefaultAzureCredential()
#     else:
#         raise ValueError(
#             "Missing QUERY_KEY environment variable. "
#             "Set QUERY_KEY in .env or environment, OR set USE_AZURE_AD=true "
#             "and configure Azure AD access for your Search service."
#         )

#     print(f"Building SearchClient with endpoint={search_endpoint}, index={index_name}")
#     return SearchClient(search_endpoint, index_name, credential)


# def parse_results(search_results) -> List[Dict[str, Any]]:
#     print("Parsing hybrid search results...")
#     results: List[Dict[str, Any]] = []
#     for document in search_results:
#         item: Dict[str, Any] = {}
#         for key in document.keys():
#             if "vector" in key.lower():
#                 continue
#             item[key] = document.get(key)
#         results.append(item)
#     print(f"Parsed {len(results)} documents")
#     return results


# def getAISearchResultHydride(query: str, query_embedding: Optional[List[float]] = None, top: int = 5) -> List[Dict[str, Any]]:
#     """Perform a hybrid search using text and optional embedding."""
#     print(f"Running hybrid search text='{query}' embedding_provided={query_embedding is not None} top={top}")
#     search_client = build_search_client()

#     if query_embedding is None:
#         search_results = search_client.search(
#             search_text=query,
#             top=top,
#             include_total_count=True,
#         )
#     else:
#         vector_query = VectorizedQuery(
#             vector=query_embedding,
#             fields=VECTOR_FIELD_NAME,
#             k_nearest_neighbors=top,
#         )
#         search_results = search_client.search(
#             search_text=query,
#             vector_queries=[vector_query],
#             include_total_count=True,
#         )

#     return parse_results(search_results)


# if __name__ == "__main__":
#     print("This file performs hybrid search using getAISearchResultHydride(query, query_embedding).")
