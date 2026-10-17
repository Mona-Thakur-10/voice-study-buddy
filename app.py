import os
import hashlib
from io import BytesIO
from gtts import gTTS

import requests
import streamlit as st
from dotenv import load_dotenv
from google import genai
from pydub import AudioSegment
from streamlit_mic_recorder import mic_recorder


# Load API keys
load_dotenv()
gemini_key = os.getenv("GEMINI_API_KEY")
gnani_key = os.getenv("GNANI_API_KEY")

st.set_page_config(
    page_title="Voice Study Buddy",
    page_icon="📚"
)

st.title("📚 Voice Study Buddy")
st.write("Your AI-powered study assistant")

if not gemini_key:
    st.error("GEMINI_API_KEY .env file mein nahi mili.")
    st.stop()

if not gnani_key:
    st.error("GNANI_API_KEY .env file mein nahi mili.")
    st.stop()

client = genai.Client(api_key=gemini_key)


# Session state
if "messages" not in st.session_state:
    st.session_state.messages = []

if "last_audio_hash" not in st.session_state:
    st.session_state.last_audio_hash = None


# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# Ask Gemini
def ask_gemini(question):
    question = question.strip()

    if not question:
        return

    st.session_state.messages.append({"role": "user","content": question})
    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                history = [
                    {
                        "role": (
                            "user"
                            if msg["role"] == "user"
                            else "model"
                        ),
                        "parts": [{"text": msg["content"]}]
                    }
                    for msg in st.session_state.messages
                ]

                # Ask for short, student-friendly answers
                response = client.models.generate_content(
                    model="gemini-3.5-flash-lite",
                    contents=history,
                    config={
                        "system_instruction": (
                            "You are Voice Study Buddy, a helpful study "
                            "assistant. Answer in simple English unless "
                            "the user asks for another language. Keep "
                            "answers concise, usually 3 to 5 lines. "
                            "For 'ok' or 'thank you', reply briefly. "
                            "Do not repeat previous questions or answers "
                            "unless the user asks you to."
                        )
                    }
                )
                
                answer = response.text or "Sorry, I couldn't generate an answer."
                st.markdown(answer)

                # Convert answer to speech
                try:
                    tts = gTTS(text=answer, lang="en", slow=False)
                    audio_buffer = BytesIO()
                    tts.write_to_fp(audio_buffer)
                    audio_buffer.seek(0)

                    st.audio(
                        audio_buffer.getvalue(),
                        format="audio/mp3"
                    )

                except Exception as e:
                    st.warning(f"Voice playback unavailable: {e}")

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": answer
                })

            except Exception as e:
                st.error(f"Gemini error: {e}")

# Text question
prompt = st.chat_input("Ask your question in English...")

if prompt:
    ask_gemini(prompt)


# Voice recorder
audio = mic_recorder(
    start_prompt="🎙️ Record Question",
    stop_prompt="⏹️ Stop Recording",
    key="voice_input"
)


# Process each unique recording only once
if audio and audio.get("bytes"):
    audio_hash = hashlib.sha256(audio["bytes"]).hexdigest()

    if audio_hash != st.session_state.last_audio_hash:
        # Mark it as processed before making the API request
        st.session_state.last_audio_hash = audio_hash

        try:
            with st.spinner("Converting speech to text..."):

                # Convert WebM audio to WAV
                audio_segment = AudioSegment.from_file(
                    BytesIO(audio["bytes"]),
                    format="webm"
                )

                wav_buffer = BytesIO()

                audio_segment.export(
                    wav_buffer,
                    format="wav",
                    parameters=["-acodec", "pcm_s16le"]
                )

                wav_bytes = wav_buffer.getvalue()

                if not wav_bytes.startswith(b"RIFF"):
                    st.error("Audio conversion failed. Please record again.")
                    st.stop()

                # Send WAV audio to Gnani
                response = requests.post(
                    "https://api.vachana.ai/stt/v3",
                    headers={
                        "X-API-Key-ID": gnani_key
                    },
                    data={
                        "language_code": "en-IN",
                        "preferred_language": "en-IN",
                        "format": "transcribe",
                        "itn_native_numerals": "true"
                    },
                    files={
                        "audio_file": (
                            "recording.wav",
                            wav_bytes,
                            "audio/wav"
                        )
                    },
                    timeout=60
                )

                response.raise_for_status()
                result = response.json()
                question = result.get("transcript", "").strip()

            if question:
                st.success(f"You said: {question}")
                ask_gemini(question)
            else:
                st.error(f"Transcript not found: {result}")

        except Exception as e:
            st.error(f"Voice error: {e}")


# Clear chat button
if st.button("🗑️ Clear Chat"):
    st.session_state.messages = []
    st.session_state.last_audio_hash = None
    st.rerun()
