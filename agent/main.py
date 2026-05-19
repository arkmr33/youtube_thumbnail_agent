# import sys
# from agent.graph import build_graph

# def run(topic: str):
#     app = build_graph()

#     state = {
#         "topic": topic,
#         "search_summary": "",
#         "current_prompt": "",
#         "image_path": "",
#         "rating": 0,
#         "critique": "",
#         "iteration": 0,
#         "target_rating": 8,
#         "max_iterations": 3,
#         "history": []
#     }

#     result = app.invoke(state)
#     print("\nFINAL OUTPUT:\n", result)


# if __name__ == "__main__":
#     run(topic)


import argparse
from graph import build_graph


def run(topic: str, stream: bool = False):
    app = build_graph()

    state = {
        "topic": topic,
        "search_summary": "",
        "current_prompt": "",
        "image_path": "",
        "rating": 0,
        "critique": "",
        "iteration": 0,
        "target_rating": 8,
        "max_iterations": 3,
        "output_dir": f"test_run/{topic}/",
        "history": []
    }

    if stream:
        print("\n=== STREAMING EXECUTION ===\n")

        for step in app.stream(state):
            print(step)
            print("\n-------------------\n")

    else:
        result = app.invoke(state)

        print("\n=== FINAL OUTPUT ===\n")
        print(result)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="YouTube Thumbnail Reflexion Agent"
    )

    parser.add_argument(
        "topic",
        type=str,
        nargs="?",
        default="Why Python is great for AI",
        help="Video topic for thumbnail generation"
    )

    parser.add_argument(
        "--stream",
        action="store_true",
        help="Stream LangGraph node execution"
    )

    args = parser.parse_args()

    run(args.topic, args.stream)