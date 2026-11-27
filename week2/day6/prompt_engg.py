import os
import time
from pathlib import Path
from dotenv import load_dotenv
from groq import Groq
from pydantic import BaseModel, Field

load_dotenv()
my_api_key=os.getenv("GROQ_API_KEY")

if not my_api_key:
    raise ValueError("API key kaha hai bhai")

client=Groq(api_key=my_api_key)
model = "openai/gpt-oss-120b"

def llm_ans(prompt):
    message = {
        "role" : "user",
        "content" : prompt
    }

    messages = [message]
    response = client.chat.completions.create(model = model, messages = messages) 
    ans = response.choices[0].message.content
    return ans

bad_prompt="""
# Role : 
You are a support assistant at a mobile/laptop company

# Task :
you have to categorize the issue in a category 

# Constraint : 
you have to classify the issue on one of these 3 categories : Billing, Return, Technical

# Output Format
you have to answer just in one word. and that one word should me one of the categories given to you in constraints

#Example:
for instance if a customer wants a refund the categorty is "return"  

# Fallback : 
if the issue is unrelated to any of the categories from the constraints, then the category is others

This is a user complaint:
my laptop isn't working


"""

print(llm_ans(bad_prompt))