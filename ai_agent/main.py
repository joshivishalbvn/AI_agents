from groq import Groq
from dotenv import load_dotenv
load_dotenv()

client = Groq()

response = client.chat.completions.create(
    model="llama-3.1-8b-instant",
    messages=[
        {"role": "user", "content": "Hey, I am vishal joshi, nice to meet you"}
    ],
)

print("\033[38;2;40;154;232mresponse:\033[0m",response.choices[0].message.content)
