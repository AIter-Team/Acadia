from langgraph.graph import END, START, StateGraph

from acadia.utils.state import MainState
from acadia.utils.nodes import routing

def create_graph():
    graph = StateGraph(MainState)
    graph.add_node("routing", routing)

    graph.add_edge(START, "routing")
    graph.add_edge("routing", END)
    return graph