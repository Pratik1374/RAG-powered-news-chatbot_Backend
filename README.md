# Backend for News Website RAG Chatbot

This repository contains the backend implementation for a Retrieval-Augmented Generation (RAG) powered chatbot that answers queries over a corpus of news articles. It uses FastAPI for the API, Redis for session management and chat history, integrates with a vector store (ChromaDB) and leverages the Google Gemini API for generating final answers.

## Tech Stack

- **Backend Framework:** Python FastAPI
- **Vector Store:** ChromaDB
- **Embeddings:** Jina Embeddings
- **Cache & Sessions:** Redis
- **LLM API:** Google Gemini

## Prerequisites

Before running the backend, ensure you have the following installed and configured:

1.  **Python 3.8+:** Ensure Python is installed on your system.
2.  **pip:** Python's package installer.
3.  **Redis:** You need a running Redis server (Docker recommended).
4.  **Jina API Key:** You need a Jina API key to use Jina Embeddings. Sign up for a free account on the [Jina AI website](https://jina.ai/) and obtain your API key. Set this as an environment variable named `JINA_API_KEY`.
5.  **Google Gemini API Key:** You need a Google Gemini API key to interact with the LLM. Obtain one from [Google AI Studio](https://aistudio.google.com/apikey) and set it as an environment variable named `GEMINI_API_KEY`.

## Setup and Installation

1.  **Navigate to the root directory of this backend repository in your terminal.**

2.  **Install Python dependencies using pip:**

    ```bash
    pip install -r requirements.txt
    ```

3.  **Set up environment variables:**
    Create a `.env` file in the root of the repository and add your API keys:

    ```env
    JINA_API_KEY=YOUR_JINA_API_KEY
    GEMINI_API_KEY=YOUR_GEMINI_KEY
    REDIS_URL=redis://localhost:6379
    ```

4.  **Set up and run the Redis server:**
    ```bash
    docker run -d -p 6379:6379 --name RAG-App-Redis-Server redis
    ```

## RAG Pipeline Steps (Implemented via Scripts)

The initial steps of the RAG pipeline, preparing the knowledge base, are implemented using separate Python scripts located in the `rag_pipeline/scripts` directory within this repository:

1.  **`python -m rag_pipeline.scripts.fetch_and_ingest`**: Fetches and ingests news articles.
2.  **`python -m rag_pipeline.scripts.chunk_articles`**: Chunks the fetched articles.
3.  **`python -m rag_pipeline.scripts.ingest_to_chroma`**: Ingests the chunks and their embeddings into ChromaDB.

**Note:** These scripts need to be run sequentially to populate the vector store before the API can effectively answer queries.

## Running the Backend API

1.  **Navigate to the root directory of this backend repository in your terminal.**

2.  **Run the FastAPI application:**
    ```bash
    uvicorn main:app --reload
    ```
    This will start the API server on `http://127.0.0.1:8000`.

## API Endpoints

- **`POST /chat/`**: Accepts a JSON request with `session_id` and `query`. Returns the chatbot's response.
- **`POST /chat/history`**: Accepts a JSON request with `session_id`. Returns the chat history for the session.
- **`POST /chat/reset`**: Accepts a JSON request with `session_id`. Clears the chat history for the session.

## Session Management and Caching (Redis)

- **Session Identification:** Unique `session_id` from the frontend.
- **Chat History:** Stored in Redis, associated with the `session_id`.
- **Caching:** Potential for caching Gemini responses in Redis.

## How I’d Configure TTL and Cache Warming in Redis

### Session TTL (Time to Live)

To manage memory usage and avoid stale sessions, I would configure a TTL (Time To Live) of 30 minutes for each chat session stored in Redis.

- **Implementation Plan:**
  - Each session's chat history would be stored using a Redis key in the format `chat:<session_id>`.
  - I would use Redis's `EXPIRE` command (or the `expire` method in Python) to set an expiration time of 1800 seconds (30 minutes) on the Redis key holding the chat history list.

```python
# Example: setting a 30-minute TTL on the chat history list
redis_client.expire(f"chat:{session_id}", 1800)
```

## Optional: Persisting Final Transcripts (SQL Database)

Future enhancement to store transcripts in a SQL database.

## Code Walkthrough

This section provides a written explanation of the end-to-end flow of the chatbot, covering key aspects of the backend implementation.

### 1. How Embeddings are Created, Indexed, and Stored

- **Creation:** The process begins with the `rag_pipeline/scripts/fetch_and_ingest.py` script, which fetches news articles from specified RSS feeds. These raw articles are saved as a JSON file. Next, the `rag_pipeline/scripts/chunk_articles.py` script reads these articles, cleans their text content, and divides them into smaller, manageable chunks. These chunks, along with their original titles and URLs, are saved to another JSON file (`data/articles/chunks.json`).

- **Indexing and Storage:** The `rag_pipeline/scripts/ingest_to_chroma.py` script then takes over. It reads the processed chunks. For each chunk, it utilizes the `Embedder` class (defined in `rag_pipeline/vector_store/embedder.py`) to generate embeddings using the Jina Embeddings API. The `Embedder` class handles communication with the Jina API, passing the text chunks and receiving their vector representations. Finally, this script uses the `chroma_store.py` module to interact with ChromaDB. It either gets an existing collection named `news_articles` or creates it if it doesn't exist. The text chunks, their associated metadata (title, URL), unique IDs, and their corresponding Jina embeddings are then added to this ChromaDB collection. ChromaDB internally indexes these embeddings, allowing for efficient similarity search later on. The data in ChromaDB is persisted to the `chroma_data` directory.

### 2. How Redis Caching & Session History Works

- **Session Management:** User sessions are managed using a `session_id`.

  **Current Implementation:** The backend uses the `session_id` provided by the frontend as the key in Redis to store and retrieve the list of chat messages.

  **Ideal Implementation:** The backend should ideally generate a unique `session_id` for new users and manage it, sending it to the frontend for subsequent requests.

  **Reasoning:** While the current approach simplifies initial setup, backend-driven `session_id` generation offers better control, security, and aligns with a stateless API design.

- **Storing Chat History:** For each session, the conversation turns (user's query and the bot's response) are appended to a Redis list associated with the `session_id`.

- **Clearing Chat History:** When the frontend calls the `/chat/reset` endpoint, the backend uses the `del` command in Redis to remove the list associated with the `session_id`, effectively clearing the chat history for that session.

### 3. How the Frontend Calls API and Handles Responses (Backend Perspective)

From the backend's perspective, the frontend interacts via a REST API over HTTP:

- **Sending Queries:** When a user submits a query on the frontend, it makes a `POST` request to the `/chat/` endpoint. This request includes the user's `query` and their `session_id` in the request body (as JSON). The backend receives this request, extracts the query and session ID, performs the RAG pipeline, stores the conversation turn in Redis, and sends the generated answer back to the frontend in the HTTP response.

- **Clearing History:** When the user clicks the "reset session" button, the frontend makes a `POST` request to the `/chat/reset` endpoint, with the `session_id` included in the JSON request body. The backend receives this request, clears the history in Redis for that `session_id`, and sends back a success status.

### 4. Noteworthy Design Decisions and Potential Improvements

- **Design Decisions:**

  - **Modular RAG Pipeline:** Separating the fetching, chunking, embedding, and indexing steps into distinct scripts promotes modularity and makes it easier to modify or replace individual components of the pipeline.
  - **REST API for Chat:** Used a RESTful API for communication between the frontend and backend.
  - **Redis for Session and History:** Choosing Redis, an in-memory data store, for managing session IDs and chat history provides fast read and write operations.
  - **ChromaDB for Vector Storage:** Selecting ChromaDB offers a simple and efficient way to store and query embeddings for semantic search.
  - **Jina Embeddings:** A free-tier service used for generating text embeddings.
  - **Google Gemini API:** Using the free tier with the gemini-1.5-flash model.

- **Potential Improvements:**
  - Implement robust error handling and logging.
  - Add unit and integration tests.
  - Implement streaming of Gemini responses.
  - Consider user authentication and authorization.
  - Optimize Gemini prompt engineering.
  - Implement API rate limiting.
  - Secure the API endpoints.
