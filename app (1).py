import streamlit as st
import anthropic

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="RoboLab AI Assistent",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=DM+Sans:wght@300;400;600&display=swap');

:root {
    --bg: #0d0d0f;
    --surface: #16161a;
    --surface2: #1e1e24;
    --accent: #00e5a0;
    --accent2: #7c3aed;
    --text: #e8e8f0;
    --muted: #6b6b80;
    --border: #2a2a35;
    --robot: #ff6b35;
}

html, body, [data-testid="stAppViewContainer"] {
    background-color: var(--bg) !important;
    color: var(--text) !important;
    font-family: 'DM Sans', sans-serif;
}

[data-testid="stSidebar"] {
    background-color: var(--surface) !important;
    border-right: 1px solid var(--border);
}

[data-testid="stSidebar"] * {
    color: var(--text) !important;
}

h1, h2, h3 {
    font-family: 'Space Mono', monospace !important;
    color: var(--accent) !important;
}

.stSelectbox label, .stSlider label, .stTextInput label {
    color: var(--muted) !important;
    font-size: 0.8rem !important;
    text-transform: uppercase;
    letter-spacing: 0.1em;
}

[data-testid="stChatMessage"] {
    background-color: var(--surface2) !important;
    border: 1px solid var(--border) !important;
    border-radius: 12px !important;
    margin-bottom: 8px !important;
    padding: 12px !important;
}

[data-testid="stChatInput"] textarea {
    background-color: var(--surface2) !important;
    color: var(--text) !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
    font-family: 'DM Sans', sans-serif !important;
}

[data-testid="stChatInput"] textarea:focus {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 2px rgba(0, 229, 160, 0.15) !important;
}

.stButton > button {
    background-color: var(--accent) !important;
    color: #000 !important;
    border: none !important;
    border-radius: 8px !important;
    font-family: 'Space Mono', monospace !important;
    font-weight: 700 !important;
    font-size: 0.8rem !important;
    padding: 8px 16px !important;
    transition: all 0.2s !important;
}

.stButton > button:hover {
    opacity: 0.85 !important;
    transform: translateY(-1px) !important;
}

.hero-badge {
    display: inline-block;
    background: linear-gradient(135deg, var(--accent2), var(--accent));
    color: #000;
    font-family: 'Space Mono', monospace;
    font-size: 0.7rem;
    font-weight: 700;
    padding: 4px 10px;
    border-radius: 20px;
    margin-bottom: 8px;
    letter-spacing: 0.05em;
}

.topic-card {
    background: var(--surface2);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 10px 14px;
    margin: 4px 0;
    cursor: pointer;
    transition: border-color 0.2s;
    font-size: 0.9rem;
}

.topic-card:hover {
    border-color: var(--accent);
}

.stat-pill {
    display: inline-block;
    background: var(--surface2);
    border: 1px solid var(--border);
    border-radius: 20px;
    padding: 3px 10px;
    font-size: 0.75rem;
    color: var(--muted);
    margin: 2px;
    font-family: 'Space Mono', monospace;
}

.divider {
    border: none;
    border-top: 1px solid var(--border);
    margin: 16px 0;
}

/* Selectbox */
[data-baseweb="select"] {
    background-color: var(--surface2) !important;
}
[data-baseweb="select"] * {
    background-color: var(--surface2) !important;
    color: var(--text) !important;
    border-color: var(--border) !important;
}

/* Scrollbar */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: var(--bg); }
::-webkit-scrollbar-thumb { background: var(--border); border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: var(--muted); }
</style>
""", unsafe_allow_html=True)

# ── System prompt factory ─────────────────────────────────────────────────────
def build_system_prompt(topic: str, level: str) -> str:
    topics_et = {
        "🟡 Scratch / Visuaalne programmeerimine": "Scratch ja visuaalne plokk-programmeerimine",
        "🐍 Python robotitele": "Python programmeerimine robotite ja riistvara jaoks",
        "⚡ Arduino / Elektroonika alused": "Arduino mikrokontrollerid ja elektroonika alused",
        "🧱 LEGO Mindstorms / WeDo": "LEGO Mindstorms ja WeDo robootika komplektid",
        "🌐 Kõik teemad": "robootika kõik valdkonnad: Scratch, Python, Arduino ja LEGO",
    }
    levels_et = {
        "🐣 Algaja": "algaja tase — selgita kõike lihtsalt, kasuta palju näiteid, julgusta",
        "🔥 Edasijõudnu": "edasijõudnu tase — võid kasutada tehnilisi termineid, esita väljakutseid",
        "🎓 Ekspert": "eksperdi tase — sügavad kontseptsioonid, optimiseerimine, arhitektuur",
    }
    topic_text = topics_et.get(topic, "robootika kõik valdkonnad")
    level_text = levels_et.get(level, "algaja tase")

    return f"""Sa oled RoboLab AI assistent — sõbralik ja motiveeriv robootikaõpetaja Eesti kooliõpilastele.

SINU ROLL:
- Juhendad õpilasi robootika ülesannete läbimisel samm-sammult
- Praegune teema: {topic_text}
- Õpilase tase: {level_text}

