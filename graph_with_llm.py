from typing import TypedDict
from langchain_groq import ChatGroq
from langgraph.graph import StateGraph, START, END
from langchain_core.messages import SystemMessage, HumanMessage
from dotenv import load_dotenv

load_dotenv()

llm = ChatGroq(
    model='llama-3.1-8b-instant',
    temperature=0.7,
)

class State(TypedDict):
    messages: list
    response: str

def generate_response(state: State) -> State:
    messages = state['messages']
    response = llm.invoke(messages)
    return {"response": response.content}

graph = StateGraph(State)
graph.add_node("generate", generate_response)

graph.add_edge(START, "generate")
graph.add_edge("generate", END)

app = graph.compile()
print(app.get_graph().draw_ascii())

SYSTEM_PROMPT = """
You are a professional fitness assistant.

Your responsibilities:
- Provide concise and practical fitness guidance.
- Give safe, general information.
- Do not diagnose medical conditions.
- If the question requires medical advice, recommend consulting a qualified professional.
- Keep normal responses within 2-3 sentences.
"""


messages = [
    SystemMessage(content=SYSTEM_PROMPT),
    HumanMessage(
        content="What is the calorie burn for a 1 hour workout session of moderate intensity?"
    )
]

initial_state = {
    "messages": messages
}
result = app.invoke(initial_state)
print("Final State:", result)