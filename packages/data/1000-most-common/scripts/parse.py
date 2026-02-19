# parse.py
from bs4 import BeautifulSoup
import logging


def parse_languages(html: str) -> List:
    """Parse language links from HTML and return <li> elements from the first wp-block-list"""
    soup = BeautifulSoup(html, "html.parser")
    ul = soup.find("ul", class_="wp-block-list")  # get only the first
    if not ul:
        return []
    li_items = ul.find_all("li")
    return li_items


def parse_words(html: str, language_column: str):
    """Parse words table from language page"""
    try:
        soup = BeautifulSoup(html, "html.parser")
        tables = soup.find_all("table")
        words = []

        for table in tables:
            tbody = table.find("tbody")
            if not tbody:
                logging.warning(f"No <tbody> found for {language_column}")
                continue
            rows = tbody.find_all("tr")
            for row in rows:
                cells = row.find_all("td")
                if len(cells) < 3:
                    continue
                number_text = cells[0].get_text().strip().lower()
                lang_text = cells[1].get_text().strip().lower()
                eng_text = cells[2].get_text().strip().lower()
                if number_text != "number":
                    words.append(
                        {
                            "language": language_column,
                            "english": eng_text,
                            "vocabulary": lang_text,
                        }
                    )
        return sorted(words, key=lambda x: x["english"])
    except Exception as e:
        logging.error(f"Failed to parse words for {language_column}: {e}")
        return []
