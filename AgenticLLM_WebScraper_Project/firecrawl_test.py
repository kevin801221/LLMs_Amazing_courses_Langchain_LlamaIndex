from firecrawl import FirecrawlApp

app = FirecrawlApp(api_key="")

# Scrape a website:
scrape_result = app.crawl_url('https://medium.com/kaggle-blog', params={'formats': ['markdown', 'html']})
print(scrape_result)
