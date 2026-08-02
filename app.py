import streamlit as st
import time
from agents import build_reader_agent, build_search_agent, writer_chain, critic_chain

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="The Dispatch · Multi-Agent Research Wire",
    page_icon="🗞️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,500;9..144,600;9..144,700&family=Fraunces:ital,opsz,wght@1,9..144,500&family=Source+Sans+3:ital,wght@0,400;0,500;0,600;1,400&family=JetBrains+Mono:wght@400;500;600;700&display=swap');

:root {
    --ink: #12141b;
    --ink-2: #1a1d27;
    --ink-3: #21252f;
    --brass: #c9a24b;
    --brass-dim: rgba(201,162,75,0.13);
    --rust: #b8452f;
    --rust-dim: rgba(184,69,47,0.13);
    --sage: #7d9a6b;
    --sage-dim: rgba(125,154,107,0.13);
    --text: #e9e6da;
    --text-muted: #9b9a8c;
    --text-faint: #5c5d59;
    --border: rgba(233,230,218,0.12);
}

html, body, [class*="css"] {
    font-family: 'Source Sans 3', sans-serif;
    color: var(--text);
}

.stApp {
    background: var(--ink);
    background-image:
        radial-gradient(ellipse 60% 40% at 10% 0%, rgba(201,162,75,0.07) 0%, transparent 60%),
        radial-gradient(ellipse 50% 35% at 90% 100%, rgba(184,69,47,0.06) 0%, transparent 55%);
}

#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 0 3rem 4rem; max-width: 1240px; }

/* ── Masthead ── */
.masthead { text-align: center; padding: 2.4rem 0 1.4rem; border-bottom: 3px double var(--border); }
.masthead-kicker {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.68rem;
    letter-spacing: 0.32em;
    color: var(--brass);
    text-transform: uppercase;
    margin-bottom: 0.7rem;
}
.masthead h1 {
    font-family: 'Fraunces', serif;
    font-weight: 600;
    font-size: clamp(2.8rem, 6vw, 4.8rem);
    letter-spacing: -0.01em;
    margin: 0;
    color: var(--text);
    line-height: 1;
}
.masthead-sub {
    font-family: 'Fraunces', serif;
    font-style: italic;
    font-weight: 500;
    color: var(--text-muted);
    font-size: 1rem;
    margin-top: 0.7rem;
}
.masthead-meta {
    display: flex;
    justify-content: center;
    gap: 1.6rem;
    margin-top: 1.1rem;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.64rem;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: var(--text-faint);
}
.masthead-meta span.dot { color: var(--brass); }

/* ── Wire ticker ── */
.wire-ticker-wrap {
    overflow: hidden;
    border-bottom: 1px solid var(--border);
    padding: 0.6rem 0;
    margin-bottom: 2.2rem;
    background: rgba(201,162,75,0.03);
}
.wire-ticker {
    display: flex;
    width: max-content;
    gap: 2.6rem;
    animation: tickerScroll 32s linear infinite;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.72rem;
    letter-spacing: 0.06em;
    color: var(--text-muted);
    white-space: nowrap;
}
.wire-ticker .sep { color: var(--brass); }
.wire-ticker .live-dot { color: var(--rust); }
@keyframes tickerScroll { 0% { transform: translateX(0); } 100% { transform: translateX(-50%); } }

.divider {
    height: 1px;
    background: repeating-linear-gradient(90deg, var(--border) 0 6px, transparent 6px 12px);
    margin: 2rem 0 1.6rem;
}

/* ── Telegram / filing card ── */
.telegram-card {
    position: relative;
    background: var(--ink-2);
    border: 1px solid var(--border);
    border-radius: 2px;
    padding: 1.9rem 2.1rem 2.1rem;
    margin-bottom: 1.3rem;
}
.telegram-card::before {
    content: '';
    position: absolute; top: 0; left: 0; right: 0; height: 1px;
    background-image: linear-gradient(90deg, var(--brass) 50%, transparent 0);
    background-size: 9px 1px;
    background-repeat: repeat-x;
    opacity: 0.5;
}
.telegram-label {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.66rem;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: var(--brass);
    margin-bottom: 1rem;
}

