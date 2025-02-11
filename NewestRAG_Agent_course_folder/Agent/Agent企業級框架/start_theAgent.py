from upsonic import Task, Agent

task = Task("Who developed you?")

agent = Agent("Coder")

agent.print_do(task)