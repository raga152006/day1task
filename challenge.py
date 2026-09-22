from workflow import workflow
from agent import agent


QUESTION = "I can pay Rs. 30,000. Which two courses can I take together within this budget?"


print("Q:", QUESTION)

print("\nWorkflow:")
print(workflow(QUESTION))

print("\nAgent:")
print(agent(QUESTION))