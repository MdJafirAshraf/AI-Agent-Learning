from typing import TypedDict
from langgraph.graph import StateGraph, START, END


class PatientState(TypedDict):
    patient_name: str
    physician_notes: str
    cardiologist_notes: str
    surgical_notes: str


def general_physician_node(state: PatientState) -> dict:
    print("General Physician Node")

    notes = "Patient reports chest pain and shortness of breath. Recommending further cardiac evaluation."
    return {"physician_notes": notes}

def cardiologist_node(state: PatientState) -> dict:
    print("Cardiologist Node")

    notes = "Cardiologist evaluation indicates possible arrhythmia. Suggesting further tests and monitoring."
    return {"cardiologist_notes": notes}

def surgical_node(state: PatientState) -> dict:
    print("Surgical Node")

    notes = "Surgical evaluation suggests that the patient may require a procedure based on test results."
    return {"surgical_notes": notes}

# Create the state graph
builder = StateGraph(PatientState)

# Add nodes to the graph
builder.add_node("physician", general_physician_node)
builder.add_node("cardiologist", cardiologist_node)
builder.add_node("surgical", surgical_node)

# Define the edges between nodes
builder.add_edge(START, "physician")
builder.add_edge("physician", "cardiologist")
builder.add_edge("cardiologist", "surgical")
builder.add_edge("surgical", END)

# Compile the graph
graph = builder.compile()
print(graph.get_graph().draw_ascii())

initial_state: PatientState = {
    "patient_name": "John Doe",
    "physician_notes": "",
    "cardiologist_notes": "",
    "surgical_notes": ""
}

# Invoke the graph with the initial state
final_state = graph.invoke(initial_state)
print("Final State:", final_state)
