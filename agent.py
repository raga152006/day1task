import json

from config import client, MODEL, QUESTIONS, banner
from tools import TOOLS, TOOL_FUNCTIONS


SYSTEM_PROMPT = """
You are a college fee assistant.

Never guess a fee: always use get_course_fee.
Use calculator for any arithmetic.

Available course codes:
CS101, AI202, DS303.

If no tool is needed, answer directly.
"""


def agent(question, max_steps=6, verbose=True):

    messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        },
        {
            "role": "user",
            "content": question
        }
    ]

    for step in range(1, max_steps + 1):

        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            tools=TOOLS,
            tool_choice="auto",
            temperature=0
        )

        message = response.choices[0].message

        # If the model does not need a tool,
        # return its final answer.
        if not message.tool_calls:
            return message.content

        # Add the assistant's tool request
        # to the conversation.
        messages.append(message)

        # Execute every tool requested by the model.
        for tool_call in message.tool_calls:

            name = tool_call.function.name
            arguments = json.loads(tool_call.function.arguments)

            function = TOOL_FUNCTIONS.get(name)

            if function is None:
                result = f"Unknown tool: {name}"
            else:
                result = function(**arguments)

            if verbose:
                print(
                    f"step {step}: "
                    f"{name}({arguments}) -> {result}"
                )

            # Give the tool result back to the model.
            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": str(result)
                }
            )

    return "Agent stopped: maximum number of steps reached."


if __name__ == "__main__":

    banner("AI AGENT")

    for question in QUESTIONS:

        print("Q:", question)

        answer = agent(question)

        print("A:", answer)
        print()