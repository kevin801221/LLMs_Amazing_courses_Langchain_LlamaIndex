from typing import List

import ollama
from pydantic import BaseModel

class Item(BaseModel):
    name: str
    quantity: int
    price: float

class Invoice(BaseModel):
    invoice_number: str
    date: str
    vendor_name: str
    items: List[Item]
    total: float

res = ollama.chat(
    model="llama3.2-vision",
    messages=[
        {
            'role': 'user',
            'content': """Given an invoice image, Your task is to use OCR to detect and extract text, categorize it into predefined fields.
            Invoice/Receipt Number: The unique identifier of the document.
            Date: The issue or transaction date.
            Vendor Name: The business or entity issuing the document.
            Items: A list of purchased products or services with Name, Quantity and price.""",
            'images': ['images/your_file.jpg']
        }
    ],
    format=Invoice.model_json_schema(),
    options={'temperature': 0}
)

print(res['message']['content'])