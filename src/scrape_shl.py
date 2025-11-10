import argparse
import json
import time
from typing import List, Dict
import requests
from bs4 import BeautifulSoup

CATALOG_URL = "https://www.shl.com/solutions/products/product-catalog/"


def fetch(url: str) -> str:
    resp = requests.get(url, timeout=60, headers={"User-Agent": "Mozilla/5.0"})
    resp.raise_for_status()
    return resp.text


def parse_catalog(html: str) -> List[Dict]:
    soup = BeautifulSoup(html, "html.parser")
    items = []
    # NOTE: This selector may need adjustment based on SHL site structure changes.
    cards = soup.select(".product-card, .c-card")
    for card in cards:
        name = (card.select_one(".c-card__title, .product-card__title") or {}).get_text(strip=True) if card else None
        url = None
        a = card.find("a", href=True)
        if a:
            href = a["href"]
            url = href if href.startswith("http") else f"https://www.shl.com{href}"
        desc = (card.select_one(".c-card__excerpt, .product-card__description") or {}).get_text(strip=True) if card else None
        # Filter heuristic for Individual Test Solutions (ignore packaged job solutions keywords)
        if name and desc and any(k in desc.lower() for k in ["assessment", "test", "skills", "personality"]):
            items.append({
                "name": name,
                "url": url,
                "description": desc,
                "type": None,
                "duration": None,
                "skills": [],
            })
    return items


def main(out_path: str):
    html = fetch(CATALOG_URL)
    items = parse_catalog(html)
    with open(out_path, "w") as f:
        json.dump(items, f, indent=2)
    print(f"Saved {len(items)} items to {out_path}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True, help="Output JSON path")
    args = ap.parse_args()
    main(args.out)
