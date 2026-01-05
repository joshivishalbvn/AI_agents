#chain of thought prompting

import os
from dotenv import load_dotenv
from openai import OpenAI
import json

import requests
load_dotenv()

def get_weather(city:str):
    url = f"https://wttr.in/{city.lower()}?format=%C+%t"
    res = requests.get(url)

    if res.status_code==200:
        return f"The weather of {city} is {res.text}"
    
    return "Something went wrong..."

def run_command(cmd:str):
    result = os.system(cmd)
    return result

available_tools={
    "get_weather":get_weather,
    "run_command":run_command
}

client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

SYSTEM_PROMPT = """
    You're an expert ai assistant in resolving user queries using chain of thought.
    You work on START, PLAN and OUTPUT steps.
    You need to first PLAN what needs to be done. The PLAN can be multiple steps.
    Once you think enough PLAN has be done, finally you can give OUTPUT.
    You can also call a tool if required from list of available tools.
    For every tool call wait for the observe step which is the output of the called tool.

    Rules:
    - Strictly follow the given JSON output format.
    - Only run one STEP at a time.
    - The sequence of steps is START (where user gives an input), PLAN (That can be multiple times) and finally OUTPUT (which is going to be display to the user).

    Output JSON Format:
    {"step": "START" | "PLAN" | "OUTPUT" | "TOOL", "content":"string", "tool":"string","input":"string"}

    Available Tools:
    - get_weather(city: str): Takes city name as an input string and returns the weather info about the city
    - run_command(cmd: str): Takes a system linux command as string and executes on user's system and returns the output from that command.

    Example 1:
    START: Hey, Can you solve 2+3*5/10?
    PLAN: {"step":"PLAN","content":"Seems like user is interested in maths problem"} 
    PLAN: {"step":"PLAN","content":"Looking at the problem, we should solve this using BODOMAS method"} 
    PLAN: {"step":"PLAN","content":"Yes, then BODMAS is correct thing to be done here"} 
    PLAN: {"step":"PLAN","content":"First, we must multiple 3*5 which is 15"} 
    PLAN: {"step":"PLAN","content":"Now, the new equation is 2+15/10"} 
    PLAN: {"step":"PLAN","content":"We must perform the divide that is 15/10 = 1.5"} 
    PLAN: {"step":"PLAN","content":"Now, the new equation is 2+1.5"} 
    PLAN: {"step":"PLAN","content":"Finally, lets perform add 2+1.5 = 3.5"} 
    PLAN: {"step":"PLAN","content":"Great , we have solved and finally left with 3.5 as ans "} 
    OUTPUT: {"step":"OUTPUT","content":"3.5"} 

    Example 2:
    START: Hey, What is the weather of delhi?
    PLAN: {"step":"PLAN","content":"Seems like user is interested in getting weather of delhi in india"} 
    PLAN: {"step":"PLAN","content":"Lets see if we have any available tool from list of available list of tools"} 
    PLAN: {"step":"PLAN","content":"Great, we have get_weather tool available for this query"} 
    PLAN: {"step":"PLAN","content":"I need to call get_weather tool for delhi as input for city"} 
    PLAN: {"step":"TOOL","tool":"get_weather","input":"delhi"} 
    PLAN: {"step":"OBSERVE","tool":"get_weather","output":"The temperature of delhi is cloudy with 20 C"} 
    PLAN: {"step":"PLAN","content":"Great, i got the weather info about the delhi"} 
    OUTPUT: {"step":"OUTPUT","content":"The current weather of delhi is 20 C with some cloudy sky."} 

"""

print("\n\n\n")
message_history = [
    {"role":"system","content":SYSTEM_PROMPT},
]




while True:
    user_query = input("Enter Your Query : ")
    message_history.append({"role":"user","content":user_query})

    while True:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            response_format={"type":"json_object"},
            messages=message_history 
        )

        raw_result = response.choices[0].message.content
        message_history.append({"role":"assistant","content":raw_result})

        parsed_result = json.loads(raw_result)

        if parsed_result.get("step") == "START":
            print("Starting LLM Loop",parsed_result.get("content"))
            continue

        if parsed_result.get("step") == "PLAN":
            print("Thinking Process",parsed_result.get("content"))
            continue

        if parsed_result.get("step") == "OUTPUT":
            print("Answer ==",parsed_result.get("content"))
            break

        if parsed_result.get("step") == "TOOL":
            tool_to_call = parsed_result.get("tool")
            tool_input = parsed_result.get("input")
            tool_response = available_tools[tool_to_call](tool_input)

            print(f"======: {tool_to_call} ({tool_input}) : {tool_response}")

            message_history.append({"role":"developer","content":json.dumps(
                {"step":"OBSERVE", "tool":tool_to_call, "input":tool_input,"output":tool_response}
            )})

print('\033[38;2;231;54;189m'+'message_history: ' + '\033[38;2;60;53;30m', message_history, '\033[0m')