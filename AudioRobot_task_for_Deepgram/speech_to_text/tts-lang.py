import os
from dotenv import load_dotenv
import requests

load_dotenv()
dg_api_key = os.getenv("DEEPGRAM_API_KEY")

model = "aura-stella-en"
url = f"https://api.deepgram.com/v1/speak?model={model}"

headers = {
    "Authorization": f"Token {dg_api_key}",
    "Content-Type": "application/json"
}

payload = {
    "text": "Hello, Ken, How can I help you? My name is Emma and I'm very glad to meet you. What do you think of the Text-To-Speech API?"
}

response = requests.post(
    url,
    headers=headers,
    json=payload,
    stream=True
)

audio_file_path = "output-stream.wav"

if response.status_code == 200:
    with open(audio_file_path, "wb") as f:
        # f.write(response.content)
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)
        print("File save successfully!")
else:
    print(f"Error: {response.status_code} - {response.text}")