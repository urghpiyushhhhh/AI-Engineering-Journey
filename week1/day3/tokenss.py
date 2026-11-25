import os
from pathlib import Path
from dotenv import load_dotenv
from groq import Groq

load_dotenv()
my_api_key=os.getenv("GROQ_API_KEY")

if not my_api_key:
    raise ValueError("API key kaha hai bhai")

client=Groq(api_key = my_api_key)



#####################################################################################################


model = "openai/gpt-oss-20b"
role = "user"
# 3 prompts
prompt1 = "hi!"
prompt2 = "explain time travel in 100 words"
prompt3 = "write an essay on valorant in 1000 words approximately"

prompts = [prompt1, prompt2, prompt3]

for prompt in prompts:

    message={
        "role" : role,
        "content" : prompt
    }

    #message me role and content
    messages = [message]
    # default temp is 0 meaning safe, the range is [0,2]
    response = client.chat.completions.create(model = model, messages= messages, temperature = 0, max_tokens = 200)
    usage = response.usage
    print(f"tokens used: {usage.prompt_tokens + usage.completion_tokens}, input tokens: {usage.prompt_tokens}, output: {usage.completion_tokens}, finish reason: {response.choices[0].finish_reason}")