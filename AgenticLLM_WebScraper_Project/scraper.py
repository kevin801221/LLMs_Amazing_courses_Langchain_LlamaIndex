import json
from scrapegraphai.graphs import SmartScraperGraph
# Fetch -> Parse -> RAG -> Generate Answer
import os
from dotenv.main import load_dotenv

load_dotenv()

#ANSI code
PINK = "\033[95m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
RESET_COLOR = "\033[0m"

graph_config = {
    "llm": {
        "model": "ollama/llama3.2",
        "temperature": 1,
        "format": "json",
        "model_tokens": 2000,
        "base_url": "http://localhost:11434",
    },
    "embeddings": {
        "model": "ollama/nomic-embed-text",
        "temperature": 0,
        "base_url": "http://localhost:11434",
    }
}

smart_scraper_graph = SmartScraperGraph(
    prompt="List me all the projects with description.",
    source="https://perinim.github.io/projects/",
    config=graph_config,
)

result = smart_scraper_graph.run()
# print(f"{CYAN}{result}{RESET_COLOR}")

output = json.dumps(result, indent=2)
lines = output.split("\n")

for line in lines:
    print(f"{PINK}{line}{RESET_COLOR}")