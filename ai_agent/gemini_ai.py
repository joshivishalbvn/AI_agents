from dotenv import load_dotenv
from google import genai
import os

load_dotenv()

client = genai.Client(
    api_key = os.getenv("GEMINI_API_KEY")
)

response = client.models.generate_content(
    model = "gemini-2.5-flash",
    contents = "hi"
)
print('\033[38;2;117;224;95m'+'response: ' + '\033[38;2;90;85;218m', response.text, '\033[0m')