.stTextInput > div > div > input {
    background: var(--ink-3) !important;
    border: 1px solid var(--border) !important;
    border-radius: 2px !important;
    color: var(--text) !important;
    font-family: 'Source Sans 3', sans-serif !important;
    font-size: 0.95rem !important;
    padding: 0.75rem 0.95rem !important;
    transition: border-color 0.2s, box-shadow 0.2s !important;
}
.stTextInput > div > div > input:focus {
    border-color: var(--brass) !important;
    box-shadow: 0 0 0 3px var(--brass-dim) !important;
    outline: none !important;
}
.stTextInput > label {
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.68rem !important;
    letter-spacing: 0.16em !important;
    text-transform: uppercase !important;
    color: var(--text-muted) !important;
    font-weight: 500 !important;
}

.stButton > button {
    background: var(--brass) !important;
    color: #14161c !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-weight: 700 !important;
    font-size: 0.82rem !important;
    letter-spacing: 0.12em !important;
    text-transform: uppercase;
    border: none !important;
    border-radius: 2px !important;
    padding: 0.8rem 2rem !important;
    cursor: pointer !important;
    transition: transform 0.12s, background 0.12s !important;
    width: 100%;
}
.stButton > button:hover { background: #ddb964 !important; transform: translateY(-1px) !important; }
.stButton > button:active { transform: translateY(0) !important; }
.stButton > button:focus-visible { outline: 2px solid var(--sage) !important; outline-offset: 2px !important; }

/* ── Filing stub chips ── */
.chip {
    display: inline-block;
    background: transparent;
    border: 1px dashed var(--border);
    border-radius: 2px;
    padding: 0.3rem 0.75rem;
    font-size: 0.74rem;
    color: var(--text-muted);
    font-family: 'JetBrains Mono', monospace;
}

/* ── Dispatch (pipeline step) cards ── */
.dispatch-card {
    display: flex;
    gap: 1.1rem;
    background: var(--ink-2);
    border: 1px solid var(--border);
    border-left: 3px solid var(--border);
    border-radius: 2px;
    padding: 1.15rem 1.4rem;
    margin-bottom: 0.85rem;
    transition: border-color 0.3s, background 0.3s;
}
.dispatch-card.active { border-left-color: var(--brass); background: var(--brass-dim); }
.dispatch-card.done { border-left-color: var(--sage); background: var(--sage-dim); }

.dispatch-role-col { display: flex; flex-direction: column; align-items: center; padding-top: 0.1rem; min-width: 2.2rem; }
.dispatch-numeral { font-family: 'Fraunces', serif; font-weight: 600; font-size: 1.3rem; color: var(--text-faint); }
.dispatch-card.active .dispatch-numeral { color: var(--brass); }
.dispatch-card.done .dispatch-numeral { color: var(--sage); }

.dispatch-body { flex: 1; min-width: 0; }
.dispatch-header { display: flex; align-items: baseline; gap: 0.7rem; margin-bottom: 0.25rem; flex-wrap: wrap; }
.dispatch-title { font-family: 'Fraunces', serif; font-weight: 600; font-size: 1.02rem; color: var(--text); }
.dispatch-desc { font-size: 0.82rem; color: var(--text-muted); margin-bottom: 0.6rem; font-style: italic; }

.stamp {
    margin-left: auto;
    display: inline-block;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.6rem;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    padding: 0.18rem 0.6rem;
    border-radius: 2px;
    transform: rotate(-3deg);
    white-space: nowrap;
}
.stamp.pending { color: var(--text-faint); border: 1.5px dashed var(--text-faint); }
.stamp.running { color: var(--brass); border: 1.5px solid var(--brass); animation: stampPulse 1.3s ease-in-out infinite; }
.stamp.done { color: var(--sage); border: 1.5px solid var(--sage); }

.wire-meter { height: 3px; border-radius: 2px; background: rgba(255,255,255,0.05); overflow: hidden; }
.wire-meter-fill { height: 100%; width: 0%; background: var(--text-faint); transition: width 0.4s ease; }
.wire-meter-fill.running { width: 60%; background: var(--brass); animation: scan 1.3s ease-in-out infinite; }
.wire-meter-fill.done { width: 100%; background: var(--sage); }

@keyframes stampPulse { 0%,100% { opacity: 1; } 50% { opacity: 0.45; } }
@keyframes scan { 0% { transform: translateX(-40%); } 100% { transform: translateX(180%); } }
@media (prefers-reduced-motion: reduce) {
    .stamp.running, .wire-meter-fill.running, .wire-ticker, .approved-stamp { animation: none !important; }
}

/* ── Result panels ── */
.clipping-panel {
    background: var(--ink-2);
    border: 1px solid var(--border);
    border-radius: 2px;
    padding: 1.5rem 1.7rem;
    margin-top: 0.6rem;
    margin-bottom: 1.2rem;
}
.clipping-title {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.66rem;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: var(--brass);
    margin-bottom: 0.9rem;
    padding-bottom: 0.6rem;
    border-bottom: 1px solid var(--border);
}
.clipping-content {
    font-size: 0.87rem;
    line-height: 1.75;
    color: var(--text-muted);
    white-space: pre-wrap;
    font-family: 'JetBrains Mono', monospace;
}

.report-panel {
    position: relative;
    background: var(--ink-2);
    border: 1px solid rgba(201,162,75,0.28);
    border-radius: 3px;
    padding: 2.1rem 2.4rem;
    margin-top: 0.8rem;
}
.report-panel :is(h1,h2,h3) { font-family: 'Fraunces', serif; }

.feedback-panel {
    background: var(--ink-2);
    border: 1px solid rgba(125,154,107,0.3);
    border-radius: 3px;
    padding: 2.1rem 2.4rem;
    margin-top: 0.8rem;
    border-left: 3px solid var(--rust);
}

.approved-stamp {
    position: absolute;
    top: 1.3rem; right: 1.7rem;
    font-family: 'JetBrains Mono', monospace;
    font-weight: 700;
    font-size: 0.85rem;
    letter-spacing: 0.1em;
    color: var(--rust);
    border: 3px double var(--rust);
    padding: 0.5rem 0.9rem;
    border-radius: 3px;
    transform: rotate(-7deg);
    text-transform: uppercase;
    animation: stampIn 0.45s ease-out;
    pointer-events: none;
}
@keyframes stampIn {
    0% { opacity: 0; transform: rotate(-16deg) scale(1.5); }
    60% { opacity: 1; transform: rotate(-7deg) scale(0.94); }
    100% { transform: rotate(-7deg) scale(1); }
}

.panel-label {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.7rem;
    letter-spacing: 0.16em;
    text-transform: uppercase;
    margin-bottom: 1.1rem;
    padding-bottom: 0.6rem;
    border-bottom: 1px solid var(--border);
}
.panel-label.brass { color: var(--brass); }
.panel-label.rust { color: var(--rust); }

details summary {
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.74rem !important;
    color: var(--text-muted) !important;
    letter-spacing: 0.06em !important;
}

.section-heading {
    font-family: 'Fraunces', serif;
    font-weight: 600;
    font-style: italic;
    font-size: 1.3rem;
    color: var(--text);
    margin: 1.7rem 0 1rem;
}

.notice {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.66rem;
    color: var(--text-faint);
    text-align: center;
    margin-top: 3rem;
    letter-spacing: 0.06em;
    text-transform: uppercase;
}
</style>
""", unsafe_allow_html=True)


# ── Helper: render a dispatch card into a placeholder (so it can be updated live) ─
def dispatch_card_html(numeral: str, role: str, title: str, state: str, desc: str = "") -> str:
    status_map = {
        "waiting": ("PENDING", "pending"),
        "running": ("ON THE WIRE", "running"),
        "done":    ("FILED",   "done"),
    }
    label, cls = status_map.get(state, ("", ""))
    card_cls = {"running": "active", "done": "done"}.get(state, "")
    meter_cls = {"running": "running", "done": "done"}.get(state, "")
    return f"""
    <div class="dispatch-card {card_cls}">
        <div class="dispatch-role-col"><span class="dispatch-numeral">{numeral}</span></div>
        <div class="dispatch-body">
            <div class="dispatch-header">
                <span class="dispatch-title">{role} &mdash; {title}</span>
                <span class="stamp {cls}">{label}</span>
            </div>
            <div class="dispatch-desc">{desc}</div>
            <div class="wire-meter"><div class="wire-meter-fill {meter_cls}"></div></div>
        </div>
    </div>
    """

def render_dispatch(placeholder, numeral: str, role: str, title: str, state: str, desc: str = ""):
    placeholder.markdown(dispatch_card_html(numeral, role, title, state, desc), unsafe_allow_html=True)


# ── Session state init ────────────────────────────────────────────────────────
for key in ("results", "running", "done"):
    if key not in st.session_state:
        st.session_state[key] = {} if key == "results" else False


# ── Masthead ──────────────────────────────────────────────────────────────────
if st.session_state.running:
    _status = "PRESSES RUNNING"
elif st.session_state.done:
    _status = "EDITION CLOSED"
else:
    _status = "AWAITING COPY"

st.markdown(f"""
<div class="masthead">
    <div class="masthead-kicker">Multi-Agent Research Wire Service</div>
    <h1>The Dispatch</h1>
    <div class="masthead-sub">Four desks, one byline &mdash; from raw wire to printed report</div>
    <div class="masthead-meta">
        <span><span class="dot">&#9679;</span> STATUS: {_status}</span>
        <span><span class="dot">&#9679;</span> DESKS: 4</span>
        <span><span class="dot">&#9679;</span> RUNTIME: LANGCHAIN / GROQ</span>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="wire-ticker-wrap">
    <div class="wire-ticker">
        <span><span class="live-dot">&#9679;</span> CORRESPONDENT DESK ONLINE</span>
        <span class="sep">//</span>
        <span>ARCHIVIST STANDING BY</span>
        <span class="sep">//</span>
        <span>STAFF WRITER AT THE DESK</span>
        <span class="sep">//</span>
        <span>CHIEF EDITOR REVIEWING COPY</span>
        <span class="sep">//</span>
        <span>WIRE FEED: STABLE</span>
        <span class="sep">//</span>
        <span><span class="live-dot">&#9679;</span> CORRESPONDENT DESK ONLINE</span>
        <span class="sep">//</span>
        <span>ARCHIVIST STANDING BY</span>
        <span class="sep">//</span>
        <span>STAFF WRITER AT THE DESK</span>
        <span class="sep">//</span>
        <span>CHIEF EDITOR REVIEWING COPY</span>
        <span class="sep">//</span>
        <span>WIRE FEED: STABLE</span>
    </div>
</div>
""", unsafe_allow_html=True)


# ── Layout: filing card left, wire room right ────────────────────────────────
col_input, col_spacer, col_pipeline = st.columns([5, 0.5, 4])

with col_input:
    st.markdown('<div class="telegram-card">', unsafe_allow_html=True)
    st.markdown('<div class="telegram-label">File a Request</div>', unsafe_allow_html=True)
    topic = st.text_input(
        "Dateline / Topic",
        placeholder="e.g. Quantum computing breakthroughs in 2025",
        key="topic_input",
        label_visibility="visible",
    )
    run_btn = st.button("📨  Send to the Wire", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("""
    <div style="display:flex;gap:0.5rem;flex-wrap:wrap;margin-bottom:1.5rem;align-items:center;">
        <span style="font-family:'JetBrains Mono',monospace;font-size:0.66rem;color:var(--text-faint);letter-spacing:0.1em;">PAST FILINGS &rarr;</span>
    """, unsafe_allow_html=True)
    examples = ["LLM agents 2025", "CRISPR gene editing", "Fusion energy progress"]
    for ex in examples:
        st.markdown(f'<span class="chip">{ex}</span>', unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

with col_pipeline:
    st.markdown('<div class="section-heading">The Wire Room</div>', unsafe_allow_html=True)

    r = st.session_state.results

    def s(step):
        if not r:
            return "waiting"
        steps = ["search", "reader", "writer", "critic"]
        if step in r:
            return "done"
        if st.session_state.running:
            for k in steps:
                if k not in r:
                    return "running" if k == step else "waiting"
        return "waiting"

    step_defs = [
        ("search", "I",   "The Correspondent", "Search Desk",  "Wires in fresh reports from across the web"),
        ("reader", "II",  "The Archivist",      "Reading Room", "Pulls the full story from the primary source"),
        ("writer", "III", "Staff Writer",       "Copy Desk",    "Drafts the dispatch, ready for print"),
        ("critic", "IV",  "Chief Editor",       "Editor's Desk","Marks up the copy before it runs"),
    ]

    step_placeholders = {}
    for key, numeral, role, title, desc in step_defs:
        ph = st.empty()
        step_placeholders[key] = ph
        render_dispatch(ph, numeral, role, title, s(key), desc)


# ── Run pipeline ──────────────────────────────────────────────────────────────
if run_btn:
    if not topic.strip():
        st.warning("File a topic before sending it to the wire.")
    else:
        st.session_state.results = {}
        st.session_state.running = True
        st.session_state.done = False
        st.rerun()

if st.session_state.running and not st.session_state.done:
    results = {}
    topic_val = st.session_state.topic_input

    step_labels = {
        "search": ("I",   "The Correspondent", "Search Desk",   "Wires in fresh reports from across the web"),
        "reader": ("II",  "The Archivist",      "Reading Room",  "Pulls the full story from the primary source"),
        "writer": ("III", "Staff Writer",       "Copy Desk",     "Drafts the dispatch, ready for print"),
        "critic": ("IV",  "Chief Editor",       "Editor's Desk", "Marks up the copy before it runs"),
    }

    def mark(step, state):
        if step in step_placeholders:
            numeral, role, title, desc = step_labels[step]
            render_dispatch(step_placeholders[step], numeral, role, title, state, desc)

    try:
        # ── Step 1: Correspondent (search) ──
        mark("search", "running")
        with st.spinner("📡  The Correspondent is wiring in reports…"):
            search_agent = build_search_agent()
            sr = search_agent.invoke({
                "messages": [("user", f"Find recent, reliable and detailed information about: {topic_val}")]
            })
            results["search"] = sr["messages"][-1].content
            st.session_state.results = dict(results)
        mark("search", "done")

        # ── Step 2: Archivist (reader) ──
        mark("reader", "running")
        with st.spinner("🗂️  The Archivist is pulling the full story…"):
            reader_agent = build_reader_agent()
            rr = reader_agent.invoke({
                "messages": [("user",
                    f"Based on the following search results about '{topic_val}', "
                    f"pick the most relevant URL and scrape it for deeper content.\n\n"
                    f"Search Results:\n{results['search'][:800]}"
                )]
            })
            results["reader"] = rr["messages"][-1].content
            st.session_state.results = dict(results)
        mark("reader", "done")

        # ── Step 3: Staff Writer (writer) ──
        mark("writer", "running")
        with st.spinner("🖋️  Staff Writer is drafting the dispatch…"):
            research_combined = (
                f"SEARCH RESULTS:\n{results['search']}\n\n"
                f"DETAILED SCRAPED CONTENT:\n{results['reader']}"
            )
            results["writer"] = writer_chain.invoke({
                "topic": topic_val,
                "research": research_combined
            })
            st.session_state.results = dict(results)
        mark("writer", "done")

        # ── Step 4: Chief Editor (critic) ──
        mark("critic", "running")
        with st.spinner("🧐  Chief Editor is marking up the copy…"):
            results["critic"] = critic_chain.invoke({
                "report": results["writer"]
            })
            st.session_state.results = dict(results)
        mark("critic", "done")

        st.session_state.running = False
        st.session_state.done = True
        st.rerun()

    except Exception as e:
        st.session_state.running = False
        st.session_state.done = False
        st.session_state.results = dict(results)
        st.error(
            f"⚠️ The wire went down at desk **{len(results) + 1}**: `{type(e).__name__}: {e}`\n\n"
            "Usually a rate limit, missing/invalid API key, or a network issue. "
            "Check your `.env` file and try again."
        )
        st.stop()


# ── Results display ───────────────────────────────────────────────────────────
r = st.session_state.results

if r:
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    st.markdown('<div class="section-heading">On the Record</div>', unsafe_allow_html=True)

    if "search" in r:
        with st.expander("📡 Correspondent's Wire (raw)", expanded=False):
            st.markdown(f'<div class="clipping-panel"><div class="clipping-title">Search Desk Output</div>'
                        f'<div class="clipping-content">{r["search"]}</div></div>', unsafe_allow_html=True)

    if "reader" in r:
        with st.expander("🗂️ Archivist's Findings (raw)", expanded=False):
            st.markdown(f'<div class="clipping-panel"><div class="clipping-title">Reading Room Output</div>'
                        f'<div class="clipping-content">{r["reader"]}</div></div>', unsafe_allow_html=True)

    if "writer" in r:
        stamp_html = '<div class="approved-stamp">Approved for Print</div>' if "critic" in r else ""
        st.markdown(f"""
        <div class="report-panel">
            {stamp_html}
            <div class="panel-label brass">📰 Final Dispatch</div>
        """, unsafe_allow_html=True)
        st.markdown(r["writer"])
        st.markdown("</div>", unsafe_allow_html=True)

        st.download_button(
            label="📨  Send to Print (Download .md)",
            data=r["writer"],
            file_name=f"research_report_{int(time.time())}.md",
            mime="text/markdown",
        )

    if "critic" in r:
        st.markdown("""
        <div class="feedback-panel">
            <div class="panel-label rust">🖊️ Editor's Markup</div>
        """, unsafe_allow_html=True)
        st.markdown(r["critic"])
        st.markdown("</div>", unsafe_allow_html=True)


# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="notice">
    The Dispatch &middot; Multi-Agent Research Wire &middot; LangChain / LangGraph &middot; Streamlit Edition
</div>
""", unsafe_allow_html=True)