from typing import TypedDict, Annotated
import operator


class ThumbnailState(TypedDict):
    topic: str

    search_summary: str

    current_prompt: str

    image_path: str

    rating: int

    critique: str

    iteration: int

    target_rating: int

    max_iterations: int

    output_dir: str

    history: Annotated[list, operator.add]