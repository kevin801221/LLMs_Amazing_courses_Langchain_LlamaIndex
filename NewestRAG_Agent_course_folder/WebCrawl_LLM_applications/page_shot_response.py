import requests

url = 'https://r.jina.ai/https://165.npa.gov.tw/#/'
headers = {
    'Authorization': 'Bearer "jina_api_key"',
    'X-Return-Format': 'pageshot'
}

response = requests.get(url, headers=headers)
print(response.text)
