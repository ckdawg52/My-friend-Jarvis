import os
import sys
import argparse
from google import genai
from google.genai import types
from dotenv import load_dotenv
from call_function import available_functions, call_function

system_prompt = system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

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
for i in range(20):
    request = client.models.generate_content(model='gemini-2.5-flash', contents=messages, config=types.GenerateContentConfig(tools=[available_functions], system_instruction=system_prompt))
    if request.usage_metadata == None:
        raise RuntimeError("No metadata found. Check if API key is present")
    if request.candidates:
        for candidate in request.candidates:
            if candidate.content:
                messages.append(candidate.content)
    if args.verbose:
        print(f"User prompt: {args.user_prompt}")
        print(f"Prompt tokens: {request.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {request.usage_metadata.candidates_token_count}")
    if request.function_calls is None:
        print(request.text)
        sys.exit(0)
        break
    else: 
        function_results = []
        for function_call in request.function_calls:
            function_call_result = call_function(function_call, args.verbose)
            if not function_call_result.parts:
                raise Exception("Call function must have returned an empty .parts list")
            if function_call_result.parts[0].function_response is None:
                raise Exception("Function response somehow None")
            if function_call_result.parts[0].function_response.response is None:
                raise Exception("Response is somehow None")
            function_results.append(function_call_result.parts[0])
            if args.verbose:
                print(f"-> {function_call_result.parts[0].function_response.response}")
        messages.append(types.Content(role="user", parts=function_results))

print("Maximum iterations reached without a final response")
sys.exit(1)