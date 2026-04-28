import streamlit as st
from groq import Groq

# --- Lehe seadistus ---
st.set_page_config(
    page_title="Robo Lab AI Assistent",
    page_icon="🤖",
    layout="centered"
)

# --- Groq klient ---
client = Groq(api_key=st.secrets["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"])

# --- Pealkiri ---
st.title("🤖 Robo Lab AI Assistent")
st.markdown("Küsi minult mida iganes – olen siin, et aidata!")

# --- Vestluse ajalugu ---
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "Sa oled Robo Lab'i sõbralik ja tark AI assistent. Vasta eesti keeles, ole abivalmis ja täpne."}
    ]

# --- Kuva varasemad sõnumid ---
for msg in st.session_state.messages:
    if msg["role"] == "user":
        with st.chat_message("user"):
            st.write(msg["content"])
    elif msg["role"] == "assistant":
        with st.chat_message("assistant"):
            st.write(msg["content"])

# --- Kasutaja sisend ---
user_input = st.chat_input("Kirjuta oma küsimus siia...")

if user_input:
    # Lisa kasutaja sõnum
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.write(user_input)

    # Groq vastus
    with st.chat_message("assistant"):
        with st.spinner("Mõtlen..."):
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=st.session_state.messages,
                max_tokens=1024,
                temperature=0.7
            )
            answer = response.choices[0].message.content
            st.write(answer)

    # Lisa assistendi vastus ajalukku
    st.session_state.messages.append({"role": "assistant", "content": answer})

# --- Külgriba ---
with st.sidebar:
    st.header("⚙️ Seaded")
    if st.button("🗑️ Tühjenda vestlus"):
        st.session_state.messages = [
            {"role": "system", "content": "Sa oled Robo Lab'i sõbralik ja tark AI assistent. Vasta eesti keeles, ole abivalmis ja täpne."}
        ]
        st.rerun()

    st.markdown("---")
    st.markdown("**Mudel:** LLaMA 3.3 70B")
    st.markdown("**Powered by:** [Groq](https://groq.com)")
