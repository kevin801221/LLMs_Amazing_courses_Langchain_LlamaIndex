# OCR (Optical Character Recognition)
A simple OCR project using Ollama's vision models to extract text from invoices, receipts, etc.

You can watch the video on how it was built on my [YouTube](https://youtu.be/ZZHWLXyZHlA?si=6BSOXiDObXcTCQgk&t=191).

# Pre-requisites
Install Ollama on your local machine from the [official website](https://ollama.com/). And then pull the llama vision model:

```bash
ollama pull llama3.2-vision
```

Install the dependencies using pip:

```bash
pip install -r requirements.txt
```

# Configuration 
Add your invoice in the [images](images) folder, and make sure you replace the `your_file.jpg` with your invoice name in the [invoice_text_extractor.py](invoice_text_extractor.py) file.

# Run
Run the [invoice_text_extractor.py](invoice_text_extractor.py) file:

```bash
python invoice_text_extractor.py
``` 