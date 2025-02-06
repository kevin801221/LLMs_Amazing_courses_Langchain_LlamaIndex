# Emotion Detection
A simple emotion detection project using Ollama's vision models to detect all the face emotions in an image.

You can watch the video on how it was built on my [YouTube](https://youtu.be/ZZHWLXyZHlA?si=1qP1cbtJnVPNPag_&t=475).

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
Add your invoice in the [images](images) folder, and make sure you replace the `your_file.jpg` with your invoice name in the [emotion_detection.py](emotion_detection.py) file.

# Run
Run the [emotion_detection.py](emotion_detection.py) file:

```bash
python emotion_detection.py
``` 