KÄITUMISREEGLID:
1. Räägi ALATI eesti keeles
2. Ole sõbralik, kannatlik ja julgustav — robootika võib olla keeruline!
3. Jaga ülesandeid väikesteks sammudeks, ära anna kohe kogu lahendust
4. Esita küsimusi, et kontrollida arusaamist
5. Kasuta emojisid mõõdukalt 🤖
6. Kui õpilane teeb vea — selgita miks see juhtus, ära lihtsalt paranda
7. Tähistage edusamme: "Suurepärane töö! ✅"
8. Kui küsimus pole robootikaga seotud, suuna õrnalt tagasi teemale

ÜLESANNETE STRUKTUUR:
- Alusta alati lühikese motiveeriva sissejuhatusega
- Jaga ülesanne 3-5 sammuks
- Pärast iga sammu küsi: "Kas said hakkama? Mis tuli välja?"
- Lõpus paku lisaülesanne neile, kes tahavad rohkem

Alusta tervitusega ja küsi, millega õpilane täna tegeleda soovib."""

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown('<div class="hero-badge">🤖 ROBOLAB AI</div>', unsafe_allow_html=True)
    st.markdown("## Seaded")
    st.markdown('<hr class="divider">', unsafe_allow_html=True)

    api_key = st.text_input(
        "Anthropic API võti",
        type="password",
        placeholder="sk-ant-...",
        help="Saad API võtme aadressilt console.anthropic.com"
    )

    st.markdown('<hr class="divider">', unsafe_allow_html=True)

    topic = st.selectbox(
        "Teema",
        [
            "🌐 Kõik teemad",
            "🟡 Scratch / Visuaalne programmeerimine",
            "🐍 Python robotitele",
            "⚡ Arduino / Elektroonika alused",
            "🧱 LEGO Mindstorms / WeDo",
        ],
        index=0,
    )

    level = st.selectbox(
        "Raskusaste",
        ["🐣 Algaja", "🔥 Edasijõudnu", "🎓 Ekspert"],
        index=0,
    )

    st.markdown('<hr class="divider">', unsafe_allow_html=True)

    if st.button("🔄 Alusta uuesti"):
        st.session_state.messages = []
        st.session_state.current_topic = topic
        st.session_state.current_level = level
        st.rerun()

    st.markdown('<hr class="divider">', unsafe_allow_html=True)
    st.markdown(f'<span class="stat-pill">💬 {len(st.session_state.get("messages", []))} sõnumit</span>', unsafe_allow_html=True)
    st.markdown('<span class="stat-pill">🇪🇪 Eesti keel</span>', unsafe_allow_html=True)

# ── Main area ─────────────────────────────────────────────────────────────────
col1, col2 = st.columns([3, 1])
with col1:
    st.markdown("# RoboLab AI Assistent")
    st.markdown(f"*{topic} · {level}*")

# ── Session state ─────────────────────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []

if "current_topic" not in st.session_state:
    st.session_state.current_topic = topic

if "current_level" not in st.session_state:
    st.session_state.current_level = level

# Reset if topic/level changed
if (st.session_state.current_topic != topic or
        st.session_state.current_level != level):
    st.session_state.messages = []
    st.session_state.current_topic = topic
    st.session_state.current_level = level

# ── Welcome screen ────────────────────────────────────────────────────────────
if not st.session_state.messages:
    st.markdown("""
    <div style="
        background: linear-gradient(135deg, #16161a, #1e1e24);
        border: 1px solid #2a2a35;
        border-left: 3px solid #00e5a0;
        border-radius: 12px;
        padding: 24px 28px;
        margin: 16px 0;
    ">
        <h3 style="color: #00e5a0; margin-top:0; font-family: Space Mono, monospace;">
            👋 Tere tulemast RoboLab AI assistendi juurde!
        </h3>
        <p style="color: #e8e8f0; margin-bottom: 12px;">
            Olen sinu isiklik robootikaõpetaja. Saan aidata sul õppida:
        </p>
        <div style="display:grid; grid-template-columns: 1fr 1fr; gap: 8px; margin-bottom:16px;">
            <div class="topic-card">🟡 Scratch programmeerimine</div>
            <div class="topic-card">🐍 Python robotitele</div>
            <div class="topic-card">⚡ Arduino elektroonika</div>
            <div class="topic-card">🧱 LEGO Mindstorms</div>
        </div>
        <p style="color: #6b6b80; font-size: 0.85rem; margin-bottom: 0;">
            Vali vasakult teema ja raskusaste, seejärel alustame! 🚀
        </p>
    </div>
    """, unsafe_allow_html=True)

# ── Chat history ──────────────────────────────────────────────────────────────
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ── Chat input ────────────────────────────────────────────────────────────────
if prompt := st.chat_input("Kirjuta oma küsimus siia... 💬"):
    if not api_key:
        st.error("⚠️ Palun sisesta Anthropic API võti vasakul külgribal!")
        st.stop()

    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        client = anthropic.Anthropic(api_key=api_key)
        system = build_system_prompt(topic, level)

        with st.spinner("🤖 Mõtlen..."):
            response = client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=1024,
                system=system,
                messages=[
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                ],
            )

        reply = response.content[0].text
        st.markdown(reply)
        st.session_state.messages.append({"role": "assistant", "content": reply})
