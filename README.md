# 🎙️ Voice Study Buddy

An AI-powered study assistant built using Python, Streamlit, Google Gemini, and Gnani AI. It allows users to ask study questions through text or voice and receive AI-generated answers with audio playback.

## ✨ Features

- 💬 Ask questions through text input.
- 🎤 Ask questions using voice input.
- 🤖 Generate answers using Google Gemini.
- 🔊 Listen to answers with text-to-speech.
- 🧹 Clear chat and start a fresh conversation.

## 🛠️ Technologies Used

- Python
- Streamlit
- Google Gemini API
- Gnani AI Speech-to-Text API
- gTTS (Text-to-Speech)
- PyDub

## ⚙️ Installation and Setup

1. Clone the repository:

   ```bash
   git clone https://github.com/Mona-Thakur-10/voice-study-buddy.git
   cd voice-study-buddy
   ```

2. Create and activate a virtual environment:

   ```bash
   python -m venv .venv
   .venv\Scripts\activate
   ```

3. Install the required packages:

   ```bash
   pip install streamlit requests python-dotenv google-genai streamlit-mic-recorder pydub gTTS
   ```

4. Create a `.env` file in the project folder and add your API keys:

   ```env
   GEMINI_API_KEY=your_gemini_api_key
   GNANI_API_KEY=your_gnani_api_key
   ```

   Replace the placeholder values with your own API keys. **Never upload your `.env` file or share your API keys publicly.**

5. Install FFmpeg if it is not already installed and ensure it is available in your system PATH.

6. Run the application:

   ```bash
   streamlit run app.py
   ```

## 🚀 Future Improvements

- Support for multiple languages.
- Study notes and summaries.
- Quiz generation.
- Improved conversation history.

## 👩‍💻 Author

**Mona Thakur**

GitHub: [Mona-Thakur-10](https://github.com/Mona-Thakur-10)

---

*Built as a learning project to explore AI, speech recognition, and conversational applications.*
