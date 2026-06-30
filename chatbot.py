import streamlit as st
from groq import Groq

# 1. Konfigurasi Halaman Utama
st.set_page_config(page_title="SiCerdik AI", page_icon="🌸", layout="centered")

# 2. Injeksi CSS untuk Mengubah Warna Aplikasi (Pink & Biru Muda Pastel)
st.markdown("""
    <style>
    .stApp { background-color: #FFF0F5 !important; }
    h1 { color: #FF69B4 !important; font-family: 'Comic Sans MS', cursive, sans-serif; text-align: center; }
    .stChatInputContainer { border: 2px solid #B0E0E6 !important; border-radius: 15px !important; }
    .stCaption { color: #FF1493 !important; font-weight: bold !important; }
    </style>
""", unsafe_allow_html=True)

st.title("🎀 SiCerdik AI 🎀")

# 3. Konfigurasi API Groq (Menggunakan kunci gsk_ milikmu)
import os
API_KEY = os.environ.get("GROQ_API_KEY")
client = Groq(api_key=API_KEY.strip())

# Instruksi karakter untuk model AI
instruksi_sistem = (
    "Nama Anda adalah SiCerdik AI, sebuah kecerdasan buatan imut yang diciptakan oleh Raisya. "
    "Jawab selalu dalam bahasa Indonesia dengan gaya yang sangat ramah, ceria, menggemaskan, "
    "dan gunakan banyak emoji lucu (seperti ✨, 🌸, 💖, 🐱, 🎀) di setiap jawabanmu."
)

# 4. Inisialisasi Histori Pesan di Session State
if 'messages' not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant", 
            "caption": "🌸 SiCerdik AI", 
            "content": "Halo! Jaa~ Kenalin, namaku SiCerdik AI! ✨ Aku adalah AI lucu yang dibuat oleh Raisya tercinta. 💖 Ada yang bisa aku bantu hari ini? Ketik apa saja yuk! 🐱🎀"
        }
    ]

# Tampilkan semua histori pesan
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.caption(message["caption"])
        st.write(message["content"])

# 5. Area Input Chat User
chat_saya = st.chat_input("Ketik pesan manismu di sini... 🐾")

if chat_saya:
    # Tampilkan & simpan pesan user
    with st.chat_message("user"):
        st.caption("✨ Kamu")
        st.write(chat_saya)
    st.session_state.messages.append({"role": "user", "caption": "✨ Kamu", "content": chat_saya})
    
    # Ambil respon dari Groq API
    with st.spinner("Tunggu sebentar ya, SiCerdik lagi mikir dulu... 🌸✨"):
        try:
            # Menyusun chat history format Groq
            groq_messages = [{"role": "system", "content": instruksi_sistem}]
            for msg in st.session_state.messages:
                # Menyesuaikan role agar sesuai standar API (user/assistant)
                groq_role = "assistant" if msg["role"] == "assistant" or msg["role"] == "ai" else "user"
                groq_messages.append({"role": groq_role, "content": msg["content"]})

            # Panggil model llama-3.1 yang cepat dan pintar
            completion = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=groq_messages,
                temperature=0.8,
                max_tokens=1024,
            )
            jawaban_ai = completion.choices[0].message.content
        except Exception as e:
            jawaban_ai = f"Duh maaf banget, sepertinya ada gangguan koneksi nih... 😢 (Error: {str(e)})"

    # Tampilkan & simpan jawaban AI
    with st.chat_message("assistant"):
        st.caption("🌸 SiCerdik AI")
        st.write(jawaban_ai)
    st.session_state.messages.append({"role": "assistant", "caption": "🌸 SiCerdik AI", "content": jawaban_ai})