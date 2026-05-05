import streamlit as st
from groq import Groq

# --- Lehe seadistus ---
st.set_page_config(
    page_title="Robo Lab AI Assistent",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- CSS Stiil (hele lilla teema) ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=Syne:wght@700;800&display=swap');

:root {
    --bg: #f3f0ff;
    --surface: #ede9fe;
    --card: #ffffff;
    --border: #d8b4fe;
    --accent1: #7c3aed;
    --accent2: #a855f7;
    --accent3: #c084fc;
    --accent4: #e879f9;
    --text: #3b1f6e;
    --muted: #7c6ba0;
}

html, body, [data-testid="stAppViewContainer"], [data-testid="stMain"] {
    background-color: var(--bg) !important;
    color: var(--text) !important;
    font-family: 'Space Grotesk', sans-serif !important;
}

[data-testid="stSidebar"] {
    background: var(--surface) !important;
    border-right: 1.5px solid var(--border) !important;
}

[data-testid="stChatInput"] textarea {
    background: var(--card) !important;
    color: var(--text) !important;
    border: 1.5px solid var(--border) !important;
    border-radius: 16px !important;
    font-family: 'Space Grotesk', sans-serif !important;
}

[data-testid="stChatInput"] textarea:focus {
    border-color: var(--accent1) !important;
    box-shadow: 0 0 0 3px rgba(124,58,237,0.15) !important;
}

[data-testid="stChatMessage"] {
    background: var(--card) !important;
    border: 1.5px solid var(--border) !important;
    border-radius: 16px !important;
    padding: 16px !important;
    margin-bottom: 8px !important;
    box-shadow: 0 2px 12px rgba(124,58,237,0.07) !important;
}

.stButton > button {
    background: linear-gradient(135deg, #7c3aed, #a855f7) !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-weight: 600 !important;
    padding: 10px 20px !important;
    transition: all 0.2s ease !important;
    box-shadow: 0 4px 14px rgba(124,58,237,0.25) !important;
}

.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 25px rgba(124,58,237,0.4) !important;
}

h1, h2, h3 { font-family: 'Syne', sans-serif !important; color: var(--text) !important; }
</style>
""", unsafe_allow_html=True)

# --- Groq klient ---
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# --- Sessiooni olekud ---
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": (
            "Sa oled Robo Lab'i tark ja sõbralik AI assistent, mis aitab õpilastel ja õpetajatel. "
            "Oled ekspert robootika, matemaatika, loodusteaduste, programmeerimise ja füüsika alal. "
            "Vasta selgelt, struktureeritult ja innustavalt. Kasuta emojisid mõõdukalt."
        )}
    ]

if "page" not in st.session_state:
    st.session_state.page = "home"

# ─────────────────────────────────────────────
# AVALEHT
# ─────────────────────────────────────────────
if st.session_state.page == "home":

    # Hero sektsioon
    st.markdown("""
    <div style="text-align:center; padding: 60px 20px 30px;">
        <div style="font-size:80px; margin-bottom:12px; filter:drop-shadow(0 4px 16px #a855f766);">🤖</div>
        <h1 style="font-size:3.2rem; background:linear-gradient(135deg,#7c3aed,#a855f7,#e879f9);
                   -webkit-background-clip:text; -webkit-text-fill-color:transparent;
                   background-clip:text; margin-bottom:12px;">
            Robo Lab AI Assistent
        </h1>
        <p style="font-size:1.2rem; color:#7c6ba0; max-width:600px; margin:0 auto 40px;">
            Sinu tark partner robootika, matemaatika ja teaduse maailmas 🚀
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Õppeained
    st.markdown("""
    <h2 style="text-align:center; font-size:1.5rem; margin-bottom:20px;">📚 Vali õppeaine</h2>
    """, unsafe_allow_html=True)

    subjects = [
        {"emoji": "🤖", "name": "Robootika",        "gen": "robootika",        "color": "#7c3aed", "light": "#ede9fe", "desc": "Robotid, andurid, projektid"},
        {"emoji": "💻", "name": "Programmeerimine", "gen": "programmeerimise", "color": "#0ea5e9", "light": "#e0f2fe", "desc": "Python, Scratch, algoritmid"},
        {"emoji": "🔢", "name": "Matemaatika",      "gen": "matemaatika",      "color": "#d97706", "light": "#fef3c7", "desc": "Algebra, geomeetria, statistika"},
        {"emoji": "⚡", "name": "Füüsika",          "gen": "füüsika",          "color": "#dc2626", "light": "#fee2e2", "desc": "Elekter, jõud, energia"},
        {"emoji": "🧪", "name": "Keemia",           "gen": "keemia",           "color": "#059669", "light": "#d1fae5", "desc": "Elemendid, reaktsioonid"},
        {"emoji": "🌱", "name": "Loodusõpetus",     "gen": "loodusõpetuse",    "color": "#16a34a", "light": "#dcfce7", "desc": "Ökosüsteemid, keskkond"},
    ]

    cols = st.columns(3)
    for i, subj in enumerate(subjects):
        with cols[i % 3]:
            st.markdown(f"""
            <div style="background:{subj['light']};
                        border:2px solid {subj['color']}44;
                        border-radius:18px; padding:22px;
                        margin-bottom:16px;
                        box-shadow:0 2px 16px {subj['color']}18;">
                <div style="font-size:2.4rem; margin-bottom:8px;">{subj['emoji']}</div>
                <div style="font-size:1.1rem; font-weight:700; color:{subj['color']}; margin-bottom:4px;">{subj['name']}</div>
                <div style="font-size:0.85rem; color:#6b7280;">{subj['desc']}</div>
            </div>
            """, unsafe_allow_html=True)

            if st.button(f"Küsi {subj['gen']} kohta", key=f"subj_{i}"):
                st.session_state.messages.append({
                    "role": "user",
                    "content": f"Räägi mulle {subj['gen']} kohta – mis on peamised teemad ja kuidas sa saad aidata?"
                })
                st.session_state.page = "chat"
                st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    # Soovitatud küsimused
    st.markdown("""
    <h2 style="text-align:center; font-size:1.5rem; margin-bottom:20px;">💡 Proovi neid küsimusi</h2>
    """, unsafe_allow_html=True)

    suggested = [
        "🤖 Kuidas programmeerida robotit Python'iga?",
        "🔢 Seleta mulle Pythagorase teoreemi",
        "⚡ Mis on elektrivool ja kuidas see töötab?",
        "💻 Kuidas teha oma esimene programm Scratch'is?",
        "🌍 Mis on kliimamuutus ja miks see oluline on?",
        "🧮 Kuidas lahendada ruutvõrrandeid?",
    ]

    cols2 = st.columns(2)
    for i, q in enumerate(suggested):
        with cols2[i % 2]:
            if st.button(q, key=f"q_{i}", use_container_width=True):
                clean_q = q[3:].strip()
                st.session_state.messages.append({"role": "user", "content": clean_q})
                st.session_state.page = "chat"
                st.rerun()

    st.markdown("<br><br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("💬 Alusta vestlust →", use_container_width=True):
            st.session_state.page = "chat"
            st.rerun()

# ─────────────────────────────────────────────
# CHAT LEHT
# ─────────────────────────────────────────────
elif st.session_state.page == "chat":

    col1, col2 = st.columns([5, 1])
    with col1:
        st.markdown("""
        <div style="display:flex; align-items:center; gap:12px; padding:10px 0;">
            <span style="font-size:2.2rem;">🤖</span>
            <div>
                <h1 style="font-size:1.6rem; margin:0;
                           background:linear-gradient(135deg,#7c3aed,#e879f9);
                           -webkit-background-clip:text; -webkit-text-fill-color:transparent;
                           background-clip:text;">Robo Lab AI</h1>
                <p style="margin:0; font-size:0.85rem; color:#7c6ba0;">Alati valmis aitama ✨</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        if st.button("🏠 Avaleht"):
            st.session_state.page = "home"
            st.rerun()

    st.markdown("<hr style='border-color:#d8b4fe; margin:10px 0 20px;'>", unsafe_allow_html=True)

    for msg in st.session_state.messages:
        if msg["role"] == "user":
            with st.chat_message("user", avatar="👤"):
                st.write(msg["content"])
        elif msg["role"] == "assistant":
            with st.chat_message("assistant", avatar="🤖"):
                st.write(msg["content"])

    if len(st.session_state.messages) <= 1:
        st.markdown("<p style='color:#7c6ba0; font-size:0.9rem; margin-bottom:10px;'>💡 Kiirküsimused:</p>", unsafe_allow_html=True)
        quick = ["Mis on Python?", "Seleta robootika alused", "Aita matemaatikas"]
        qcols = st.columns(3)
        for i, qq in enumerate(quick):
            with qcols[i]:
                if st.button(qq, key=f"quick_{i}", use_container_width=True):
                    st.session_state.messages.append({"role": "user", "content": qq})
                    st.rerun()

    if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
        with st.chat_message("assistant", avatar="🤖"):
            with st.spinner("Mõtlen..."):
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=st.session_state.messages,
                    max_tokens=1024,
                    temperature=0.7
                )
                answer = response.choices[0].message.content
                st.write(answer)
                st.session_state.messages.append({"role": "assistant", "content": answer})

    user_input = st.chat_input("Küsi midagi... 💬")
    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        st.rerun()

    with st.sidebar:
        st.markdown("### ⚙️ Seaded")
        if st.button("🗑️ Tühjenda vestlus", use_container_width=True):
            st.session_state.messages = [st.session_state.messages[0]]
            st.rerun()
        if st.button("🏠 Mine avalehele", use_container_width=True):
            st.session_state.page = "home"
            st.rerun()
        st.markdown("---")
        st.markdown("**🤖 Mudel:** LLaMA 3.3 70B")
        st.markdown("**⚡ Powered by:** Groq")
        st.markdown("**💜 Tehtud:** Robo Lab")
