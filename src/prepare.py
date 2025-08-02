import os
import pandas as pd
import tqdm
from transform.pdf import extract_text_from_pdf


def process():
    LABELS_PATH = "data/train_labels.csv"
    PDFS_PATH = "data/train/PDF"
    assert os.path.exists(LABELS_PATH), "data/train_labels.csv does not exist"
    assert os.path.exists(PDFS_PATH), "data/train/PDF does not exist"

    df = pd.read_csv("data/train_labels.csv")

    articles_id = df["article_id"]
    dataset_id = df["dataset_id"]
    type_column = df["type"]

    tqdm.tqdm.pandas(desc="Processing articles")

    paths = articles_id.progress_apply(
        lambda x: os.path.join(PDFS_PATH, f"{x}.pdf"), "MAKING PATHS"
    ).progress_apply(lambda x: extract_text_from_pdf(x), "MAKING RAW TEXT")

    pd.DataFrame(
        {
            "article_id": articles_id,
            "dataset_id": dataset_id,
            "type": type_column,
            "text": paths,
        }
    ).to_csv("data/raw_articles.csv", index=False)


if __name__ == "__main__":
    process()
