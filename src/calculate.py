from typing import Optional
from src.search.text import find_substring_in_text


def relative_location_of_substring(text: str, substring: str) -> Optional[float]:
    """Calculate the relative location of a substring in a text."""
    if not text or not substring:
        return None
    index: Optional[int] = find_substring_in_text(text, substring)
    if index is None:
        return None
    return index / len(text) if len(text) > 0 else None
