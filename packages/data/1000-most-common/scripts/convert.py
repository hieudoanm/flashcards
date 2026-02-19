import csv
import json

# Input CSV file
input_csv = "data/words.csv"
# Output JSON files
output_json = "data/cards/words.json"
languages_json = "data/cards/languages.json"

data = []
languages_set = set()

# Read CSV and collect data
with open(input_csv, encoding="utf-8") as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        item = {
            "language": row["language"],
            "front": row["vocabulary"],
            "back": row["english"],
        }
        data.append(item)
        languages_set.add(row["language"])

# Write words JSON
with open(output_json, "w", encoding="utf-8") as jsonfile:
    json.dump(data, jsonfile, ensure_ascii=False, indent=2)
print(f"Converted {len(data)} rows from {input_csv} to {output_json}")

# Write unique languages JSON
languages_list = sorted(list(languages_set))
with open(languages_json, "w", encoding="utf-8") as jsonfile:
    json.dump(languages_list, jsonfile, ensure_ascii=False, indent=2)
print(f"Saved {len(languages_list)} unique languages to {languages_json}")
