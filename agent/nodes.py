import os
import json
import base64
import shutil
import requests

from pathlib import Path
from pydantic import BaseModel, Field

from groq import Groq
from langchain_groq import ChatGroq

from prompts import PROMPT_WRITER_SYSTEM, CRITIC_SYSTEM
from tools import web_search


# -------------------------
# CLIENTS
# -------------------------

groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

writer_llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    api_key=os.getenv("GROQ_API_KEY"),
    temperature=0.7
)


# -------------------------
# STRUCTURED OUTPUT
# -------------------------

class CriticOutput(BaseModel):
    rating: int = Field(..., ge=1, le=10)
    critique: str


# -------------------------
# NODE 1: WEB SEARCH
# -------------------------

def web_search_node(state):
    return web_search(state)


# -------------------------
# NODE 2: PROMPT WRITER
# -------------------------

def prompt_writer(state):

    prompt = f"""
{PROMPT_WRITER_SYSTEM}

TOPIC: {state['topic']}

SEARCH:
{state['search_summary']}

PREVIOUS CRITIQUE:
{state.get('critique','')}

Write ONE improved thumbnail prompt.
"""

    res = writer_llm.invoke(prompt)

    return {"current_prompt": res.content}


# -------------------------
# NODE 3: IMAGE GENERATOR (NVIDIA FLUX)
# -------------------------

def generator(state):

    iteration = state["iteration"] + 1

    out_dir = Path(state["output_dir"])
    out_dir.mkdir(parents=True, exist_ok=True)

    image_path = out_dir / f"iter_{iteration}.png"

    invoke_url = "https://ai.api.nvidia.com/v1/genai/black-forest-labs/flux.2-klein-4b"

    headers = {
        "Authorization": f"Bearer {os.getenv('NVIDIA_API_KEY')}",
        "Accept": "application/json",
    }

    payload = {
        "prompt": state["current_prompt"],
        "width": 512,
        "height": 512,
        "seed": iteration,
        "steps": 4
    }

    r = requests.post(invoke_url, headers=headers, json=payload)
    r.raise_for_status()
    data = r.json()

    image_url = data.get("image") or data.get("output", [None])[0]

    img = requests.get(image_url).content

    with open(image_path, "wb") as f:
        f.write(img)

    return {
        "image_path": str(image_path),
        "iteration": iteration
    }


# -------------------------
# NODE 4: CRITIC (LLAMA 4 SCOUT)
# -------------------------

def critic(state):

    img_bytes = Path(state["image_path"]).read_bytes()
    img_b64 = base64.b64encode(img_bytes).decode()

    res = groq_client.chat.completions.create(
        model="meta-llama/llama-4-scout-17b-16e-instruct",
        temperature=0,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": f"""
{CRITIC_SYSTEM}

Return ONLY JSON:
{{
  "rating": 1-10,
  "critique": "feedback"
}}

TOPIC: {state['topic']}
"""
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/png;base64,{img_b64}"
                        }
                    }
                ]
            }
        ]
    )

    raw = res.choices[0].message.content

    try:
        parsed = json.loads(raw)
    except:
        parsed = {"rating": 5, "critique": "parse error"}

    result = CriticOutput(**parsed)

    history_item = {
        "iteration": state["iteration"],
        "prompt": state["current_prompt"],
        "image_path": state["image_path"],
        "rating": result.rating,
        "critique": result.critique
    }

    return {
        "rating": result.rating,
        "critique": result.critique,
        "history": [history_item]
    }


# -------------------------
# CONDITION
# -------------------------

def should_continue(state):

    if state["rating"] >= state["target_rating"] or state["iteration"] >= state["max_iterations"]:
        return "saver"

    return "prompt_writer"


# -------------------------
# NODE 5: SAVER
# -------------------------

def saver(state):

    out = Path(state["output_dir"])

    best = max(state["history"], key=lambda x: x["rating"])

    shutil.copy(best["image_path"], out / "final.png")

    report = out / "report.md"

    text = ["# Thumbnail Report\n", f"Topic: {state['topic']}\n"]

    for h in state["history"]:
        text.append("---")
        text.append(f"Iteration {h['iteration']}")
        text.append(f"Rating: {h['rating']}")
        text.append(f"Critique: {h['critique']}")
        text.append(f"Prompt:\n{h['prompt']}\n")

    report.write_text("\n".join(text))

    return {}