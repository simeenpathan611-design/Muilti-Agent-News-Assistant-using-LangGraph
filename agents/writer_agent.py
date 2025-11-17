# # Generates newsletter content in email format
# # agents/writer_agent.py

import os
import json
from datetime import datetime
from dotenv import load_dotenv
from pathlib import Path
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

# Get API details
api_key = os.getenv("OPENROUTER_API_KEY")
base_url = os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")

if not api_key:
    raise ValueError("OPENROUTER_API_KEY missing in .env")

# Initialize LLM
llm = ChatOpenAI(
    model="meta-llama/llama-3-8b-instruct",
    temperature=0.7,
    max_tokens=2500,
    api_key=api_key,
    base_url=base_url,
)

# HTML newsletter template prompt
# prompt_template = ChatPromptTemplate.from_template("""
# You are an expert newsletter writer for an AI news digest.

# Write a professional and engaging newsletter in **HTML format** that includes:
# - A short introductory paragraph about the latest AI trends.
# - The summarized articles formatted as sections with:
#   - The title as a bold clickable link.
#   - The short summary below it.
# - A closing note like "Stay tuned for more AI insights!"

# Articles:
# {articles_json}

# Return only the final HTML code.
# """)

prompt_template = ChatPromptTemplate.from_template("""
You are an expert newsletter writer for an AI news digest.

Write a professional and engaging newsletter in HTML format ONLY (no markdown, no **bold**, no markdown-style formatting).

Generate a newsletter in HTML format.

IMPORTANT: Return ONLY the HTML code, starting with <html> tag.
Do not include any explanatory text before or after the HTML.

IMPORTANT:
- Never output markdown.
- Never output **bold**.
- Never wrap text inside {{ }} unless part of HTML.
- Only use clean HTML.

For each article inside the JSON:
- Use a <div> card.
- Show <h2> for the title.
- Show <p> for the summary.
- Use: <a href="ARTICLE_URL">Read full article</a>


STYLE REQUIREMENTS:
Return HTML exactly in this structure (curly braces escaped):

<html>
  <body style="background-color:#0e1117; color:white; font-family:Arial; padding:25px;">
    <h1 style="text-align:center; color:#61dafb;">AI Newsletter Digest</h1>

    <p style="font-size:16px; opacity:0.9;">
      Write a short introduction about today's AI news.
    </p>

    <!-- Article card example -->
    <div style="background-color:#1a1f25; padding:20px; border-radius:10px; margin-bottom:25px;">
      <h2 style="color:#61dafb;">ARTICLE_TITLE</h2>
      <p>ARTICLE_SUMMARY</p>
      <a href="ARTICLE_URL" style="color:#ff9f1c;">Read full article</a>
    </div>

    <p style="margin-top:40px;">Stay tuned for more AI insights!</p>
  </body>
</html>

ARTICLES JSON:
{articles_json}

Return ONLY valid HTML. No markdown. No extraneous characters.

Do not stop early. Generate the complete HTML until the final </html> tag.

""")




output_parser = StrOutputParser()

CACHE_DIR = Path("data/cache")
CACHE_DIR.mkdir(parents=True, exist_ok=True)

def generate_newsletter(summaries):
    """Takes list of {title, summary, url} dicts and returns HTML newsletter string."""
    try:
        articles_json = json.dumps(summaries, ensure_ascii=False, indent=2)
        chain = prompt_template | llm | output_parser
        newsletter_html = chain.invoke({"articles_json": articles_json})
    except Exception as e:
        raise RuntimeError(f"Newsletter generation failed: {e}")

    # Save HTML to cache
    #output_path = CACHE_DIR / "newsletter.html"
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    output_path = CACHE_DIR / f"newsletter_{timestamp}.html"

    # Also update the latest pointer
    latest_path = CACHE_DIR / "newsletter.html"
    with open(latest_path, "w", encoding="utf-8") as f:
        f.write(newsletter_html)


    return newsletter_html


# ✅ Test code
if __name__ == "__main__":
    from agents.summarizer_agent import summarize_articles
    from agents.fetcher_agent import run_fetcher

    print("Running writer_agent test...")

    # Fetch & summarize first
    articles = run_fetcher(page_size=3)
    summaries = summarize_articles(articles)

    # Generate newsletter
    newsletter_html = generate_newsletter(summaries)

    print("\n✅ Newsletter generated successfully! Preview:")
    print(newsletter_html[:600], "...")  # preview first few lines
    print("\nSaved at: data/cache/newsletter.html")
