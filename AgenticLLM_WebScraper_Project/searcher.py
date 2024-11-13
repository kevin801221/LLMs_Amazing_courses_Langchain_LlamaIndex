import json
from scrapegraphai.graphs import ScriptCreatorGraph
from scrapegraphai.graphs import SearchGraph
#ANSI code
PINK = "\033[95m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
RESET_COLOR = "\033[0m"

graph_config = {
    "llm": {
        "model": "ollama/llama3.2",
        "temperature": 0.5,
        "format": "json",
        "model_tokens": 6000,
        "base_url": "http://localhost:11434"
    },
    "library": "beautifulsoup4",
    # "embeddings": {
    #     "model": "ollama/nomic-embed-text",
    #     "temperature": 0,
    #     "base_url": "http://localhost:11434",
    # }
}

# source = [
#     "https://www.google.com",
#     "https://www.udemy.com/courses/development/data-science/"
# ]

script_creator_graph = ScriptCreatorGraph(
    prompt="Create a Python script to scrape the projects ",
    source="https://perinim.github.io/projects",
    config=graph_config,
)
script_creator_graph = ScriptCreatorGraph(
    prompt="Display the top 10 courses with the most students enrolled in computer vision,and display the course names, teacher names, ratings, and number of enrolled students of those courses",
    source="https://www.udemy.com",
    config=graph_config,
)

result = script_creator_graph.run()
print(f"{CYAN}{result}{RESET_COLOR}")

# output = json.dumps(result, indent=2)
# lines = output.split("/n")

# for line in lines:
#     print(f"{CYAN}{line}{RESET_COLOR}")