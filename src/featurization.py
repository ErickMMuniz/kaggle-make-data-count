import pandas as pd
import dvc.api

from search.text import (
    extract_doi_id_from_uri,
    find_substring_index_in_text_splited,
    get_surrounding_text,
)
from calculate import relative_location_of_substring
from tqdm import tqdm

import re

url_regex = r"https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)"
tqdm.pandas(desc="Processing articles")

params = dvc.api.params_show()


def clean_sourrounding_text(text):
    """
    Cleans the surrounding text by removing URLS, by regex 
    """
    text_splited = text.split()
    text_cleaned = []


    def urls_ends_for_one_text_cleaned(maybe_ending):
        """
        Check if the maybe_ending is a URL ending
        """
        for clean_word in text_cleaned:
            if clean_word.endswith(maybe_ending):
                return True
        return False

    for i in range(len(text_splited) - 1):
        left_word = text_splited[i]
        right_word = text_splited[i + 1]

        joined_word = left_word + right_word

        if re.match(url_regex, joined_word):
            text_cleaned.append(joined_word)
        elif not urls_ends_for_one_text_cleaned(right_word):
            text_cleaned.append(left_word)
        else:
            pass

    return " ".join(text_cleaned)

def change_url_to_generic_url_or_target_by_doi(text, doi):
    """
    Change the URL to a generic URL or target by DOI
    """
    text_splited = text.split()
    text_cleaned = []

    for word in text_splited:
        if re.match(url_regex, word):
            if doi in word:
                text_cleaned.append("<TARGET>")
            else:
                text_cleaned.append("<URL>")
        else:
            # Replace the url with a generic URL using re expression
            word = re.sub(url_regex, "<URL>", word)
            word = word.replace(doi, "<TARGET>")
            text_cleaned.append(word)
            

    return " ".join(text_cleaned)



def extract_sorrounding_text_from_raw_articles(text, article_id, n=10):
    doi = extract_doi_id_from_uri(article_id)
    index_doi = find_substring_index_in_text_splited(text, doi)
    surronding_text = get_surrounding_text(text, index_doi, n)
    clean_sourrounding_text_from_raw_articles = clean_sourrounding_text(surronding_text)
    clean_sourrounding_text_from_raw_articles = change_url_to_generic_url_or_target_by_doi(
        clean_sourrounding_text_from_raw_articles, doi
    )
    return clean_sourrounding_text_from_raw_articles


def calculate_relative_location_of_doi(text, article_id):
    doi = extract_doi_id_from_uri(article_id)
    return relative_location_of_substring(text, doi)


def process():

    n = params["featurization"]["surrounding_text_length"]
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

    df = pd.DataFrame(
        {
            "article_id": articles["article_id"],
            "dataset_id": articles["dataset_id"],
            "type": articles["type"],
            "surrounding_text": surrounding_text,
            "relative_location": relative_location,
        }
    )

    #Filter section
    df = df[df["type"] != "Missing"]
    df = df[df["surrounding_text"].str.count("<TARGET>") == 1]
    
    df.to_csv("data/processed_articles.csv", index=False)


if __name__ == "__main__":
    process()
