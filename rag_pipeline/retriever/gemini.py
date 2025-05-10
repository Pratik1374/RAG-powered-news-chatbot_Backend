import os
from google import genai
import re

def call_gemini(query, context_docs):
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY not set in environment.")

    client = genai.Client(api_key=api_key)

    context_text = "\n".join(f"- {doc}" for doc in context_docs)

    prompt = (
        "You are a helpful assistant. Based on the following news documents, answer the user's question.\n\n"
        f"Context:\n{context_text}\n\n"
        f"Question: {query}\nAnswer:"
        " Return the answer in HTML format, but exclude <!DOCTYPE>, <html>, <head>, <h1> and <body> tags. "
        "Only use inner HTML elements like <p>, <ul>, <li>, <strong>, etc."
    )


    response = client.models.generate_content(
        model="gemini-1.5-flash",
        contents=prompt
    )

    if not response.candidates or not hasattr(response.candidates[0].content, 'parts') or not response.candidates[0].content.parts:
        # Fallback or handle error if response structure is unexpected
        # For older client versions or different response structures, response.text might be direct
        try:
            raw_output = response.text.strip()
        except AttributeError:
            print("Warning: Unexpected response structure. Trying to access parts.")
            try:
                raw_output = "".join(part.text for part in response.candidates[0].content.parts).strip()
            except Exception as e:
                print(f"Error accessing response content: {e}")
                return "Error: Could not parse Gemini response."
    else:
        raw_output = "".join(part.text for part in response.candidates[0].content.parts).strip()


    # Remove markdown-style code block wrappers like ```html and ```
    html_after_fences = re.sub(r"^```(?:html)?\n?|\n?```$", "", raw_output, flags=re.IGNORECASE).strip()

    single_line_html = html_after_fences.replace("\n", "")

    wrapped_html = f"{single_line_html}"

    return wrapped_html
