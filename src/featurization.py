import pandas as pd

from search.text import (
    extract_doi_id_from_uri,
    find_substring_index_in_text_splited,
    get_surrounding_text,
)
from calculate import relative_location_of_substring
from tqdm import tqdm

tqdm.pandas(desc="Processing articles")


def extract_sorrounding_text_from_raw_articles(text, article_id, n=10):
    doi = extract_doi_id_from_uri(article_id)
    index_doi = find_substring_index_in_text_splited(text, doi)
    surronding_text = get_surrounding_text(text, index_doi, n)
    return surronding_text


def calculate_relative_location_of_doi(text, article_id):
    doi = extract_doi_id_from_uri(article_id)
    return relative_location_of_substring(text, doi)


def process():

    n = 10  # Number of words to include before and after the DOI in the surrounding text
    RAW_ARTICLES_PATH = "data/raw_articles.csv"

    articles = pd.read_csv(RAW_ARTICLES_PATH)
    assert articles.columns.tolist() == [
        "article_id",
        "dataset_id",
        "type",
        "text",
    ], "Columns in raw articles do not match expected format"

    surrounding_text = articles.progress_apply(
        lambda x: extract_sorrounding_text_from_raw_articles(
            x["text"], x["dataset_id"], n=n
        ),
        axis=1,
    )
    relative_location = articles.progress_apply(
        lambda x: calculate_relative_location_of_doi(x["text"], x["dataset_id"]),
        axis=1,
    )

    pd.DataFrame(
        {
            "article_id": articles["article_id"],
            "dataset_id": articles["dataset_id"],
            "type": articles["type"],
            "surrounding_text": surrounding_text,
            "relative_location": relative_location,
        }
    ).to_csv("data/processed_articles.csv", index=False)


if __name__ == "__main__":
    process()
