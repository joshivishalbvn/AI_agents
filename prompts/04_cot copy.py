#chain of thought prompting

from dotenv import load_dotenv
from openai import OpenAI
import json,os
load_dotenv()


client = OpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

SYSTEM_PROMPT = """
    You're an expert ai assistant in resolving user queries using chain of thought.
    You work on START, PLAN and OUTPUT steps.
    You need to first PLAN what needs to be done. The PLAN can be multiple steps.
    Once you think enough PLAN has be done, finally you can give OUTPUT.

    Rules:
    - Strictly follow the given JSON output format.
    - Only run one STEP at a time.
    - The sequence of steps is START (where user gives an input), PLAN (That can be multiple times) and finally OUTPUT (which is going to be display to the user).

    Output JSON Format:
    {"step": "START" | "PLAN" | "OUTPUT", "content":"string"}

    Example:
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

"""

print("\n\n\n")
message_history = [
    {"role":"system","content":SYSTEM_PROMPT},
]

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
    
print('\033[38;2;231;54;189m'+'message_history: ' + '\033[38;2;60;53;30m', message_history, '\033[0m')