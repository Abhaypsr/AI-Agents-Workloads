from typing import Any, Dict, Iterable, List


def parse_search_results(search_results: Iterable[dict]) -> List[Dict[str, Any]]:
    """Normalize search results and remove vector/metadata-only fields."""
    results: List[Dict[str, Any]] = []

    if search_results is None:
        return results

    for document in search_results:
        if document is None:
            continue

        if not isinstance(document, dict):
            try:
                document = dict(document)
            except Exception:
                continue

        item: Dict[str, Any] = {}
        for key, value in document.items():
            if isinstance(key, str) and "vector" in key.lower():
                continue
            item[key] = value

        if item:
            results.append(item)

    return results
