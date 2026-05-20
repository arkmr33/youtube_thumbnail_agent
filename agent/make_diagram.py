from graph import build_graph
from pathlib import Path

output_path = Path(__file__).parent / "graph.png"


def main():

    graph = build_graph()

    png = graph.get_graph().draw_mermaid_png(
        max_retries=5,
        retry_delay=2.0,
    )

    with open(output_path, "wb") as f:
        f.write(png)

    print(f"Saved to {output_path}")


if __name__ == "__main__":
    main()