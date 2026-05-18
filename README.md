# 🎯 YouTube Thumbnail Designer — Reflexion Agent (LangGraph + Groq)

This project implements an **iterative AI agent using LangGraph** that generates and improves YouTube thumbnails using a reflection loop.

The agent repeatedly generates a thumbnail, critiques it using a vision model, and improves it until it reaches a target quality score.

---

# 🚀 What This Project Does

Given a YouTube video topic, the agent:

1. 🔎 Searches the web for ideas and visual context (Tavily)
2. ✍️ Writes a detailed thumbnail prompt (Groq LLM)
3. 🎨 Generates a thumbnail image (mock or DALL·E integration)
4. 👁️ Critiques the image using a vision LLM (Groq structured output)
5. 🔁 Improves the prompt using feedback
6. 🏁 Stops when:
   - rating ≥ target (default 8), OR
   - max iterations reached (default 3)

Finally it outputs:
- 🖼️ `final.png` (best thumbnail)
- 📄 `report.md` (full iteration history)

---

# 🧠 Architecture (LangGraph Workflow)
