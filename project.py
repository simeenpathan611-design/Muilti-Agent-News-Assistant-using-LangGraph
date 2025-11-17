import os

# Define folder structure directly inside 'newsassistant'
folders = [
    "config",
    "data/logs",
    "data/cache",
    "agents",
    "utils",
    "langgraph_workflow",
]

# Define files with initial content
files = {
    "main.py": "# Entry point for AI Newsletter Agent\n\nif __name__ == '__main__':\n    print('Run the AI Newsletter Agent workflow...')\n",
    "config/__init__.py": "",
    "config/settings.py": "import os\nfrom dotenv import load_dotenv\n\nload_dotenv()\n\nNEWS_API_KEY = os.getenv('NEWS_API_KEY')\nEMAIL_USER = os.getenv('EMAIL_USER')\nEMAIL_PASS = os.getenv('EMAIL_PASS')\nTOPIC = 'Artificial Intelligence'\n",
    "config/prompts.py": "# Prompt templates for summarizer, validator, and writer\n",
    "data/subscribers.json": "[\n    {\n        \"name\": \"John Doe\",\n        \"email\": \"john@example.com\"\n    }\n]\n",
    "agents/__init__.py": "",
    "agents/fetcher_agent.py": "# Fetches AI news from NewsAPI\n",
    "agents/summarizer_agent.py": "# Summarizes fetched AI news\n",
    "agents/validator_agent.py": "# Validates summaries for factual correctness\n",
    "agents/writer_agent.py": "# Generates newsletter content in email format\n",
    "agents/categorizer_agent.py": "# Categorizes news into sections (Research, Startups, Policy, etc.)\n",
    "agents/mailer_agent.py": "# Sends the final newsletter to subscribers\n",
    "utils/__init__.py": "",
    "utils/email_utils.py": "# Handles email sending via SMTP or API\n",
    "utils/api_utils.py": "# Handles external API requests like NewsAPI\n",
    "utils/db_utils.py": "# Reads and updates subscriber data\n",
    "utils/logger.py": "# Sets up logging\n",
    "langgraph_workflow/__init__.py": "",
    "langgraph_workflow/graph_definition.py": "# Defines the LangGraph nodes and connections\n",
    "langgraph_workflow/scheduler.py": "# Handles daily scheduling (cron/APScheduler)\n",
    "requirements.txt": "langchain\nlanggraph\nopenai\nrequests\npython-dotenv\napscheduler\n",
    "README.md": "# AI Newsletter Agent\n\nAutomated daily newsletter on AI updates using LangGraph agents.\n",
    ".env": "NEWS_API_KEY=your_newsapi_key_here\nEMAIL_USER=your_email@gmail.com\nEMAIL_PASS=your_password_here\n",
}

# Create folders
for folder in folders:
    os.makedirs(folder, exist_ok=True)

# Create files with content
for filepath, content in files.items():
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

print("✅ Folder structure for 'newsassistant' project created successfully!")
