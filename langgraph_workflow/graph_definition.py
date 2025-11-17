# langgraph_workflow/graph_definition.py

from utils.logger import setup_logger

# Import agents
from agents.fetcher_agent import run_fetcher
from agents.summarizer_agent import summarize_articles
from agents.writer_agent import generate_newsletter
from agents.mailer_agent import run_mailer

logger = setup_logger("workflow")

def run_newsletter_workflow():
    """
    Executes the full newsletter pipeline step by step.
    """
    logger.info("🚀 Starting AI Newsletter Workflow...")

    # --- Step 1: Fetch News ---
    logger.info("Step 1: Fetching AI news...")
    articles = run_fetcher(page_size=5)
    logger.info(f"Fetched {len(articles)} articles successfully.")

    # --- Step 2: Summarize Articles ---
    logger.info("Step 2: Summarizing articles...")
    summaries = summarize_articles(articles)
    logger.info(f"Generated {len(summaries)} summaries.")

    # --- Step 3: Write Newsletter ---
    logger.info("Step 3: Creating newsletter...")
    newsletter_html = generate_newsletter(summaries)
    logger.info("Newsletter HTML generated successfully.")

    # --- Step 4: Send Emails ---
    logger.info("Step 4: Sending emails to subscribers...")
    run_mailer()
    logger.info("Emails sent successfully ✅")

    logger.info("🎉 Newsletter Workflow Completed Successfully!")

    return {
        "articles_fetched": len(articles),
        "summaries_created": len(summaries),
        "newsletter_path": "data/cache/newsletter.html",
    }

if __name__ == "__main__":
    result = run_newsletter_workflow()
    print(result)
