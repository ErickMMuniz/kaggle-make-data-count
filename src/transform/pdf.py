import pymupdf
from functools import reduce


def transform_text(text: str) -> str:
    """Transform text by removing newlines and encoding."""
    return text.encode("ascii", "ignore").decode("utf8").replace("\n", " ")


def extract_text_from_pdf(pdf_path: str) -> str:
    """Extract and transform text from a PDF file."""
    doc: pymupdf.Document = pymupdf.open(filename=pdf_path, filetype="pdf")
    reduced_text = reduce(
        lambda x, y: x + " " + y, [transform_text(page.get_text()) for page in doc]
    )
    return reduced_text
