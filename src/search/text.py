from typing import Text, Optional


def extract_doi_id_from_uri(uri: str) -> Optional[Text]:
    """Extract the last folder from a URI.
    For example, from 'https://doi.org/10.1000/xyz123', it returns 'xyz123'.
    """
    if not uri:
        return None
    parts = uri.split("/")
    return parts[-1] if parts[-1] else None


def find_substring_in_text(text: str, substring: str) -> Optional[int]:
    """Find the index of the first occurrence of a substring in a text."""
    if not text or not substring:
        return None
    index = text.find(substring)
    return index if index != -1 else None


def find_substring_index_in_text_splited(text: str, substring: str) -> Optional[int]:
    """Find the index of the first occurrence of a substring in a text."""
    text_splited = text.split()
    index: Optional[int] = next(
        map(
            lambda word_with_substring: text_splited.index(word_with_substring),
            filter(lambda word: substring in word, text_splited),
        ),
        None,
    )
    return index


def get_surrounding_text(text: str, index: int, n: int = 10) -> str:
    """Get surrounding text with n alphanumeric words before and after the index."""
    if not text or index is None or index < 0 or n < 0:
        return ""

    words = text.split()
    start_index = max(0, index - n)
    end_index = min(len(words), index + n + 1)

    surrounding_text = " ".join(words[start_index:end_index])
    return surrounding_text
