import os
from dotenv import load_dotenv

load_dotenv()

NEWS_API_KEY = os.getenv('NEWS_API_KEY')
EMAIL_USER = os.getenv('EMAIL_USER')
EMAIL_PASS = os.getenv('EMAIL_PASS')
TOPIC = 'Artificial Intelligence'
