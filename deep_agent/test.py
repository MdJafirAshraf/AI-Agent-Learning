from deepagents import create_deep_agent
from langchain_core.tools import tool


@tool
def get_customer(customer_id: int) -> dict:
    """Get customer information by customer ID."""

    customers = {
        1: {
            "id": 1,
            "name": "Jafir",
            "email": "jafir@example.com",
            "status": "active",
        },
        2: {
            "id": 2,
            "name": "Ahmed",
            "email": "ahmed@example.com",
            "status": "inactive",
        },
    }

    return customers.get(
        customer_id,
        {"error": "Customer not found"},
    )


agent = create_deep_agent(
    model="openai:gpt-5.5",
    tools=[get_customer],
    system_prompt="""
    You are a customer support agent.

    When the user asks about a customer,
    use the get_customer tool to retrieve the information.
    """
)


result = agent.invoke(
    {
        "messages": [
            {
                "role": "user",
                "content": "Get customer 1 and tell me their status."
            }
        ]
    }
)

print(result["messages"][-1].content)