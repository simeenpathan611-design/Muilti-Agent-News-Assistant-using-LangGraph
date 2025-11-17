# Summarizes fetched AI news
# agents/summarizer_agent.py

import os
import json
from dotenv import load_dotenv
from pathlib import Path
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

# Get keys from .env
api_key = os.getenv("OPENROUTER_API_KEY")
base_url = os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")

if not api_key:
    raise ValueError("OPENROUTER_API_KEY missing in .env")

# Initialize LLM (OpenRouter model)
llm = ChatOpenAI(
    model="meta-llama/llama-3-8b-instruct",
    temperature=0.7,
    max_tokens=256,
    api_key=api_key,
    base_url=base_url,
)

# Define prompt template for summarization
prompt_template = ChatPromptTemplate.from_template("""
Summarize the following news article in about 2-3 sentences.
Keep the tone professional and informative.
Avoid unnecessary details or promotional content.

Title: {title}
Content: {content}

Return only the summary text.
""")

output_parser = StrOutputParser()

CACHE_DIR = Path("data/cache")
CACHE_DIR.mkdir(parents=True, exist_ok=True)


def summarize_articles(articles):
    """
    Summarize list of article dicts.
    Each dict must contain 'title', 'description' or 'content'.
    """
    summaries = []

    for idx, article in enumerate(articles):
        title = article.get("title", "Untitled")
        content = article.get("description") or article.get("content") or ""
        if not content:
            continue  # skip if no content to summarize

        try:
            chain = prompt_template | llm | output_parser
            summary = chain.invoke({"title": title, "content": content})
        except Exception as e:
            summary = f"[Error summarizing article {idx+1}: {e}]"

        summaries.append({
            "title": title,
            "summary": summary.strip(),
            "url": article.get("url"),
        })

    # Save summaries locally for debugging
    with open(CACHE_DIR / "latest_summaries.json", "w", encoding="utf-8") as f:
        json.dump(summaries, f, indent=2, ensure_ascii=False)

    return summaries


# Test function
if __name__ == "__main__":
    from agents.fetcher_agent import run_fetcher
    print("Running summarizer_agent test...")

    articles = run_fetcher(page_size=3)
    summaries = summarize_articles(articles)

    for i, s in enumerate(summaries, 1):
        print(f"\n{i}. {s['title']}")
        print(f"Summary: {s['summary']}")
        print(f"Link: {s['url']}")
