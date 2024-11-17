from firecrawl import FirecrawlApp

app = FirecrawlApp(api_key="fc-d92bfd051afd4a91b71f48c78aa9b871")

# Scrape a website:
scrape_result = app.crawl_url('https://medium.com/kaggle-blog', params={'formats': ['markdown', 'html']})
print(scrape_result)
