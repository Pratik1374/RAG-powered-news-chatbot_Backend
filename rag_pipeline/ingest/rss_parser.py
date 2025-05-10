# rag_pipeline/ingest/rss_parser.py

import feedparser

def extract_rss_urls(feed_url: str, max_articles: int = 50):
    """
    Parses an RSS feed and extracts article URLs.
    """
    feed = feedparser.parse(feed_url)
    return [entry.link for entry in feed.entries][:max_articles]
