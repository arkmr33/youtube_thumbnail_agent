from agent.graph import build_graph


def main():

    graph = build_graph()

    png = graph.get_graph().draw_mermaid_png()

    with open("graph.png", "wb") as f:
        f.write(png)

    print("Saved graph.png")


if __name__ == "__main__":
    main()