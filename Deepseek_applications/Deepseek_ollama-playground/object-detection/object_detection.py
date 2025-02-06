from typing import List

import ollama
from pydantic import BaseModel

class Object(BaseModel):
    name: str
    color: List[str]
    count: int


class ObjectDetectionResponse(BaseModel):
    objects: list[Object]

res = ollama.chat(
    model="llama3.2-vision",
    messages=[
        {
            'role': 'user',
            'content': """Your task is to perform object detection on the image and return a structured output in JSON format. For each detected object, include the following attributes:
            Name: The name of the detected object (e.g., 'cat', 'car', 'person').
            Count: The total number of detected instances of this object type in the image.
            Color: The dominant color or primary colors of the object.
            """,
            'images': ['images/your_file.jpg']
        }
    ],
    format=ObjectDetectionResponse.model_json_schema(),
    options={'temperature': 0}
)

print(res['message']['content'])