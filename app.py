import re
import time
import streamlit as st

from agents import build_search_agent, build_reader_agent, writer_chain, critic_chain

# ---------------------------------------------------------------- page setup
st.set_page_config(
    page_title="Nova Research | Multi-Agent Research Studio",
    page_icon="🔭",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------------------------------------------------------- styling
st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;600;700&family=Plus+Jakarta+Sans:wght@400;500;600&display=swap');

:root{
  --bg:#0b1020; --panel:#131a33; --panel2:#1a2347; --line:#2a3566;
  --text:#e9ecff; --muted:#9aa4d6;
  --violet:#7c5cff; --cyan:#22d3ee; --pink:#ff5c93; --amber:#ffb547; --green:#2ee6a6;
}
html, body, [class*="css"], .stApp { font-family:'Plus Jakarta Sans',sans-serif; color:var(--text); }
.stApp{
  background:
    radial-gradient(900px 500px at 8% -10%, rgba(124,92,255,.30), transparent 60%),
    radial-gradient(800px 500px at 100% 0%, rgba(34,211,238,.18), transparent 55%),
    radial-gradient(700px 500px at 50% 110%, rgba(255,92,147,.14), transparent 60%),
    var(--bg);
}
#MainMenu, footer, header[data-testid="stHeader"]{ visibility:hidden; height:0; }
.block-container{ padding-top:2rem; max-width:1200px; }
h1,h2,h3,h4{ font-family:'Space Grotesk',sans-serif !important; letter-spacing:-.02em; }

/* sidebar */
section[data-testid="stSidebar"]{ background:var(--panel); border-right:1px solid var(--line); }
section[data-testid="stSidebar"] *{ color:var(--text); }

/* hero */
.hero{ padding:2.2rem 2.4rem; border-radius:24px; border:1px solid var(--line);
  background:linear-gradient(135deg, rgba(124,92,255,.22), rgba(34,211,238,.10) 55%, rgba(255,92,147,.14));
  margin-bottom:1.4rem; }
.hero h1{ font-size:2.8rem; margin:0 0 .4rem 0; line-height:1.1;
  background:linear-gradient(90deg,#fff,#b9a8ff 45%,#6ee7f9); -webkit-background-clip:text; background-clip:text; color:transparent; }
.hero p{ color:var(--muted); font-size:1.05rem; max-width:62ch; margin:0; }
.chips{ margin-top:1rem; display:flex; gap:.5rem; flex-wrap:wrap; }
.chip{ font-size:.8rem; padding:.3rem .75rem; border-radius:999px; border:1px solid var(--line); background:rgba(255,255,255,.04); color:var(--text); }

/* input + button */
.stTextInput input{ background:var(--panel) !important; border:1px solid var(--line) !important; color:var(--text) !important;
  border-radius:14px !important; padding:.9rem 1rem !important; font-size:1.05rem !important; }
.stTextInput input:focus{ border-color:var(--violet) !important; box-shadow:0 0 0 3px rgba(124,92,255,.35) !important; }
.stButton>button, .stDownloadButton>button{ border:0; border-radius:14px; padding:.8rem 1.4rem; font-weight:600; color:#fff;
  background:linear-gradient(90deg,var(--violet),var(--pink)); transition:transform .15s, box-shadow .15s; }
.stButton>button:hover, .stDownloadButton>button:hover{ transform:translateY(-1px); box-shadow:0 10px 28px rgba(124,92,255,.45); color:#fff; }
.stButton>button:focus-visible{ outline:3px solid var(--cyan); }

/* pipeline steps */
.steps{ display:grid; grid-template-columns:repeat(4,1fr); gap:.9rem; margin:1rem 0 1.4rem; }
@media(max-width:900px){ .steps{ grid-template-columns:1fr 1fr; } }
.step{ background:var(--panel); border:1px solid var(--line); border-radius:18px; padding:1rem 1.1rem; position:relative; overflow:hidden; }
.step::before{ content:""; position:absolute; inset:0 0 auto 0; height:4px; background:var(--c); opacity:.35; }
.step .ico{ font-size:1.4rem; }
.step .t{ font-family:'Space Grotesk'; font-weight:600; margin-top:.3rem; }
.step .d{ color:var(--muted); font-size:.82rem; margin-top:.15rem; }
.step .s{ margin-top:.6rem; font-size:.78rem; font-weight:600; color:var(--muted); }
.step.running{ border-color:var(--c); box-shadow:0 0 0 1px var(--c), 0 0 28px -6px var(--c); }
.step.running::before{ opacity:1; animation:slide 1.2s linear infinite; background:linear-gradient(90deg,transparent,var(--c),transparent); background-size:200% 100%; }
.step.running .s{ color:var(--c); }
.step.done::before{ opacity:1; } .step.done .s{ color:var(--green); }
.step.error{ border-color:#ff5c5c; } .step.error .s{ color:#ff7b7b; }
@keyframes slide{ from{background-position:200% 0} to{background-position:-200% 0} }
@media(prefers-reduced-motion:reduce){ .step.running::before{ animation:none; } }

/* cards */
.card{ background:var(--panel); border:1px solid var(--line); border-radius:20px; padding:1.4rem 1.6rem; }
.report{ background:var(--panel); border:1px solid var(--line); border-radius:20px; padding:1.6rem 2rem; line-height:1.75; }
.report h2{ color:#c9bcff; margin-top:1.4rem; }
.report a{ color:var(--cyan); }

/* score ring */
.ring{ --p:0; width:150px; height:150px; border-radius:50%; margin:auto; display:grid; place-items:center;
  background:conic-gradient(var(--rc) calc(var(--p)*1%), rgba(255,255,255,.08) 0); }
.ring div{ width:116px; height:116px; border-radius:50%; background:var(--panel); display:grid; place-items:center;
  font-family:'Space Grotesk'; font-size:2.1rem; font-weight:700; }
.ring small{ font-size:.9rem; color:var(--muted); font-weight:500; }

/* sources */
.src{ display:flex; gap:.8rem; align-items:center; padding:.8rem 1rem; border:1px solid var(--line); border-radius:14px; margin-bottom:.6rem; background:var(--panel2); }
.src .n{ background:linear-gradient(135deg,var(--violet),var(--cyan)); color:#fff; width:28px; height:28px; border-radius:8px; display:grid; place-items:center; font-weight:700; font-size:.8rem; flex:none; }
.src a{ color:var(--text); text-decoration:none; word-break:break-all; font-size:.9rem; }
.src a:hover{ color:var(--cyan); }

/* tabs & metrics */
.stTabs [data-baseweb="tab-list"]{ gap:.4rem; }
.stTabs [data-baseweb="tab"]{ background:var(--panel); border-radius:12px; padding:.5rem 1.1rem; border:1px solid var(--line); }
.stTabs [aria-selected="true"]{ background:linear-gradient(90deg,var(--violet),var(--cyan)) !important; color:#fff !important; }
.stTabs [data-baseweb="tab-highlight"], .stTabs [data-baseweb="tab-border"]{ display:none; }
div[data-testid="stMetric"]{ background:var(--panel); border:1px solid var(--line); border-radius:16px; padding:.9rem 1.1rem; }
</style>
""",
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------- constants
STEPS = [
    ("🔎", "Search Agent", "Finds recent, reliable sources", "#22d3ee"),
    ("📖", "Reader Agent", "Scrapes the best source in depth", "#7c5cff"),
    ("✍️", "Writer", "Drafts the structured report", "#ffb547"),
    ("🧐", "Critic", "Scores and reviews the draft", "#ff5c93"),
]
EXAMPLES = [
    "Impact of AI on healthcare in 2026",
    "Future of solid-state batteries",
    "Pakistan's IT export growth",
    "Quantum computing breakthroughs",
]
LABELS = {"pending": "Waiting", "running": "Working...", "done": "Complete", "error": "Failed"}


# ---------------------------------------------------------------- helpers
def render_steps(slot, states, timings):
    html = '<div class="steps">'
    for (ico, title, desc, color), state, t in zip(STEPS, states, timings):
        label = LABELS[state] + (f" · {t:.1f}s" if state == "done" and t else "")
        html += (
            f'<div class="step {state}" style="--c:{color}">'
            f'<div class="ico">{ico}</div><div class="t">{title}</div>'
            f'<div class="d">{desc}</div><div class="s">{label}</div></div>'
        )
    slot.markdown(html + "</div>", unsafe_allow_html=True)


def run_pipeline(topic, slot):
    states, timings, out = ["pending"] * 4, [0.0] * 4, {}

    def step(i, fn):
        states[i] = "running"
        render_steps(slot, states, timings)
        start = time.time()
        try:
            result = fn()
        except Exception as e:
            states[i] = "error"
            render_steps(slot, states, timings)
            raise RuntimeError(f"{STEPS[i][1]} failed: {e}") from e
        timings[i] = time.time() - start
        states[i] = "done"
        render_steps(slot, states, timings)
        return result

    render_steps(slot, states, timings)

    out["search"] = step(
        0,
        lambda: build_search_agent()
        .invoke({"messages": [("user", f"Find recent, reliable and detailed information about: {topic}")]})["messages"][-1]
        .content,
    )
    out["scraped"] = step(
        1,
        lambda: build_reader_agent()
        .invoke(
            {
                "messages": [
                    (
                        "user",
                        f"Based on the following search results about '{topic}', pick the most relevant URL "
                        f"and scrape it for deeper content.\n\nSearch Results:\n{out['search'][:800]}",
                    )
                ]
            }
        )["messages"][-1]
        .content,
    )
    research = f"SEARCH RESULTS:\n{out['search']}\n\nDETAILED SCRAPED CONTENT:\n{out['scraped']}"
    out["report"] = step(2, lambda: writer_chain.invoke({"topic": topic, "research": research}))
    out["feedback"] = step(3, lambda: critic_chain.invoke({"report": out["report"]}))
    out["timings"] = timings
    out["topic"] = topic
    return out


def as_text(x):
    """Gemini sometimes returns a list of content blocks instead of a string."""
    if isinstance(x, list):
        return "\n".join(b.get("text", "") if isinstance(b, dict) else str(b) for b in x)
    return str(x)


def get_score(feedback):
    m = re.search(r"Score:\s*(\d+(?:\.\d+)?)\s*/\s*10", feedback)
    return float(m.group(1)) if m else None


def get_urls(*texts):
    seen, urls = set(), []
    for t in texts:
        for u in re.findall(r"https?://[^\s)\]>\"']+", t):
            u = u.rstrip(".,;")
            if u not in seen:
                seen.add(u)
                urls.append(u)
    return urls


def score_color(s):
    return "#2ee6a6" if s >= 8 else "#ffb547" if s >= 6 else "#ff5c5c"


# ---------------------------------------------------------------- sidebar
with st.sidebar:
    st.markdown("### 🔭 Nova Research")
    st.caption("Four specialised agents, one polished report.")
    st.markdown("**Try a topic**")
    for ex in EXAMPLES:
        if st.button(ex, key=f"ex_{ex}", use_container_width=True):
            st.session_state["topic_input"] = ex
    st.divider()
    if st.session_state.get("result"):
        if st.button("Clear results", use_container_width=True):
            st.session_state.pop("result", None)
            st.rerun()
    st.caption("Search: Tavily · Model: Gemini · Framework: LangChain")

# ---------------------------------------------------------------- hero
st.markdown(
    """
<div class="hero">
  <h1>Research anything. Get a reviewed report.</h1>
  <p>Enter a topic and four agents search the web, read the best source, write a structured report, and score it.</p>
  <div class="chips"><span class="chip">Live web search</span><span class="chip">Deep page reading</span>
  <span class="chip">Structured report</span><span class="chip">Critic score</span></div>
</div>
""",
    unsafe_allow_html=True,
)

c1, c2 = st.columns([5, 1.2], vertical_alignment="bottom")
topic = c1.text_input(
    "Research topic",
    key="topic_input",
    placeholder="e.g. Impact of AI on healthcare in 2026",
    label_visibility="collapsed",
)
go = c2.button("Start research", use_container_width=True, type="primary")

steps_slot = st.empty()

# ---------------------------------------------------------------- run
if go:
    if not topic.strip():
        st.warning("Enter a research topic to begin.")
    else:
        st.session_state.pop("result", None)
        try:
            res = run_pipeline(topic.strip(), steps_slot)
            for k in ("search", "scraped", "report", "feedback"):
                res[k] = as_text(res[k])
            st.session_state["result"] = res
        except Exception as e:
            st.error(f"{e}\n\nCheck your API keys in `.env` and try again.")

# ---------------------------------------------------------------- results
res = st.session_state.get("result")
if res:
    render_steps(steps_slot, ["done"] * 4, res["timings"])
    score = get_score(res["feedback"])
    urls = get_urls(res["report"], res["search"])

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Critic score", f"{score:g}/10" if score is not None else "n/a")
    m2.metric("Sources found", len(urls))
    m3.metric("Report words", f"{len(res['report'].split()):,}")
    m4.metric("Total time", f"{sum(res['timings']):.0f}s")
    st.write("")

    tab_report, tab_review, tab_sources, tab_raw = st.tabs(["📄 Report", "🧐 Critic review", "🔗 Sources", "🧪 Raw agent output"])

    with tab_report:
        st.markdown('<div class="report">', unsafe_allow_html=True)
        st.markdown(res["report"])
        st.markdown("</div>", unsafe_allow_html=True)
        st.write("")
        st.download_button(
            "Download report (.md)",
            data=f"# {res['topic']}\n\n{res['report']}\n\n---\n## Critic review\n\n{res['feedback']}",
            file_name="research_report.md",
            mime="text/markdown",
        )

    with tab_review:
        a, b = st.columns([1, 2.4])
        with a:
            if score is not None:
                st.markdown(
                    f'<div class="card"><div class="ring" style="--p:{score*10};--rc:{score_color(score)}">'
                    f"<div>{score:g}<small>/10</small></div></div></div>",
                    unsafe_allow_html=True,
                )
        with b:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown(res["feedback"])
            st.markdown("</div>", unsafe_allow_html=True)

    with tab_sources:
        if urls:
            for i, u in enumerate(urls, 1):
                st.markdown(
                    f'<div class="src"><div class="n">{i}</div><a href="{u}" target="_blank" rel="noopener">{u}</a></div>',
                    unsafe_allow_html=True,
                )
        else:
            st.info("No URLs were found in the research output.")

    with tab_raw:
        with st.expander("Search agent output"):
            st.text(res["search"])
        with st.expander("Reader agent output (scraped content)"):
            st.text(res["scraped"])
elif not go:
    st.markdown(
        '<div class="card" style="text-align:center;color:var(--muted)">Your report will appear here. '
        "Pick an example in the sidebar or type your own topic.</div>",
        unsafe_allow_html=True,
    )

    