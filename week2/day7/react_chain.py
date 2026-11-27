
import os
import json
import ast
import operator

from dotenv import load_dotenv
from groq import Groq


# --------------------------------
# 1. ENVIRONMENT SETUP
# --------------------------------

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError("GROQ_API_KEY missing!")

client = Groq(api_key=api_key)

model = "openai/gpt-oss-120b"


# --------------------------------
# 2. TOOL FUNCTIONS
# --------------------------------

def get_product_price(product):

    prices = {
        "iphone 17": 1000,
        "iphone 15": 500
    }

    return prices.get(product.lower(), 0)


def calculator(expression):

    operators = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv
    }

    def calculate(node):

        if isinstance(node, ast.Expression):
            return calculate(node.body)

        if isinstance(node, ast.Constant):
            if type(node.value) in (int, float):
                return node.value

        if isinstance(node, ast.BinOp):
            operation = operators.get(type(node.op))

            if operation:
                return operation(
                    calculate(node.left),
                    calculate(node.right)
                )

        if isinstance(node, ast.UnaryOp):
            if isinstance(node.op, ast.USub):
                return -calculate(node.operand)

            if isinstance(node.op, ast.UAdd):
                return calculate(node.operand)

        raise ValueError("Invalid expression")

    try:
        tree = ast.parse(expression, mode="eval")
        return calculate(tree)

    except Exception as e:
        return f"Calculation error: {e}"


# --------------------------------
# 3. TOOL DEFINITIONS
# --------------------------------

tools = [
    {
        "type": "function",
        "function": {
            "name": "get_product_price",
            "description": "Get the price of a product.",
            "parameters": {
                "type": "object",
                "properties": {
                    "product": {
                        "type": "string",
                        "description": "Product name"
                    }
                },
                "required": ["product"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "calculator",
            "description": "Perform mathematical calculations.",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": "Mathematical expression"
                    }
                },
                "required": ["expression"]
            }
        }
    }
]


# --------------------------------
# 4. AVAILABLE FUNCTIONS
# --------------------------------

available_functions = {
    "get_product_price": get_product_price,
    "calculator": calculator
}


# --------------------------------
# 5. SYSTEM PROMPT
# --------------------------------

system_prompt = """
You are a shopping assistant.

You have access to tools for product prices and calculations.

Rules:

1. Use get_product_price to find product prices.
2. Never invent or guess product prices.
3. Use calculator for mathematical calculations.
4. Never calculate using guessed prices.
5. Use actual tool results to answer the user.
6. When all tasks are complete, provide a clear final answer.
7. Do not claim a tool was executed unless it was actually called.
"""


# --------------------------------
# 6. AGENT FUNCTION
# --------------------------------

def run_agent(question):

    messages = [
        {
            "role": "system",
            "content": system_prompt
        },
        {
            "role": "user",
            "content": question
        }
    ]

    max_steps = 10

    for step in range(max_steps):

        print("\n" + "=" * 40)
        print("STEP", step + 1)
        print("=" * 40)

        response = client.chat.completions.create(
            model=model,
            messages=messages,
            tools=tools,
            tool_choice="auto",
            parallel_tool_calls=False,
            temperature=0
        )

        response_message = response.choices[0].message

        # Save assistant response in conversation history
        messages.append(
            response_message.model_dump(exclude_none=True)
        )

        # --------------------------------
        # 7. CHECK TOOL CALLS
        # --------------------------------

        if response_message.tool_calls:

            for tool_call in response_message.tool_calls:

                tool_name = tool_call.function.name

                arguments = json.loads(
                    tool_call.function.arguments
                )

                print("\nTOOL:", tool_name)
                print("ARGUMENTS:", arguments)

                # Execute requested function
                if tool_name in available_functions:

                    function = available_functions[tool_name]

                    result = function(**arguments)

                else:

                    result = "Tool not found"

                print("OBSERVATION:", result)

                # Send tool result back to LLM
                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "name": tool_name,
                    "content": json.dumps(result)
                })

        else:

            # No more tool calls = final response
            final_answer = response_message.content

            print("\nFINAL ANSWER:")
            print(final_answer)

            return final_answer

    print("\nMaximum steps reached.")
    return None


# --------------------------------
# 8. RUN AGENT
# --------------------------------

prompt = """
I have 5000 rupees.

Find the price of an iPhone 17
and 4 iPhone 15.

Calculate how much money I will have left
after buying both.
"""

run_agent(prompt)
