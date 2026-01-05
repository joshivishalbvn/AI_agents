#chain of thought prompting

import os
from dotenv import load_dotenv
from openai import OpenAI
import json
from pydantic import BaseModel, Field
from typing import Optional
import requests

load_dotenv()

def get_weather(city:str):
    url = f"https://wttr.in/{city.lower()}?format=%C+%t"
    res = requests.get(url)

    if res.status_code==200:
        return f"The weather of {city} is {res.text}"
    
    return "Something went wrong..."

available_tools={
    "get_weather":get_weather
}

class MyOutputFormat(BaseModel):
    step:str = Field(...,description="The ID of step, Example : PLAN,OUTPUT,TOOL")
    content:Optional[str] = Field(None,description="The optional string content for the step")
    tool:Optional[str] = Field(None,description="The ID of the tool to call")
    input:Optional[str] = Field(None,description="The input params for the tool")

#have to replace groq model to handle structured output using pydantic model bcz groq do not supportr this
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
    - get_weather: Takes city name as an input string and returns the weather info about the city

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
        response = client.chat.completions.parse(
            model="llama-3.3-70b-versatile",
            response_format=MyOutputFormat,
            messages=message_history 
        )

        raw_result = response.choices[0].message.content
        message_history.append({"role":"assistant","content":raw_result})

        parsed_result = response.choices[0].message.parsed

        if parsed_result.step == "START":
            print("Starting LLM Loop",parsed_result.content)
            continue

        if parsed_result.step == "PLAN":
            print("Thinking Process",parsed_result.content)
            continue

        if parsed_result.step == "OUTPUT":
            print("Answer ==",parsed_result.content)
            break

        if parsed_result.step == "TOOL":
            tool_to_call = parsed_result.tool
            tool_input = parsed_result.input
            tool_response = available_tools[tool_to_call](tool_input)

            print(f"======: {tool_to_call} ({tool_input}) : {tool_response}")

            message_history.append({"role":"developer","content":json.dumps(
                {"step":"OBSERVE", "tool":tool_to_call, "input":tool_input,"output":tool_response}
            )})
