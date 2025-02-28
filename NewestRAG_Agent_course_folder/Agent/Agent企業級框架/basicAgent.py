from upsonic import Agent, Task

task = Task("Do an in-depth analysis of US history")

agent = Agent("Historian")

agent.print_do(task)

