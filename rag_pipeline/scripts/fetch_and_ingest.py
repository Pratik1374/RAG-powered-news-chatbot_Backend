# rag_pipeline/scripts/fetch_and_ingest.py

from rag_pipeline.ingest.rss_parser import extract_rss_urls
from rag_pipeline.ingest.fetch_articles import fetch_articles

def get_articles_from_rss(limit=50):
    rss_urls = [
        "https://www.theguardian.com/world/rss",
        "https://www.theguardian.com/uk/technology/rss",
    ]

    all_urls = []
    for rss in rss_urls:
        all_urls.extend(extract_rss_urls(rss, max_articles=limit))

    all_urls = all_urls[:limit]
    fetch_articles(all_urls, limit=limit)

if __name__ == "__main__":
    get_articles_from_rss()
