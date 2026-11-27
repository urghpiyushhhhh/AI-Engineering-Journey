import os
import json
import ast
import operator

from dotenv import load_dotenv
from groq import Groq

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError("GROQ_API_KEY missing!")

client = Groq(api_key=api_key)

model = "openai/gpt-oss-120b"
prompt = "explain how the internet works"
message = {
    "role" : "user",
    "content" : prompt
}

messages = [message]
# response1 = client.chat.completions.create(model=model, messages=messages)
# ans = response1.choices[0].message.content
# print(ans)

stream = client.chat.completions.create(model=model, messages=messages, stream=True)

for chunk in stream:
    content = chunk.choices[0].delta.content
    if content:
        print(content, end="", flush=True)