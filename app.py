import streamlit as st
import time
import builtins

from pipeline import run_research_pipeline

# ─────────────────────────────────────────────
#  PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="ResearchMind AI",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─────────────────────────────────────────────
#  GLOBAL CSS + ANIMATIONS
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800;900&family=JetBrains+Mono:ital,wght@0,300;0,400;0,500;1,300&display=swap');

:root {
  --bg:         #050810;
  --surface:    #0c1120;
  --surface2:   #101828;
  --border:     #1a2540;
  --border2:    #243050;
  --accent:     #00f5b4;
  --accent-dim: rgba(0,245,180,.12);
  --accent2:    #4f8dff;
  --accent3:    #b06aff;
  --warn:       #ff5f5f;
  --text:       #e2eaf8;
  --muted:      #4a5878;
  --muted2:     #2e3d5a;
  --radius:     14px;
  --radius-lg:  20px;
}

/* ── Reset & base ── */
*, *::before, *::after { box-sizing: border-box; }

html, body,
[data-testid="stAppViewContainer"],
[data-testid="stApp"] {
  background: var(--bg) !important;
  color: var(--text) !important;
  font-family: 'Outfit', sans-serif !important;
}

[data-testid="stHeader"]           { background: transparent !important; display: none; }
[data-testid="stToolbar"]          { display: none !important; }
[data-testid="stDecoration"]       { display: none !important; }
[data-testid="stSidebar"]          { display: none !important; }
#MainMenu, footer, header          { visibility: hidden !important; }

/* ── Animated mesh background ── */
[data-testid="stAppViewContainer"]::before {
  content: '';
  position: fixed;
  inset: 0;
  background:
    radial-gradient(ellipse 80% 60% at 10% 0%,   rgba(0,245,180,.055) 0%, transparent 60%),
    radial-gradient(ellipse 60% 50% at 90% 5%,   rgba(79,141,255,.06)  0%, transparent 55%),
    radial-gradient(ellipse 50% 40% at 50% 100%,  rgba(176,106,255,.05) 0%, transparent 50%);
  pointer-events: none;
  z-index: 0;
  animation: meshShift 18s ease-in-out infinite alternate;
}
@keyframes meshShift {
  0%   { opacity: .7; transform: scale(1)   translateY(0); }
  100% { opacity: 1;  transform: scale(1.05) translateY(-12px); }
}

/* ── Scrollbar ── */
::-webkit-scrollbar             { width: 5px; height: 5px; }
::-webkit-scrollbar-track       { background: transparent; }
::-webkit-scrollbar-thumb       { background: var(--border2); border-radius: 99px; }
::-webkit-scrollbar-thumb:hover { background: var(--muted); }

/* ── Main content wrapper ── */
.block-container {
  max-width: 1100px !important;
  padding: 0 2rem 4rem !important;
  margin: 0 auto !important;
  position: relative;
  z-index: 1;
}

/* ═══════════════════════════════════════
   NAVBAR
═══════════════════════════════════════ */
.navbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1.4rem 0 1rem;
  border-bottom: 1px solid var(--border);
  margin-bottom: 3rem;
  animation: fadeDown .6s ease both;
}
.nav-logo {
  display: flex;
  align-items: center;
  gap: .6rem;
  font-family: 'Outfit', sans-serif;
  font-weight: 800;
  font-size: 1.15rem;
  letter-spacing: -.02em;
  color: var(--text);
}
.nav-logo-dot {
  width: 10px; height: 10px;
  background: var(--accent);
  border-radius: 50%;
  box-shadow: 0 0 10px var(--accent), 0 0 24px rgba(0,245,180,.4);
  animation: pulse 2.5s ease-in-out infinite;
}
@keyframes pulse {
  0%,100% { box-shadow: 0 0 8px var(--accent), 0 0 20px rgba(0,245,180,.35); }
  50%      { box-shadow: 0 0 16px var(--accent), 0 0 40px rgba(0,245,180,.55); }
}
.nav-pills {
  display: flex;
  gap: .5rem;
  align-items: center;
}
.nav-pill {
  font-size: .68rem;
  letter-spacing: .12em;
  text-transform: uppercase;
  color: var(--muted);
  border: 1px solid var(--border2);
  border-radius: 999px;
  padding: .25rem .8rem;
  font-family: 'JetBrains Mono', monospace;
}
.nav-pill.green {
  color: var(--accent);
  border-color: rgba(0,245,180,.3);
  background: rgba(0,245,180,.06);
}

