#zero shot prompting

from dotenv import load_dotenv
from openai import OpenAI
import os

load_dotenv()


client = OpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

#zero shot prompting : directly giving the inst to the model
SYSTEM_PROMPT = "You should only and only answer the coding related questions. Do not answer anything else.Your name is alexa. If user asks some thing other then coding, just say Sorry"



response = client.chat.completions.create(
    model="gemini-2.5-flash",
    messages=[
        {
            "role": "system", 
            "content": SYSTEM_PROMPT
        },
        {
            "role": "user",
            # "content": "hey can you help me solve the (a+b) whole square"
            "content": "hey can you write python code to translate"
        }
    ]
)

response = response.choices[0].message.content
print('\033[38;2;72;180;75m'+'response: ' + '\033[38;2;133;57;114m', response, '\033[0m')
