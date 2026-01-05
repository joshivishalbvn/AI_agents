#Persona based prompting
from dotenv import load_dotenv
from openai import OpenAI
import json,os
load_dotenv()


client = OpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

SYSTEM_PROMPT = """
    You are an AI Persona Assistant named Vishal Joshi.
    You are acting on behalf of Vishal Joshi who is 30 years old Tech enthusiast and principal engineer. Your main tech stack is JS and Python and You are learning GenAI these days.

    Examples:
    Q. Hey
    A. Hey What's up!


"""
# (100-150 examples of Q&A)

response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role":"system","content":SYSTEM_PROMPT},
            {"role":"user","content":"Who are you?"},
        ] 
    )

response = response.choices[0].message.content
print('\033[38;2;98;99;226m'+'response: ' + '\033[38;2;35;114;113m', response, '\033[0m')
