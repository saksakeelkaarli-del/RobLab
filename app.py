import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="RoboLab AI Assistent", page_icon="🤖", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700;800&display=swap');
html, body, [data-testid="stAppViewContainer"] {
    background-color: #f0f7ff !important;
    color: #2d3a4a !important;
    font-family: 'Nunito', sans-serif !important;
}
[data-testid="stSidebar"] {
    background-color: #ffffff !important;
    border-right: 2px solid #d0e8ff !important;
}
[data-testid="stSidebar"] * { color: #2d3a4a !important; font-family: 'Nunito', sans-serif !important; }
h1 { color: #1a73e8 !important; font-family: 'Nunito', sans-serif !important; font-weight: 800 !important; font-size: 2rem !important; }
h2, h3 { color: #1a73e8 !important; font-family: 'Nunito', sans-serif !important; font-weight: 700 !important; }
[data-testid="stChatMessage"] {
    background-color: #ffffff !important;
    border: 2px solid #d0e8ff !important;
    border-radius: 16px !important;
    margin-bottom: 10px !important;
}
[data-testid="stChatInput"] textarea {
    background-color: #ffffff !important;
    color: #2d3a4a !important;
    border: 2px solid #90c8ff !important;
    border-radius: 16px !important;
    font-family: 'Nunito', sans-serif !important;
    font-size: 1rem !important;
}
[data-testid="stChatInput"] textarea:focus { border-color: #1a73e8 !important; }
.stButton > button {
    background-color: #1a73e8 !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 12px !important;
    font-family: 'Nunito', sans-serif !important;
    font-weight: 700 !important;
    font-size: 0.95rem !important;
    padding: 8px 20px !important;
}
.stButton > button:hover { background-color: #1558b0 !important; }
.stSelectbox label, .stTextInput label {
    color: #5a7a99 !important;
    font-weight: 700 !important;
    font-size: 0.85rem !important;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}
.divider { border: none; border-top: 2px dashed #d0e8ff; margin: 16px 0; }
[data-baseweb="select"] { background-color: #ffffff !important; border-radius: 12px !important; }
[data-baseweb="select"] * { background-color: #ffffff !important; color: #2d3a4a !important; border-color: #d0e8ff !important; font-family: 'Nunito', sans-serif !important; }
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
        "🐣 Algaja": "algaja — selgita väga lihtsalt, kasuta palju näiteid ja emojisid, julgusta pidevalt",
        "🔥 Edasijõudnu": "edasijõudnu — kasuta termineid, esita väljakutseid",
        "🎓 Ekspert": "ekspert — sügavad kontseptsioonid, optimeerimine",
    }
    return f"""Sa oled RoboLab AI assistent — rõõmsameelne ja sõbralik robootikaõpetaja Eesti kooliõpilastele.
Teema: {topics.get(topic, "robootika")}
Tase: {levels.get(level, "algaja")}
Reeglid:
1. Räägi ALATI eesti keeles
2. Ole väga sõbralik, rõõmsameelne ja julgustav 😊
3. Jaga ülesandeid väikesteks lihtsateks sammudeks
4. Kasuta emojisid et muuta õppimine lõbusamaks 🤖🎉
5. Selgita vigu õrnalt ja positiivselt
6. Tähistage edusamme: Suurepärane töö! 🎉✅
7. Paku alati lisaülesanne lõpus neile kes tahavad rohkem"""

with st.sidebar:
    st.markdown("## 🤖 RoboLab AI")
    st.markdown('<hr class="divider">', unsafe_allow_html=True)
    api_key = st.text_input(
        "Google Gemini API võti",
        type="password",
        placeholder="AIzaSy...",
        help="Tasuta: aistudio.google.com → Get API key"
    )
    st.caption("🆓 100% tasuta — aistudio.google.com")
    st.markdown('<hr class="divider">', unsafe_allow_html=True)
    topic = st.selectbox("Teema", [
        "🌐 Kõik teemad", "🟡 Scratch", "🐍 Python", "⚡ Arduino", "🧱 LEGO"
    ])
    level = st.selectbox("Tase", ["🐣 Algaja", "🔥 Edasijõudnu", "🎓 Ekspert"])
    st.markdown('<hr class="divider">', unsafe_allow_html=True)
    if st.button("🔄 Alusta uuesti"):
        st.session_state.messages = []
        st.rerun()

st.markdown("# 🤖 RoboLab AI Assistent")
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
    <div style="background:#ffffff;border:2px solid #d0e8ff;border-left:5px solid #1a73e8;border-radius:16px;padding:24px;margin:16px 0;">
        <h3 style="color:#1a73e8;margin-top:0;font-family:Nunito,sans-serif;">👋 Tere tulemast RoboLab AI juurde!</h3>
        <p style="color:#2d3a4a;font-family:Nunito,sans-serif;">Olen sinu sõbralik robootikaõpetaja! 🤖 Saan aidata sul õppida:</p>
        <p style="color:#5a7a99;font-size:0.9rem;font-family:Nunito,sans-serif;">
            🟡 Scratch plokk-programmeerimist<br>
            🐍 Pythonit robotite jaoks<br>
            ⚡ Arduino elektroonikut<br>
            🧱 LEGO Mindstormsi
        </p>
        <p style="color:#2d3a4a;font-family:Nunito,sans-serif;margin-bottom:0;">Alusta küsimuse kirjutamisega allpool! 👇</p>
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
                    history.append({
                        "role": "user" if m["role"] == "user" else "model",
                        "parts": [m["content"]]
                    })
                chat = model.start_chat(history=history)
                reply = chat.send_message(prompt).text
            except Exception as e:
                reply = f"⚠️ Viga: {e}\n\nKontrolli API võtit!"
        st.markdown(reply)
        st.session_state.messages.append({"role": "assistant", "content": reply})
