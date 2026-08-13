from dotenv import load_dotenv

from langchain_groq import ChatGroq
from langchain_core.tools import tool
from langchain.agents import create_agent


load_dotenv()

llm = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0,
)

@tool
def calculator(a: float, b: float, operation: str) -> float:
    """
    Perform a basic mathematical calculation.

    operation can be:
    add, subtract, multiply, divide
    """

    if operation == "add":
        return a + b

    if operation == "subtract":
        return a - b

    if operation == "multiply":
        return a * b

    if operation == "divide":
        if b == 0:
            raise ValueError("Cannot divide by zero.")
        return a / b

    raise ValueError("Invalid operation.")


agent = create_agent(
    model=llm,
    tools=[calculator],
)

result = agent.invoke(
    {"messages": [
            {
                "role": "user",
                "content": "What is 25 multiplied by 8?"
            }
        ]
    }
)


print(result["messages"][-1].content)