import requests
import json
from termcolor import colored
import getpass

from numpy.linalg import norm
import numpy as np

url = "https://api.jina.ai/v1/embeddings"
api_key = getpass.getpass("請輸入您的Jian API Key: ")
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}"
}
data = {
    "model": "jina-embeddings-v3",
    "task": "text-matching",
    "dimensions": 1024,
    "late_chunking": False,
    "embedding_type": "float",
    "input": [
        "Organic skincare for sensitive skin",
        "針對敏感肌膚的天然護膚產品",
    ]
}
response = requests.post(url, headers=headers, json=data)
result = json.dumps(response.json(), indent=2)
# print(colored(result, "cyan"))

cos_sin = lambda a, b: (a @ b.T) / norm(a) * norm(b)

parsed_data = json.loads(result)
embeddings = parsed_data["data"]

a = np.array(embeddings[0]["embedding"], dtype=np.float32)
b = np.array(embeddings[1]["embedding"], dtype=np.float32)
print(colored(cos_sin(a, b), "light_magenta"))