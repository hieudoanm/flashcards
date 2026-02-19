# save.py
import os
import pandas as pd
import json
import logging


def save_csv(words, path):
    df = pd.DataFrame(words).drop_duplicates().sort_values(by="english")
    df.to_csv(path, index=False)
    logging.info(f"Saved CSV: {path}")
    return df


def save_json(data, path):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    logging.info(f"Saved JSON: {path}")


def save_languages_list(languages, path):
    languages = sorted(list(set(languages)))
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(languages))
    logging.info(f"Saved languages list: {path}")
