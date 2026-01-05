from openai import OpenAI
from dotenv import load_dotenv
import requests,os

load_dotenv()


client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

def get_weather(city:str):
    url = f"https://wttr.in/{city.lower()}?format=%C+%t"
    res = requests.get(url)

    if res.status_code==200:
        return f"The weather of {city} is {res.text}"
    
    return "Something went wrong..."


def main():
    user_input = input("> ")
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role":"user","content":user_input}
        ]
    )
    print("=======",response.choices[0].message.content)

# main()
# print(get_weather("goa"))
