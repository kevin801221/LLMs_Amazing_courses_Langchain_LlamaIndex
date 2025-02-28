# import os
# print(os.getenv('OPENAI_API_KEY'))
# print(os.getenv('TAVILY_API_KEY'))
from upsonic import Task, Agent

task = Task("Who developed Tensor?")

agent = Agent("Physic teacher")

agent.print_do(task)