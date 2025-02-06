import ollama
from pydantic import BaseModel

class Emotion(BaseModel):
    name: str
    score: float

class EmotionResponse(BaseModel):
    emotions: list[Emotion]

res = ollama.chat(
    model="llama3.2-vision",
    messages=[
        {
            'role': 'user',
            'content': """Analyze the facial expression in this image and provide the intensity of the following
             emotions as scores between 0 and 1.
             The emotions are: happiness, sadness, anger, fear, surprise, disgust, and neutral.
            """,
            'images': ['images/your_file.jpg']
        }
    ],
    format=EmotionResponse.model_json_schema(),
    options={'temperature': 0}
)

print(res['message']['content'])