from langgraph.graph import StateGraph, START, END

from state import ThumbnailState

from nodes import (
    web_search_node,
    prompt_writer,
    generator,
    critic,
    saver,
    should_continue,
)


def build_graph():

    graph = StateGraph(ThumbnailState)

    graph.add_node("web_search_node", web_search_node)

    graph.add_node("prompt_writer", prompt_writer)

    graph.add_node("generator", generator)

    graph.add_node("critic", critic)

    graph.add_node("saver", saver)

    graph.add_edge(START, "web_search_node")

    graph.add_edge("web_search_node", "prompt_writer")

    graph.add_edge("prompt_writer", "generator")

    graph.add_edge("generator", "critic")

    graph.add_conditional_edges(
        "critic",
        should_continue,
        {
            "prompt_writer": "prompt_writer",
            "saver": "saver",
        }
    )

    graph.add_edge("saver", END)

    return graph.compile()