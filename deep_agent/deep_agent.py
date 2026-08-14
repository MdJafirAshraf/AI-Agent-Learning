from deepagents import create_deep_agent
from langchain_groq import ChatGroq

from prompts import MAIN_SYSTEM_PROMPT, ORDER_AGENT_PROMPT
from tools import get_customer, get_customer_orders, get_order, get_customers_by_city
from middleware.logging_middleware import LoggingMiddleware

from dotenv import load_dotenv
load_dotenv()

model = ChatGroq(model="openai/gpt-oss-120b", temperature=0.4)

# Main Agent
agent = create_deep_agent(
    model=model,
    tools=[get_customer, get_order, get_customers_by_city],
    middleware=[LoggingMiddleware()],
    subagents=[{
        "name": "order_specialist",
        "description": """
            Specialist for customer order analysis.

            Use this specialist when you need to:
            - Get customer orders
            - Calculate order totals
            - Find pending orders
            - Find delivered orders
        """,

        "system_prompt": ORDER_AGENT_PROMPT,
        "tools": [get_customer_orders,],
    }],
    system_prompt=MAIN_SYSTEM_PROMPT
)

# Run Agent
result = agent.invoke({
    "messages": [{
        "role": "user",
        "content": """
        Analyze customer 1.

        I need:
        1. Customer information
        2. All orders
        3. Total order amount
        4. Pending orders
        5. Delivered orders
        6. Final summary

        This is a multi-step task.
        Create and follow a plan.
        """
    }]
})

# result = agent.invoke(
#     {"messages": [{
#         "role": "user",
#         "content": """
#         Get all orders for customer 1.

#         You MUST delegate this task
#         to order_specialist.
#         """
#         }
#     ]})


from io import BytesIO
import os
from PIL import Image
img_bytes = agent.get_graph(xray=True).draw_mermaid_png()
img = Image.open(BytesIO(img_bytes))
img.show()

for message in result["messages"]:
    print("\n---")
    print(message.content)
