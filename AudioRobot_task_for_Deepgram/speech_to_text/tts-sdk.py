import os
from dotenv import load_dotenv

from deepgram import (
    DeepgramClient,
    SpeakOptions
)

load_dotenv()

SPEAK_OPTIONS = {
    "text": "Hello, Ken, Good afternoon."
}
filename = "output-sdk.wav"

def main():
    try:
        deepgram = DeepgramClient(
            api_key=os.getenv("DEEPGRAM_API_KEY")
        )

        options = SpeakOptions(
            model="aura-luna-en",
            encoding="linear16",
            container="wav"
        )

        response = deepgram.speak.v("1").save(filename, SPEAK_OPTIONS, options)

        print(response.to_json(indent=4))

    except Exception as error:
        print(f"Exception: {error}")

if __name__=="__main__":
    main()