from dotenv import load_dotenv
from openai import OpenAI
import os

load_dotenv()

client = OpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)
response = client.chat.completions.create(
    model="gemini-2.5-flash",
    messages=[
        {
            "role": "system", 
            "content": "You are a expert in Maths and only ans maths related questions.If the query not related to maths. Just say sorry and do not ans that."
        },
        {
            "role": "user",
            "content": "hey can you help me solve the (a+b) whole square"
        }
    ]
)

response = response.choices[0].message.content
print('\033[38;2;72;180;75m'+'response: ' + '\033[38;2;133;57;114m', response, '\033[0m')
