# rag_pipeline/ingest/fetch_articles.py
from newsplease import NewsPlease
import json
from pathlib import Path

ARTICLES_DIR = Path("data/articles")
ARTICLES_DIR.mkdir(parents=True, exist_ok=True)

def fetch_articles(urls: list, limit: int = 50):
    articles = []
    count = 0

    for url in urls:
        try:
            article = NewsPlease.from_url(url)
            if article and article.maintext:
                articles.append({
                    "title": article.title,
                    "text": article.maintext,
                    "date": str(article.date_publish),
                    "url": article.url
                })
                count += 1
        except Exception as e:
            print(f"Error with URL {url}: {e}")

        if count >= limit:
            break

    with open(ARTICLES_DIR / "raw_articles.json", "w", encoding="utf-8") as f:
        json.dump(articles, f, indent=2)

    print(f"[+] Fetched and saved {len(articles)} articles.")
    return articles
