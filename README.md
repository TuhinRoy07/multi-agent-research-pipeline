# 🗞️ The Dispatch — Multi-Agent Research System

An autonomous multi-agent research pipeline that turns a single topic into a fact-checked, structured report — powered by **LangChain**, **Groq's Llama 3.3 70B**, **Tavily Search**, and a custom **Streamlit** newsroom-themed UI.

Four specialized agents work in sequence, like a real editorial desk: one searches, one reads deeper, one writes, and one critiques — all visualized live as dispatches moving through a wire room.

---

## ✨ Features

- **🔎 Search Agent (The Correspondent)** — Queries the web via Tavily to gather recent, relevant sources on any topic
- **📖 Reader Agent (The Archivist)** — Scrapes and extracts clean content from the most relevant source for deeper context
- **✍️ Writer Chain (Staff Writer)** — Synthesizes research into a structured report (Introduction, Key Findings, Conclusion, Sources)
- **🧐 Critic Chain (Chief Editor)** — Independently reviews the report, scores it out of 10, and provides structured feedback
- **🖥️ Live Streamlit dashboard** — Newsroom/wire-desk themed UI showing real-time agent status, a scrolling wire ticker, and a stamped "Approved for Print" seal on completion
- **📥 Export** — Download the final report as a Markdown file

---

## 🏗️ Architecture

```
Topic Input
     │
     ▼
┌─────────────────────┐
│  Search Agent        │  → Tavily web search
│  (Correspondent)     │
└──────────┬───────────┘
           ▼
┌─────────────────────┐
│  Reader Agent         │  → BeautifulSoup scraping
│  (Archivist)          │
└──────────┬───────────┘
           ▼
┌─────────────────────┐
│  Writer Chain         │  → Drafts structured report
│  (Staff Writer)       │
└──────────┬───────────┘
           ▼
┌─────────────────────┐
│  Critic Chain         │  → Reviews & scores report
│  (Chief Editor)       │
└──────────┬───────────┘
           ▼
     Final Report + Feedback
```

Each agent is built with LangChain's `create_agent`, running on Groq's `llama-3.3-70b-versatile` model for fast inference.

---

## 🛠️ Tech Stack

| Layer         | Tool/Library                              |
|---------------|--------------------------------------------|
| LLM           | Groq — Llama 3.3 70B Versatile              |
| Agent framework | LangChain (`create_agent`)                |
| Web search    | Tavily API                                  |
| Web scraping  | BeautifulSoup4 + Requests                   |
| Frontend      | Streamlit (custom CSS UI)                   |
| Env config    | python-dotenv                               |

---

## 📂 Project Structure

```
Multi-Agent-System/
├── app.py              # Streamlit UI — "The Dispatch"
├── agents.py            # Agent & chain definitions (search, reader, writer, critic)
├── pipeline.py           # CLI pipeline runner (non-UI version)
├── tools.py              # Custom tools: web_search, scrape_url
├── requirements.txt       # Python dependencies
├── .env                  # API keys (not committed)
└── README.md
```

---

## ⚙️ Setup & Installation

### 1. Clone the repository
```bash
git clone https://github.com/<your-username>/Multi-Agent-System.git
cd Multi-Agent-System
```

### 2. Create and activate a virtual environment
```bash
# Create
python -m venv .venv

# Activate — Windows
.venv\Scripts\activate

# Activate — macOS/Linux
source .venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Set up API keys
Create a `.env` file in the project root:
```env
GROQ_API_KEY=your_groq_api_key_here
TAVILY_API_KEY=your_tavily_api_key_here
```
- Get a free Groq API key at [console.groq.com](https://console.groq.com)
- Get a free Tavily API key at [tavily.com](https://tavily.com)

### 5. Run the app

**Streamlit UI:**
```bash
streamlit run app.py
```

**CLI version:**
```bash
python pipeline.py
```

---

## 🖥️ Usage

1. Launch the app with `streamlit run app.py`
2. Enter a research topic in the **Dateline / Topic** field
3. Click **Send to the Wire**
4. Watch the four desks work through the pipeline live
5. Read the final report and editor's feedback, or download the report as Markdown

---

## ⚠️ Notes & Limitations

- Groq's free tier has rate limits (requests/tokens per minute) — heavy or repeated use may briefly slow down responses
- Web scraping depends on target site structure and may not always return clean content
- This is a research/learning project and not intended for production use without further hardening (input validation, error recovery, etc.)

---

## 📌 Roadmap Ideas

- [ ] Add retry/backoff logic for network and rate-limit resilience
- [ ] Support multiple source scraping instead of a single URL
- [ ] Add report history / session persistence
- [ ] Export to PDF in addition to Markdown

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

---

## 🙋 Author

Built by **Hey** — BCA student, JIS University · Data Analytics & AI enthusiast
