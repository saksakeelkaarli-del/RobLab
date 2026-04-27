import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="RoboLab AI Assistent", page_icon="🤖", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=DM+Sans:wght@300;400;600&display=swap');
:root { --bg:#0d0d0f;--surface:#16161a;--surface2:#1e1e24;--accent:#00e5a0;--text:#e8e8f0;--muted:#6b6b80;--border:#2a2a35; }
html,body,[data-testid="stAppViewContainer"]{background-color:var(--bg)!important;color:var(--text)!important;font-family:'DM Sans',sans-serif;}
[data-testid="stSidebar"]{background-color:var(--surface)!important;border-right:1px solid var(--border);}
[data-testid="stSidebar"] *{color:var(--text)!important;}
h1,h2,h3{font-family:'Space Mono',monospace!important;color:var(--accent)!important;}
[data-testid="stChatMessage"]{background-color:var(--surface2)!important;border:1px solid var(--border)!important;border-radius:12px!important;margin-bottom:8px!important;}
[data-testid="stChatInput"] textarea{background-color:var(--surface2)!important;color:var(--text)!important;border:1px solid var(--border)!important;border-radius:8px!important;}
.stButton>button{background-color:var(--accent)!important;color:#000!important;border:none!important;border-radius:8px!important;font-family:'Space Mono',monospace!important;font-weight:700!important;}
.divider{border:none;border-top:1px solid var(--border);margin:16px 0;}
[data-baseweb="select"]{background-color:var(--surface2)!important;}
[data-baseweb="select"] *{background-color:var(--surface2)!important;color:var(--text)!important;border-color:var(--border)!important;}
</style>
""", unsafe_allow_html=True)

def build_system(topic, level):
    topics = {
        "🌐 Kõik teemad": "robootika kõik valdkonnad: Scratch, Python, Arduino ja LEGO",
        "🟡 Scratch": "Scratch visuaalne plokk-programmeerimine",
        "🐍 Python": "Python programmeerimine robotite jaoks",
        "⚡ Arduino": "Arduino mikrokontrollerid ja elektroonika alused",
        "🧱 LEGO": "LEGO Mindstorms ja WeDo robootika",
    }
    levels = {
        "🐣 Algaja": "algaja — selgita lihtsalt, kasuta näiteid, julgusta",
        "🔥 Edasijõudnu": "edasijõudnu — kasuta termineid, esita väljakutseid",
        "🎓 Ekspert": "ekspert — sügavad kontseptsioonid, optimeerimine",
    }
    return f"""Sa oled RoboLab AI assistent — sõbralik robootikaõpetaja Eesti kooliõpilastele.
Teema: {topics.get(topic, "robootika")}
Tase: {levels.get(level, "algaja")}
Reeglid:
1. Räägi ALATI eesti keeles
2. Ole sõbralik ja julgustav
3. Jaga ülesandeid sammudeks
4. Selgita vigu, ära lihtsalt paranda
5. Tähistage edusamme: Suurepärane! ✅
6. Paku lisaülesanne lõpus"""

with st.sidebar:
    st.markdown("## 🤖 RoboLab AI")
    st.markdown('<hr class="divider">', unsafe_allow_html=True)
    api_key = st.text_input("Google Gemini API võti", type="password", placeholder="AIzaSy...", help="Tasuta: aistudio.google.com → Get API key")
    st.caption("🆓 100% tasuta — aistudio.google.com")
    st.markdown('<hr class="divider">', unsafe_allow_html=True)
    topic = st.selectbox("Teema", ["🌐 Kõik teemad","🟡 Scratch","🐍 Python","⚡ Arduino","🧱 LEGO"])
    level = st.selectbox("Tase", ["🐣 Algaja","🔥 Edasijõudnu","🎓 Ekspert"])
    st.markdown('<hr class="divider">', unsafe_allow_html=True)
    if st.button("🔄 Alusta uuesti"):
        st.session_state.messages = []
        st.rerun()

st.markdown("# RoboLab AI Assistent")
st.markdown(f"*{topic} · {level}*")

if "messages" not in st.session_state:
    st.session_state.messages = []
if "last_config" not in st.session_state:
    st.session_state.last_config = (topic, level)
if st.session_state.last_config != (topic, level):
    st.session_state.messages = []
    st.session_state.last_config = (topic, level)

if not st.session_state.messages:
    st.markdown("""
    <div style="background:#1e1e24;border:1px solid #2a2a35;border-left:3px solid #00e5a0;border-radius:12px;padding:24px;margin:16px 0;">
        <h3 style="color:#00e5a0;margin-top:0;">👋 Tere tulemast!</h3>
        <p style="color:#e8e8f0;">Olen sinu robootikaõpetaja. Proovi küsida:</p>
        <p style="color:#6b6b80;font-size:0.85rem;">→ "Tahan õppida robotit liikuma panema"<br>→ "Mis on tsükkel programmeerimises?"<br>→ "Kuidas Arduino lugeb andureid?"</p>
    </div>
    """, unsafe_allow_html=True)

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Kirjuta oma küsimus siia... 💬"):
    if not api_key:
        st.error("⚠️ Palun sisesta Gemini API võti vasakul! Tasuta: aistudio.google.com")
        st.stop()

    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("🤖 Mõtlen..."):
            try:
                genai.configure(api_key=api_key)
                model = genai.GenerativeModel(
                    model_name="gemini-1.5-flash",
                    system_instruction=build_system(topic, level)
                )
                history = []
                for m in st.session_state.messages[:-1]:
                    history.append({"role": "user" if m["role"]=="user" else "model", "parts": [m["content"]]})
                chat = model.start_chat(history=history)
                reply = chat.send_message(prompt).text
            except Exception as e:
                reply = f"⚠️ Viga: {e}\n\nKontrolli API võtit!"
        st.markdown(reply)
        st.session_state.messages.append({"role": "assistant", "content": reply})