/* ═══════════════════════════════════════
   HERO
═══════════════════════════════════════ */
.hero {
  text-align: center;
  padding: 1rem 1rem 2.5rem;
  animation: fadeUp .7s .1s ease both;
}
.hero-eyebrow {
  display: inline-flex;
  align-items: center;
  gap: .5rem;
  font-family: 'JetBrains Mono', monospace;
  font-size: .68rem;
  letter-spacing: .15em;
  text-transform: uppercase;
  color: var(--accent);
  margin-bottom: 1.4rem;
}
.hero-eyebrow-line {
  width: 28px; height: 1px;
  background: linear-gradient(90deg, transparent, var(--accent));
}
.hero-eyebrow-line.r { background: linear-gradient(90deg, var(--accent), transparent); }

.hero-title {
  font-family: 'Outfit', sans-serif !important;
  font-size: clamp(2.8rem, 6vw, 5rem) !important;
  font-weight: 900 !important;
  letter-spacing: -.04em !important;
  line-height: 1.0 !important;
  color: var(--text) !important;
  margin: 0 0 1rem !important;
}
.hero-title .grad {
  background: linear-gradient(135deg, var(--accent) 0%, var(--accent2) 50%, var(--accent3) 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}
.hero-sub {
  color: var(--muted);
  font-size: .95rem;
  font-weight: 400;
  max-width: 480px;
  margin: 0 auto;
  line-height: 1.6;
}

/* ═══════════════════════════════════════
   INPUT SECTION
═══════════════════════════════════════ */
.input-wrap {
  max-width: 700px;
  margin: 0 auto 2.5rem;
  animation: fadeUp .7s .2s ease both;
}
.input-label {
  font-size: .72rem;
  letter-spacing: .14em;
  text-transform: uppercase;
  color: var(--muted);
  font-family: 'JetBrains Mono', monospace;
  margin-bottom: .6rem;
}

[data-testid="stTextInput"] input {
  background: var(--surface) !important;
  border: 1px solid var(--border2) !important;
  border-radius: 12px !important;
  color: var(--text) !important;
  font-family: 'Outfit', sans-serif !important;
  font-size: 1rem !important;
  font-weight: 500 !important;
  padding: .9rem 1.25rem !important;
  transition: border-color .25s, box-shadow .25s, background .25s !important;
  caret-color: var(--accent);
}
[data-testid="stTextInput"] input:focus {
  border-color: var(--accent) !important;
  background: var(--surface2) !important;
  box-shadow: 0 0 0 3px rgba(0,245,180,.1), 0 4px 20px rgba(0,0,0,.3) !important;
  outline: none !important;
}
[data-testid="stTextInput"] input::placeholder { color: var(--muted) !important; }
[data-testid="stTextInput"] label {
  color: var(--muted) !important;
  font-family: 'JetBrains Mono', monospace !important;
  font-size: .7rem !important;
  letter-spacing: .12em !important;
  text-transform: uppercase !important;
  margin-bottom: .5rem !important;
}

/* ── Run button ── */
[data-testid="stButton"] > button {
  background: linear-gradient(135deg, #00f5b4 0%, #00c98a 100%) !important;
  color: #050810 !important;
  border: none !important;
  border-radius: 12px !important;
  font-family: 'Outfit', sans-serif !important;
  font-weight: 800 !important;
  font-size: .95rem !important;
  letter-spacing: .02em !important;
  padding: .8rem 2.5rem !important;
  cursor: pointer !important;
  width: 100% !important;
  transition: transform .2s, box-shadow .2s, opacity .2s !important;
  box-shadow: 0 4px 20px rgba(0,245,180,.25), 0 2px 8px rgba(0,0,0,.3) !important;
  position: relative !important;
  overflow: hidden !important;
}
[data-testid="stButton"] > button:hover {
  transform: translateY(-2px) !important;
  box-shadow: 0 8px 32px rgba(0,245,180,.4), 0 4px 16px rgba(0,0,0,.4) !important;
}
[data-testid="stButton"] > button:active {
  transform: translateY(0) !important;
}

/* ── Download buttons ── */
[data-testid="stDownloadButton"] > button {
  background: var(--surface2) !important;
  color: var(--text) !important;
  border: 1px solid var(--border2) !important;
  border-radius: 10px !important;
  font-family: 'Outfit', sans-serif !important;
  font-weight: 600 !important;
  font-size: .85rem !important;
  padding: .65rem 1.5rem !important;
  transition: border-color .2s, background .2s, transform .15s !important;
  width: 100% !important;
}
[data-testid="stDownloadButton"] > button:hover {
  border-color: var(--accent) !important;
  background: var(--accent-dim) !important;
  transform: translateY(-1px) !important;
}

/* ═══════════════════════════════════════
   PIPELINE TRACKER
═══════════════════════════════════════ */
.pipeline-wrap {
  margin: .5rem 0 1rem;
  animation: fadeUp .5s ease both;
}
.pipeline-title {
  font-size: .68rem;
  letter-spacing: .14em;
  text-transform: uppercase;
  color: var(--muted);
  font-family: 'JetBrains Mono', monospace;
  margin-bottom: 1rem;
  text-align: center;
}
.pipeline-track {
  display: flex;
  align-items: stretch;
  gap: 0;
  position: relative;
}
.pipeline-connector {
  flex: 1;
  height: 2px;
  background: var(--border);
  align-self: center;
  margin-top: -2.5rem;
  position: relative;
  overflow: hidden;
}
.pipeline-connector.filled::after {
  content: '';
  position: absolute;
  inset: 0;
  background: linear-gradient(90deg, var(--accent2), var(--accent));
  animation: fillLine .5s ease forwards;
}
@keyframes fillLine { from { width: 0; } to { width: 100%; } }

.step-node {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: .55rem;
  flex: 0 0 auto;
  width: 100px;
}
.step-circle {
  width: 58px; height: 58px;
  border-radius: 50%;
  border: 2px solid var(--border2);
  background: var(--surface);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.35rem;
  position: relative;
  transition: all .4s cubic-bezier(.34,1.56,.64,1);
}
.step-circle::before {
  content: '';
  position: absolute;
  inset: -4px;
  border-radius: 50%;
  border: 2px solid transparent;
  transition: border-color .3s;
}
.step-node.active .step-circle {
  border-color: var(--accent);
  background: rgba(0,245,180,.08);
  box-shadow: 0 0 0 6px rgba(0,245,180,.08), 0 0 24px rgba(0,245,180,.25);
  transform: scale(1.08);
  animation: stepPulse 1.6s ease-in-out infinite;
}
@keyframes stepPulse {
  0%,100% { box-shadow: 0 0 0 6px rgba(0,245,180,.08), 0 0 24px rgba(0,245,180,.2); }
  50%      { box-shadow: 0 0 0 10px rgba(0,245,180,.04), 0 0 40px rgba(0,245,180,.35); }
}
.step-node.done .step-circle {
  border-color: var(--accent2);
  background: rgba(79,141,255,.1);
  box-shadow: 0 0 14px rgba(79,141,255,.2);
}
.step-done-check {
  display: none;
  position: absolute;
  top: -3px; right: -3px;
  width: 18px; height: 18px;
  background: var(--accent2);
  border-radius: 50%;
  font-size: .6rem;
  align-items: center;
  justify-content: center;
  color: #fff;
  font-weight: 700;
}
.step-node.done .step-done-check { display: flex; }

.step-text {
  text-align: center;
}
.step-name {
  font-family: 'Outfit', sans-serif;
  font-size: .78rem;
  font-weight: 700;
  letter-spacing: .04em;
  text-transform: uppercase;
  color: var(--muted);
  transition: color .3s;
}
.step-node.active .step-name { color: var(--accent); }
.step-node.done   .step-name { color: var(--accent2); }
.step-desc {
  font-size: .65rem;
  color: var(--muted2);
  font-family: 'JetBrains Mono', monospace;
  margin-top: .15rem;
}

/* ── Live status ticker ── */
.status-ticker {
  text-align: center;
  margin: 1rem 0 .5rem;
  min-height: 1.4rem;
}
.ticker-inner {
  display: inline-flex;
  align-items: center;
  gap: .5rem;
  background: rgba(0,245,180,.06);
  border: 1px solid rgba(0,245,180,.2);
  border-radius: 999px;
  padding: .3rem 1rem;
  font-family: 'JetBrains Mono', monospace;
  font-size: .72rem;
  color: var(--accent);
  letter-spacing: .05em;
  animation: fadeIn .3s ease;
}
.ticker-dot {
  width: 6px; height: 6px;
  background: var(--accent);
  border-radius: 50%;
  animation: blink .9s ease-in-out infinite;
}
@keyframes blink { 0%,100%{opacity:1;} 50%{opacity:.2;} }

/* ═══════════════════════════════════════
   STATS ROW
═══════════════════════════════════════ */
.stats-row {
  display: grid;
  grid-template-columns: repeat(3,1fr);
  gap: 1rem;
  margin: 1.5rem 0 2rem;
  animation: fadeUp .5s .1s ease both;
}
.stat-card {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 1.25rem 1rem;
  text-align: center;
  position: relative;
  overflow: hidden;
  transition: border-color .3s, transform .2s;
}
.stat-card:hover {
  border-color: var(--border2);
  transform: translateY(-2px);
}
.stat-card::after {
  content: '';
  position: absolute;
  bottom: 0; left: 50%;
  transform: translateX(-50%);
  width: 40%; height: 2px;
  border-radius: 1px;
  background: linear-gradient(90deg, transparent, var(--accent), transparent);
}
.stat-value {
  font-family: 'Outfit', sans-serif;
  font-size: 2rem;
  font-weight: 900;
  background: linear-gradient(135deg, var(--accent), var(--accent2));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  line-height: 1;
  margin-bottom: .4rem;
}
.stat-label {
  font-size: .68rem;
  color: var(--muted);
  letter-spacing: .1em;
  text-transform: uppercase;
  font-family: 'JetBrains Mono', monospace;
}

/* ═══════════════════════════════════════
   TABS
═══════════════════════════════════════ */
[data-testid="stTabs"] {
  animation: fadeUp .5s .15s ease both;
}
[data-testid="stTabs"] > div:first-child {
  border-bottom: 1px solid var(--border) !important;
  gap: .25rem !important;
  background: transparent !important;
}
[data-testid="stTabs"] [role="tab"] {
  font-family: 'Outfit', sans-serif !important;
  font-weight: 700 !important;
  font-size: .78rem !important;
  letter-spacing: .06em !important;
  text-transform: uppercase !important;
  color: var(--muted) !important;
  border-radius: 8px 8px 0 0 !important;
  padding: .6rem 1rem !important;
  transition: color .2s, background .2s !important;
  border: none !important;
}
[data-testid="stTabs"] [role="tab"]:hover {
  color: var(--text) !important;
  background: rgba(255,255,255,.03) !important;
}
[data-testid="stTabs"] [role="tab"][aria-selected="true"] {
  color: var(--accent) !important;
  background: rgba(0,245,180,.07) !important;
  border-bottom: 2px solid var(--accent) !important;
}

/* ═══════════════════════════════════════
   RESULT CARDS
═══════════════════════════════════════ */
.result-card {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  overflow: hidden;
  margin-bottom: 1rem;
  transition: border-color .3s;
  animation: fadeUp .4s ease both;
}
.result-card:hover { border-color: var(--border2); }

.result-card-header {
  display: flex;
  align-items: center;
  gap: .75rem;
  padding: 1rem 1.5rem;
  background: linear-gradient(135deg, rgba(255,255,255,.03) 0%, transparent 100%);
  border-bottom: 1px solid var(--border);
}
.result-card-icon {
  width: 36px; height: 36px;
  border-radius: 10px;
  display: flex; align-items: center; justify-content: center;
  font-size: 1rem;
  flex-shrink: 0;
}
.rc-green  { background: rgba(0,245,180,.12); }
.rc-blue   { background: rgba(79,141,255,.12); }
.rc-purple { background: rgba(176,106,255,.12); }
.rc-orange { background: rgba(255,180,80,.12); }

.result-card-title {
  font-family: 'Outfit', sans-serif;
  font-weight: 700;
  font-size: .88rem;
  letter-spacing: .04em;
  text-transform: uppercase;
  color: var(--text);
}
.result-card-agent {
  margin-left: auto;
  font-size: .62rem;
  font-family: 'JetBrains Mono', monospace;
  letter-spacing: .08em;
  text-transform: uppercase;
  padding: .2rem .65rem;
  border-radius: 999px;
  border: 1px solid var(--border2);
  color: var(--muted);
}

.result-card-body {
  padding: 1.5rem;
  font-size: .85rem;
  line-height: 1.85;
  color: #9badc8;
  white-space: pre-wrap;
  word-break: break-word;
  max-height: 420px;
  overflow-y: auto;
  font-family: 'Outfit', sans-serif;
  font-weight: 400;
}

/* ═══════════════════════════════════════
   DIVIDER & MISC
═══════════════════════════════════════ */
.fancy-divider {
  position: relative;
  margin: 2.5rem 0;
  height: 1px;
  background: var(--border);
}
.fancy-divider::before {
  content: '';
  position: absolute;
  left: 50%; top: 50%;
  transform: translate(-50%,-50%);
  width: 120px; height: 1px;
  background: linear-gradient(90deg, transparent, var(--accent), transparent);
}

.section-label {
  font-size: .65rem;
  letter-spacing: .18em;
  text-transform: uppercase;
  color: var(--muted);
  font-family: 'JetBrains Mono', monospace;
  margin-bottom: 1rem;
  display: flex;
  align-items: center;
  gap: .6rem;
}
.section-label::after {
  content: '';
  flex: 1;
  height: 1px;
  background: var(--border);
}

.error-box {
  background: rgba(255,95,95,.07);
  border: 1px solid rgba(255,95,95,.3);
  border-radius: var(--radius);
  padding: 1rem 1.4rem;
  color: #ff9e9e;
  font-size: .85rem;
  font-family: 'JetBrains Mono', monospace;
  display: flex;
  align-items: center;
  gap: .6rem;
}

/* ── Keyframes ── */
@keyframes fadeUp   { from { opacity:0; transform:translateY(18px);  } to { opacity:1; transform:none; } }
@keyframes fadeDown { from { opacity:0; transform:translateY(-12px); } to { opacity:1; transform:none; } }
@keyframes fadeIn   { from { opacity:0; }                               to { opacity:1; } }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  SESSION STATE
# ─────────────────────────────────────────────
for k, v in [("result", None), ("elapsed", None), ("ran_once", False), ("last_topic", "")]:
    if k not in st.session_state:
        st.session_state[k] = v


# ─────────────────────────────────────────────
#  HELPERS
# ─────────────────────────────────────────────
STEPS = [
    ("🔍", "Search",  "web crawl",   ""),
    ("📡", "Reader",  "scrape url",  ""),
    ("✍️",  "Writer",  "draft report",""),
    ("🧠", "Critic",  "qa review",   ""),
]
STATUS_MSGS = [
    "Crawling the web for sources…",
    "Scraping top result for content…",
    "Drafting your research report…",
    "Running quality critique pass…",
]

def word_count(t): return len(t.split()) if t else 0

def render_steps(active: int):
    nodes_html = ""
    for i, (icon, label, desc, _) in enumerate(STEPS):
        is_active = (i == active)
        is_done   = (i < active) or (active == 99)
        node_cls  = "active" if is_active else ("done" if is_done else "")
        nodes_html += f"""
        <div class="step-node {node_cls}">
          <div class="step-circle">
            {icon}
            <div class="step-done-check">✓</div>
          </div>
          <div class="step-text">
            <div class="step-name">{label}</div>
            <div class="step-desc">{desc}</div>
          </div>
        </div>"""
        if i < len(STEPS) - 1:
            filled_cls = "filled" if (is_done and not is_active) else ""
            nodes_html += f'<div class="pipeline-connector {filled_cls}"></div>'

    return f"""
    <div class="pipeline-wrap">
      <div class="pipeline-title">— pipeline execution —</div>
      <div class="pipeline-track">{nodes_html}</div>
    </div>"""

def render_status(step: int):
    if 0 <= step < len(STATUS_MSGS):
        return f"""
        <div class="status-ticker">
          <div class="ticker-inner">
            <div class="ticker-dot"></div>
            {STATUS_MSGS[step]}
          </div>
        </div>"""
    return '<div class="status-ticker"></div>'

def result_card(icon, icon_cls, title, agent, content, color_cls="rc-green"):
    safe = content.replace("<", "&lt;").replace(">", "&gt;")
    return f"""
    <div class="result-card">
      <div class="result-card-header">
        <div class="result-card-icon {color_cls}">{icon}</div>
        <div class="result-card-title">{title}</div>
        <div class="result-card-agent">{agent}</div>
      </div>
      <div class="result-card-body">{safe}</div>
    </div>"""


# ─────────────────────────────────────────────
#  NAVBAR
# ─────────────────────────────────────────────
st.markdown("""
<div class="navbar">
  <div class="nav-logo">
    <div class="nav-logo-dot"></div>
    ResearchMind
  </div>
  <div class="nav-pills">
    <span class="nav-pill">LangGraph</span>
    <span class="nav-pill">Multi-Agent</span>
    <span class="nav-pill green">● Live</span>
  </div>
</div>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  HERO
# ─────────────────────────────────────────────
st.markdown("""
<div class="hero">
  <div class="hero-eyebrow">
    <div class="hero-eyebrow-line"></div>
    AI-powered research pipeline
    <div class="hero-eyebrow-line r"></div>
  </div>
  <div class="hero-title">
    Research at the<br><span class="grad">Speed of Thought</span>
  </div>
  <p class="hero-sub">
    Four specialized agents working in sequence — search, read, write, and critique — to deliver publication-ready research on any topic.
  </p>
</div>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  INPUT
# ─────────────────────────────────────────────
_, mid, _ = st.columns([1, 3, 1])
with mid:
    topic = st.text_input(
        "Research Topic",
        placeholder="e.g.  The future of quantum computing in 2025",
        label_visibility="visible",
    )
    run_btn = st.button("⚡  Launch Research Pipeline", use_container_width=True)


# ─────────────────────────────────────────────
#  PIPELINE EXECUTION
# ─────────────────────────────────────────────
if run_btn:
    if not topic.strip():
        st.markdown('<div class="error-box">⚠️&nbsp; Please enter a research topic first.</div>',
                    unsafe_allow_html=True)
    else:
        st.markdown('<div class="fancy-divider"></div>', unsafe_allow_html=True)

        step_ph   = st.empty()
        status_ph = st.empty()

        current_step = {"val": -1}
        _orig_print  = builtins.print

        def _hook(*args, **kwargs):
            msg = " ".join(str(a) for a in args)
            _orig_print(*args, **kwargs)
            for idx, kw in enumerate(["STEP 1","STEP 2","STEP 3","STEP 4"]):
                if kw in msg:
                    current_step["val"] = idx
                    break
            step_ph.markdown(render_steps(current_step["val"]), unsafe_allow_html=True)
            status_ph.markdown(render_status(current_step["val"]), unsafe_allow_html=True)

        builtins.print = _hook
        start = time.time()

        try:
            result  = run_research_pipeline(topic.strip())
            elapsed = round(time.time() - start, 1)
            st.session_state.update(result=result, elapsed=elapsed,
                                    ran_once=True, last_topic=topic.strip())
        except Exception as exc:
            builtins.print = _orig_print
            st.markdown(f'<div class="error-box">❌&nbsp; Pipeline error: {exc}</div>',
                        unsafe_allow_html=True)
            st.stop()
        finally:
            builtins.print = _orig_print

        step_ph.markdown(render_steps(99), unsafe_allow_html=True)
        status_ph.empty()


# ─────────────────────────────────────────────
#  RESULTS
# ─────────────────────────────────────────────
if st.session_state.ran_once and st.session_state.result:
    res     = st.session_state.result
    elapsed = st.session_state.elapsed
    topic   = st.session_state.last_topic

    st.markdown('<div class="fancy-divider"></div>', unsafe_allow_html=True)

    # ── Stats ──────────────────────────────
    st.markdown('<div class="section-label">Research metrics</div>', unsafe_allow_html=True)
    report_wc  = word_count(res.get("report", ""))
    search_len = len(res.get("search_results", ""))
    scraped_wc = word_count(res.get("scraped_content", ""))
    st.markdown(f"""
    <div class="stats-row">
      <div class="stat-card">
        <div class="stat-value">{elapsed}s</div>
        <div class="stat-label">Total runtime</div>
      </div>
      <div class="stat-card">
        <div class="stat-value">{report_wc:,}</div>
        <div class="stat-label">Report words</div>
      </div>
      <div class="stat-card">
        <div class="stat-value">{scraped_wc:,}</div>
        <div class="stat-label">Scraped words</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Tabs ───────────────────────────────
    st.markdown('<div class="section-label">Agent outputs</div>', unsafe_allow_html=True)
    t1, t2, t3, t4 = st.tabs([
        "📋  Full Report",
        "🔍  Search Results",
        "📄  Scraped Content",
        "🧠  Critic Feedback",
    ])

    with t1:
        st.markdown(result_card("📋","rc-green","Final Report","Writer Agent",
                                res.get("report","No report generated.")), unsafe_allow_html=True)
    with t2:
        st.markdown(result_card("🔍","rc-blue","Search Results","Search Agent",
                                res.get("search_results","No search results."), "rc-blue"), unsafe_allow_html=True)
    with t3:
        st.markdown(result_card("📄","rc-purple","Scraped Content","Reader Agent",
                                res.get("scraped_content","No content scraped."), "rc-purple"), unsafe_allow_html=True)
    with t4:
        st.markdown(result_card("🧠","rc-orange","Critic Feedback","Critic Agent",
                                res.get("feedback","No feedback generated."), "rc-orange"), unsafe_allow_html=True)

    # ── Downloads ──────────────────────────
    st.markdown('<div class="fancy-divider"></div>', unsafe_allow_html=True)
    st.markdown('<div class="section-label">Export results</div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    slug = topic[:30].replace(" ","_")
    with c1:
        st.download_button(
            "⬇️  Download Report  (.txt)",
            data=res.get("report",""),
            file_name=f"report_{slug}.txt",
            mime="text/plain",
            use_container_width=True,
        )
    with c2:
        full = (
            f"TOPIC: {topic}\n\n{'='*60}\nSEARCH RESULTS\n{'='*60}\n"
            f"{res.get('search_results','')}\n\n{'='*60}\nSCRAPED CONTENT\n{'='*60}\n"
            f"{res.get('scraped_content','')}\n\n{'='*60}\nFINAL REPORT\n{'='*60}\n"
            f"{res.get('report','')}\n\n{'='*60}\nCRITIC FEEDBACK\n{'='*60}\n"
            f"{res.get('feedback','')}"
        )
        st.download_button(
            "⬇️  Download Full Pipeline Output  (.txt)",
            data=full,
            file_name=f"full_research_{slug}.txt",
            mime="text/plain",
            use_container_width=True,
        )