import os
from dotenv import load_dotenv

# This connects your script to the .env file
load_dotenv()

# We pull the keys into these variables
news_key = os.getenv('NEWS_API_KEY')
nyt_key = os.getenv('NYT_API_KEY')

print("--- API Key Check ---")
if news_key:
    print(f"NewsAPI Key found! (Ends in: ...{news_key[-2:]})")
else:
    print("NewsAPI Key NOT found.")

if nyt_key:
    print(f"NYT API Key found! (Ends in: ...{nyt_key[-2:]})")
else:
    print("NYT API Key NOT found.")