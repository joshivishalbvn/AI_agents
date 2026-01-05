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
    PLAN: {"step":"PLAN","content":"Looking at the problem, we should solve this using BODMAS method"} 
    PLAN: {"step":"PLAN","content":"Yes, then BODMAS is correct thing to be done here"} 
    PLAN: {"step":"PLAN","content":"First, we must multiple 3*5 which is 15"} 
    PLAN: {"step":"PLAN","content":"Now, the new equation is 2+15/10"} 
    PLAN: {"step":"PLAN","content":"We must perform the divide that is 15/10 = 1.5"} 
    PLAN: {"step":"PLAN","content":"Now, the new equation is 2+1.5"} 
    PLAN: {"step":"PLAN","content":"Finally, lets perform add 2+1.5 = 3.5"} 
    PLAN: {"step":"PLAN","content":"Great , we have solved and finally left with 3.5 as ans "} 
    OUTPUT: {"step":"OUTPUT","content":"3.5"} 

"""



response = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    response_format={"type":"json_object"},
    messages=[
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user","content": "Hey, write a code to add n numbers in js"},
        {"role": "assistant","content": json.dumps({"step": "PLAN","content": "To add n numbers in JavaScript, we'll first need to get the numbers from the user or define them in an array. Then we can create a function to sum these numbers."})},
        {"role": "assistant","content": json.dumps({"step": "PLAN", "content": "Let's consider using a for loop or the reduce() method in JavaScript to sum the numbers. We will also need to validate the input to ensure it's a number."})},
        {"role": "assistant","content": json.dumps({"step": "OUTPUT", "content": "function sumNumbers(numbers) {\n      return numbers.reduce((a, b) => a + b, 0);\n   }\n   // Example usage:\n   const numbers = [1, 2, 3, 4, 5];\n   const sum = sumNumbers(numbers);\n   console.log(sum);"})},
    ]
)

response = response.choices[0].message.content
print('\033[38;2;72;180;75m'+'response: ' + '\033[38;2;133;57;114m', response, '\033[0m')