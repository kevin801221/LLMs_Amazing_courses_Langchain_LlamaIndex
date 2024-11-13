import requests
from bs4 import BeautifulSoup

import getpass

#ANSI code
PINK = "\033[95m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
RESET_COLOR = "\033[0m"

def beautifulsoup_web_scrape_url(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    return str(soup)

url = "https://www.discoverhongkong.com/tc/plan/traveller-info/e-guidebooks.html"
pdf_url = "https://www.discoverhongkong.com/content/dam/dhk/intl/plan/traveller-info/e-guidebooks/foodmap-tc.pdf"

data = beautifulsoup_web_scrape_url(pdf_url)
# print(f"{CYAN}{data}{RESET_COLOR}")

def jinai_readerapi_web_scraper(url):
    headers = {"Accept": "application/json"}
    response = requests.get(f"https://r.jina.ai/{url}", headers=headers)
    return response.text

data = jinai_readerapi_web_scraper(pdf_url)
print(f"{CYAN}{data}{RESET_COLOR}")

def jina_readerapi_search(query):
    full_url = f"https://s.jina.ai/{query}"
    response = requests.get(full_url)
    return response.text

data = jina_readerapi_search("伊隆馬斯克最近有什麼新聞？")
print(f"{PINK}{data}{RESET_COLOR}")

def jina_readerapi_grounding(description):
    headers = {}
    api_key = getpass.getpass("請輸入您的Jian API Key: ")
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"
        
    full_url = f"https://g.jina.ai/{description}"
    response = requests.get(full_url, headers=headers)
    return response.text

data = jina_readerapi_grounding("Udemy的總部在台灣")
print(f"{CYAN}{data}{RESET_COLOR}")