import os
import argparse
from google import genai
from google.genai import types
from dotenv import load_dotenv
from call_function import available_functions

system_prompt = system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

if api_key == None:
    raise RuntimeError("api_key not found")

client = genai.Client(api_key=api_key)

parser = argparse.ArgumentParser(description="Chatbot")
parser.add_argument("user_prompt", type=str, help="User prompt")
parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
args = parser.parse_args()
messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]

#    welcome = client.models.generate_content(model='gemini-2.5-flash-image', contents="In a short 2-4 sentences welcome me to the terminal and introduce yourself as Jarvis my AI assistant. Make sure that it's witty too.")
#    if welcome.usage_metadata == None:
#        raise RuntimeError("No metadata found. Check if API key is present")
#    print(welcome.text)

request = client.models.generate_content(model='gemini-2.5-flash', contents=messages, config=types.GenerateContentConfig(tools=[available_functions], system_instruction=system_prompt))
if request.usage_metadata == None:
    raise RuntimeError("No metadata found. Check if API key is present")
if args.verbose:
    print(f"User prompt: {args.user_prompt}")
    print(f"Prompt tokens: {request.usage_metadata.prompt_token_count}")
    print(f"Response tokens: {request.usage_metadata.candidates_token_count}")
if request.function_calls is None:
    print(request.text)
else: 
    for function_call in request.function_calls:
        print(f"Calling function: {function_call.name}({function_call.args})")

def main():
    pass


if __name__ == "__main__":
    main()
