from callAISearchByKeywordSearch import getAISearchResultByKeyword
from callAISearchByVectorSearch import getAISearchResultByVector
# from callAISearchByHybridSearch import getAISearchResultHydride

__all__ = [
    "getAISearchResultByKeyword",
    "getAISearchResultByVector"
]

if __name__ == "__main__":
    print("This wrapper module exposes three simple search methods:")
    print("- getAISearchResultByKeyword(query)")
    print("- getAISearchResultByVector(query_vector)")
    print("- getAISearchResultHydride(query, query_embedding)")

