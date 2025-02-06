import os
from dotenv.main import load_dotenv
from termcolor import colored
from firecrawl import FirecrawlApp

load_dotenv()

# app = FirecrawlApp(
#     api_key=os.getenv("FIRECRAWL_API_KEY")
# )
app = FirecrawlApp(
    api_url="http://localhost:3002",
    api_key="nokey",
)

crawl_status = app.crawl_url(
    'https://firecrawl.dev', 
    params={
        "limit": 100,
        "scrapeOptions": {"formats": ["markdown", "html"]}
    },
    poll_interval=30
)
print(colored(crawl_status, "cyan"))