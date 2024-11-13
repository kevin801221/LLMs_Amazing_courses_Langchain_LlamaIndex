import os
import json
from dotenv.main import load_dotenv
from openai import OpenAI

from firecrawl import FirecrawlApp
from termcolor import colored

from transformers import AutoTokenizer

load_dotenv()

MODEL = "llama3-groq-70b-8192-tool-use-preview"

client = OpenAI(
    base_url="https://api.groq.com/openai/v1/",
    api_key=os.getenv("GROQ_API_KEY")
)

company = "Discord"
website = "https://discord.com"
data_points = [
    {"name": "catering_offering_for_employees", "value": None, "reference": None},
    {"name": "num_employess", "value": None, "reference": None},
    {"name": "office_locations", "value": None, "reference": None},
]

data_keys_to_search = [obj["name"] for obj in data_points if obj["value"] is None]
# print(colored(f"Data points to search: {data_keys_to_search}", "cyan"))

def scrape(url):
    app = FirecrawlApp(
        api_url="http://localhost:3002",
        api_key="nokey",
    )
    try:
        scraped_data = app.scrape_url(url)
    except Exception as error:
        print(colored(f"Unable to scrape the url: {url}", "red"))
        print(colored(f"Exception: {error}", "red"))
        return error
    
    return scraped_data["markdown"]

tools = [
    {
        "type": "function",
        "function": {
            "name": "scrape",
            "description": "Scrape a URL for information. Call this whenever you need to scrape a website, for example when you want to scrape a company information from a website.",
            "parameters": {
                "type": "object",
                "properties": {
                    "url": {
                        "type": "string",
                        "description": "the url of the website to scrape.",
                    },
                },
                "required": ["url"],
                "additionalProperties": False,
            },
        }
    }
]

system_prompt = f"""
    You are a world class web scraper, you are great at finding information on urls;
    
    You will keep scraping url base on information you received until ALL data points found;
    You will NOT stop until ALL missing data points are retrieved.
    
    You will try as hard as possible to search the web to find information about {company};
    You will search for the following data points:
    {data_keys_to_search}
    The values in data points are the answers of the data points name, and references are the url you scraping;
  
"""
user_prompt = f"""
    Please search the following company: {company}
    on the following website: {website}
    based on the data points of {data_keys_to_search}
"""
# print(colored(f"User Prompt: {user_prompt}", "yellow", "on_white"))

messages = [
    {"role": "system", "content": system_prompt},
    {"role": "user", "content": user_prompt}
]

response = client.chat.completions.create(
    model=MODEL,
    messages=messages,
    tools=tools,
)
print(colored(f"First AI response: {response}", "white", "on_blue"))

tool_calls = response.choices[0].message.tool_calls
print(colored(f"Tool Calls: {tool_calls}", "white", "on_red"))

if tool_calls:
    for tool_call in tool_calls:
        arguments = json.loads(tool_call.function.arguments)
        print(colored(f"Tool Call Arugments: {arguments}", "cyan"))
        
        url = arguments.get("url")
        scraped_data = scrape(url)
        print(colored(f"Scraped Data: {scraped_data}", "yellow"))
        
        def chunk_data(data, max_tokens):
            return [data[i:i + max_tokens] for i in range(0, len(data), max_tokens)]
            
        for chunk in chunk_data(scraped_data, 2000):
            
            function_call_result_message = {
                "role": "tool",
                "content": json.dumps({
                    "url": url,
                    "scraped_data": chunk,
                }),
                "tool_call_id": tool_call.id,
            }
            
            messages.append(function_call_result_message)
            
            tokenizer = AutoTokenizer.from_pretrained("Groq/Llama-3-Groq-70B-Tool-Use")
            
            if len(messages) > 4 or len(tokenizer.tokenize(chunk)) > 8192:
                latest_messages = messages[-4:]
            
                chat_response = client.chat.completions.create(
                    model=MODEL,
                    messages=latest_messages,
                )
                
                print(colored(f"{chat_response.choices[0].message.content}", "black", "on_blue"))