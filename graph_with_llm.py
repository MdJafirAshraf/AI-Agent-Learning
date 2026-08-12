from typing import TypedDict
from langchain_groq import ChatGroq
from langgraph.graph import StateGraph, START, END
from dotenv import load_dotenv

load_dotenv()

llm = ChatGroq(model='llama-3.1-8b-instant')

class State(TypedDict):
    messages: list
    response: str

def generate_response(state: State) -> State:
    messages = state['messages']
    respose = llm.invoke(messages)
    return {"response": respose.content}

graph = StateGraph(State)
graph.add_node("generate", generate_response)

graph.add_edge(START, "generate")
graph.add_edge("generate", END)

app = graph.compile()
print(app.get_graph().draw_ascii())

initial_state = {
    "messages": ["What is the Future of AI?"]
}
result = app.invoke(initial_state)
print("Final State:", result)