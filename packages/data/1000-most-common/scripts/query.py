# main.py

import os
import logging
from tqdm import tqdm
import pandas as pd
from config import LANGUAGES_URL, LANGUAGES_DIR, DATA_DIR
from fetch import fetch_with_retries
from parse import parse_languages, parse_words
from save import save_csv, save_json, save_languages_list

# File paths
COMBINED_CSV = os.path.join(DATA_DIR, "words.csv")
WORDS_JSON = os.path.join(DATA_DIR, "words.json")
LANGUAGES_JSON = os.path.join(DATA_DIR, "languages.json")
LANGUAGES_TXT = os.path.join(DATA_DIR, "languages.txt")
REMAINING_LANGUAGES_TXT = os.path.join(DATA_DIR, "remaining_languages.txt")

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.FileHandler("scraping.log"), logging.StreamHandler()],
)

# Ensure directories exist
os.makedirs(LANGUAGES_DIR, exist_ok=True)
os.makedirs(DATA_DIR, exist_ok=True)

# Fetch language page
response = fetch_with_retries(LANGUAGES_URL)
if not response:
    logging.error("Cannot fetch languages page. Exiting.")
    exit(1)

list_items = parse_languages(response.text)

all_languages = []
downloaded_languages = []

for list_item in tqdm(list_items, desc="Languages"):
    anchor = list_item.find("a", href=True)
    print(list_item)
    if not anchor:
        continue
    language = anchor.text.lower()
    all_languages.append(language)  # track all found languages
    column = "_".join(language.split(" "))
    link = anchor.get("href", "")
    if "1000-most-common" in link and language != "english":
        csv_path = os.path.join(LANGUAGES_DIR, f"{language}.csv")
        # Skip scraping if individual CSV already exists
        if os.path.exists(csv_path):
            logging.info(f"CSV already exists for {language}, skipping scraping.")
            downloaded_languages.append(language)
            continue

        logging.info(f"Starting query for language: {language}")
        words_response = fetch_with_retries(link)
        if not words_response:
            logging.warning(f"Failed to fetch words for {language}, skipping.")
            continue

        words = parse_words(words_response.text, column)
        if words:
            downloaded_languages.append(language)
            save_csv(words, csv_path)
            logging.info(f"Saved CSV for {language}: {csv_path}")
        else:
            logging.warning(f"No words found for {language}")

# Save list of downloaded languages
save_languages_list(downloaded_languages, LANGUAGES_TXT)
logging.info(f"Saved languages list: {LANGUAGES_TXT}")

# Combine CSVs into one
csv_files = [
    os.path.join(LANGUAGES_DIR, f)
    for f in os.listdir(LANGUAGES_DIR)
    if f.endswith(".csv")
]
combined_df = pd.concat([pd.read_csv(f) for f in csv_files], ignore_index=True)
combined_df = combined_df.sort_values(by=["language", "english"])
combined_df.to_csv(COMBINED_CSV, index=False)
logging.info(f"Saved combined CSV: {COMBINED_CSV}")

# Convert to front/back JSON
data = []
languages_set = set()
for _, row in combined_df.iterrows():
    data.append(
        {
            "language": row["language"],
            "front": row["vocabulary"],
            "back": row["english"],
        }
    )
    languages_set.add(row["language"])

# Save JSON files
save_json(data, WORDS_JSON)
logging.info(f"Saved words JSON: {WORDS_JSON}")

save_json(sorted(list(languages_set)), LANGUAGES_JSON)
logging.info(f"Saved unique languages JSON: {LANGUAGES_JSON}")

# List remaining languages that were not downloaded
remaining_languages = set(all_languages) - set(downloaded_languages)
if remaining_languages:
    logging.warning(f"Languages not downloaded: {sorted(remaining_languages)}")
    with open(REMAINING_LANGUAGES_TXT, "w", encoding="utf-8") as f:
        f.write("\n".join(sorted(remaining_languages)))
    logging.info(f"Saved remaining languages to {REMAINING_LANGUAGES_TXT}")
else:
    logging.info("All languages were downloaded successfully.")

logging.info("Scraping and conversion completed successfully.")
