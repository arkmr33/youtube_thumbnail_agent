# 🎯 YouTube Thumbnail Designer — Reflexion Agent

An AI-powered autonomous agent that generates and improves YouTube thumbnails using iterative self-reflection.

Built using:

* LangGraph
* Groq LLMs
* NVIDIA FLUX Image Generation
* Vision-based Critique Loop

---

# 🚀 Overview

This project demonstrates how AI agents can autonomously improve creative outputs using a feedback loop architecture.

Given a YouTube video topic, the agent:

1. Searches the web for inspiration
2. Writes an optimized thumbnail prompt
3. Generates a thumbnail image
4. Critiques the generated image using a vision model
5. Refines the prompt using feedback
6. Repeats until the thumbnail quality improves

The system follows a Reflexion-style iterative workflow where the AI learns from its own mistakes across multiple iterations.

---

# 🧠 Agent Workflow

The workflow is implemented using LangGraph.

```text
START
  ↓
Web Search
  ↓
Prompt Writer
  ↓
Image Generator
  ↓
Vision Critic
  ↓
Condition Check
  ├── Continue Loop
  └── Save Final Output
```

---

# ⚙️ Technologies Used

| Component         | Technology    |
| ----------------- | ------------- |
| Agent Framework   | LangGraph     |
| LLM Provider      | Groq          |
| Prompt Generation | Llama 3.3 70B |
| Vision Critique   | Llama 4 Scout |
| Image Generation  | NVIDIA FLUX   |
| Web Search        | Tavily        |
| Validation        | Pydantic      |

---

# 📂 Project Structure

```text
project/
│
├── graph.py
├── nodes.py
├── prompts.py
├── tools.py
├── state.py
├── main.py
│
├── outputs/
│   ├── final.png
│   └── report.md
│
└── README.md
```

---

# 🔄 Workflow Explanation

## 1. Web Search Node

The agent first searches the web for:

* YouTube thumbnail trends
* High CTR thumbnail styles
* Visual inspiration
* Design references

The search results are summarized and passed into the prompt generation stage.

---

## 2. Prompt Writer Node

A Groq LLM generates a concise thumbnail generation prompt based on:

* Video topic
* Search results
* Previous critique feedback

The prompt is optimized for image generation quality.

---

## 3. Image Generator Node

The generated prompt is sent to NVIDIA FLUX to create a thumbnail image.

Generation settings:

* Resolution: 512 × 512
* Seed: iteration-based
* Fast inference steps

The image is saved locally for evaluation.

---

## 4. Critic Node

A multimodal vision model(GROQ LLAMA 4 SCOUT) analyzes the generated thumbnail.

The model evaluates:

* Readability
* Composition
* Contrast
* Emotional impact
* Click-through appeal
* Visual clarity

The critic returns:

* Numerical rating
* Improvement feedback

Example:

```json
{
  "rating": 7,
  "critique": "Good composition but text readability is weak."
}
```

---

## 5. Reflexion Loop

The critique feedback is sent back into the prompt writer.

The system improves the next thumbnail generation attempt using:

* previous mistakes
* visual weaknesses
* composition feedback

This loop continues until:

* target quality score is reached
  OR
* maximum iterations are completed

---

# 🧩 Shared State

The agent maintains a shared state across all nodes.

Example:

```python
state = {
    "topic": "Why Python is Best for AI",
    "search_summary": "",
    "current_prompt": "",
    "image_path": "",
    "rating": 0,
    "critique": "",
    "iteration": 0,
    "target_rating": 8,
    "max_iterations": 3,
    "history": []
}
```

---

# 📄 Outputs

The system generates:

## 🖼️ final.png

The best-rated thumbnail image.

## 📄 report.md

Contains:

* iteration history
* prompts
* ratings
* critiques
* improvement progression

---

# 🛠️ Installation

## 1. Clone Repository

```bash
git clone https://github.com/arkmr33/youtube_thumbnail_agent
cd project
```

---

## 2. Install Dependencies

```bash
pip install -r requirements.txt
```

---

# 🔑 Environment Variables

Create a `.env` file:

```env
GROQ_API_KEY=your_key
NVIDIA_API_KEY=your_key
TAVILY_API_KEY=your_key
```
---
# References

https://console.groq.com/docs/models

https://build.nvidia.com/black-forest-labs/flux_2-klein-4b?snippet_tab=Python


---

# ▶️ Run Project

```bash
python agent.main.py "topic to search" 

eg. python agent.main.py "applications of deep learning"  

or python -m main.py "Why Python is the best language" --stream # show every node update live
```

---

# 💡 AI Concepts Demonstrated

This project demonstrates:

* AI Agents
* Reflexion Architecture
* Multimodal AI Systems
* Vision-Language Feedback Loops
* Iterative Prompt Optimization
* Autonomous Improvement Systems
* LangGraph Workflows

---


# 📌 Conclusion

This project showcases how modern AI systems can iteratively improve creative tasks using reflection and multimodal feedback.

By combining:

* LLM reasoning
* image generation
* visual critique
* iterative refinement

the agent autonomously evolves thumbnail quality across multiple iterations using LangGraph-based orchestration.


---