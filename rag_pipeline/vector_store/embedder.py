# rag_pipeline/vector_store/embedder.py
import os
import requests
from dotenv import load_dotenv
load_dotenv()


class Embedder:
    def __init__(self):
        self.api_key = os.environ.get("JINA_API_KEY")
        if not self.api_key:
            raise ValueError("JINA_API_KEY environment variable not set.")
        self.endpoint = "https://api.jina.ai/v1/embeddings"
        self.model = "jina-embeddings-v2-base-en"

    def encode(self, texts):
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "input": texts,
            "model": self.model
        }
        response = requests.post(self.endpoint, headers=headers, json=payload)

        if response.status_code == 200:
            return [item["embedding"] for item in response.json()["data"]]
        else:
            raise Exception(f"Failed to get embeddings: {response.status_code} - {response.text}")

