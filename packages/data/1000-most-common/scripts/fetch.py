# fetch.py
import requests
import logging
import time
from config import TIMEOUT, MAX_RETRIES, RETRY_DELAY


def fetch_with_retries(url: str, retries=MAX_RETRIES, delay=RETRY_DELAY):
    """Fetch a URL with retry logic"""
    attempt = 0
    while attempt < retries:
        try:
            response = requests.get(url, timeout=TIMEOUT)
            response.raise_for_status()
            return response
        except requests.RequestException as e:
            attempt += 1
            logging.warning(f"Attempt {attempt} failed for {url}: {e}")
            if attempt < retries:
                logging.info(f"Retrying in {delay} seconds...")
                time.sleep(delay)
            else:
                logging.error(f"Failed to fetch {url} after {retries} attempts.")
                return None
