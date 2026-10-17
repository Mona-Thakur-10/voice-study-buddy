
from dotenv import load_dotenv
from google import genai
import os

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("API key nahi mili. .env file check karo.")
else:
    try:
        client = genai.Client(api_key=api_key)

        response = client.models.generate_content(
            model="gemini-3.5-flash-lite",
            contents="Explain Artificial Intelligence."
        )

        print("\nGemini ka answer:\n")
        print(response.text)

    except Exception as e:
        print("Error:", e)
