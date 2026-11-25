import os
from pathlib import Path
from dotenv import load_dotenv
from groq import Groq

load_dotenv()
my_api_key=os.getenv("GROQ_API_KEY")

if not my_api_key:
    raise ValueError("API key kaha hai bhai")

client=Groq(api_key = my_api_key)

model = "openai/gpt-oss-120b"
role = "user"       



#structure
from pydantic import BaseModel 
class Ticket(BaseModel):
    name : str
    email : str
    issue : str
    item : str
    phone : int

schema = Ticket.model_json_schema()
response_format={
    "type": "json_object"
}

system_prompt = f"""
Extract the personal informationfrom the ticket passedon this schema and give me a json output {schema}
"""

message_system={
    "role" : "system",
    "content" : system_prompt
}

text = "hi there my name is Piyush. i bought an Iphone from you last week which has suddenly stopped working. i live at 34 orleans street. my phone number is 9988776655, Email: piyush@gmail.com"
prompt = f"""
    this is a customer ticket. Please extract their personal information from this.
    {text}
"""

message={
    "role" : role,
    "content" : prompt
}


messages = [message_system, message]
response = client.chat.completions.create(model = model, messages= messages, response_format = response_format)

ans = response.choices[0].message.content
# print(ans)

import json
raw_json = ans  
data_file = json.loads(raw_json)
ticket = Ticket(**data_file)

print(ticket.name)
print(ticket.item)
print(ticket.issue)
print(ticket.phone)
print(ticket.email)