# Object Detection
A simple object detection project using Ollama's vision models to detect objects in images and extract information about them.

You can watch the video on how it was built on my [YouTube](https://youtu.be/ZZHWLXyZHlA?si=nRnxMuhEmvQ4kPxc&t=673).

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
Add your invoice in the [images](images) folder, and make sure you replace the `your_file.jpg` with your invoice name in the [object_detection.py](object_detection.py) file.

# Run
Run the [object_detection.py](object_detection.py) file:

```bash
python object_detection.py
``` 