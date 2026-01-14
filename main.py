import os
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types

from prompts import system_prompt
from call_functions import available_functions


load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
if api_key == None:
    raise Exception("api_key not found")

parser = argparse.ArgumentParser(description="Chatbot")
parser.add_argument("user_prompt", type=str, help="User prompt")
parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
args = parser.parse_args()
# Now we can access `args.user_prompt`
client = genai.Client(api_key=api_key)
messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]

response = client.models.generate_content(
    model='gemini-2.5-flash',
    contents=messages,
    config=types.GenerateContentConfig(
        tools=[available_functions],
        system_instruction=system_prompt,
        temperature=0
    ),
)
if response.usage_metadata is None:
    raise RuntimeError("no usage metadata")

for function_call in response.function_calls:
    print(f"Calling function: {function_call.name}({function_call.args})")
if args.verbose:
    print("User prompt:", args.user_prompt)
    print("Prompt tokens:", response.usage_metadata.prompt_token_count)
    print("Response tokens:", response.usage_metadata.candidates_token_count)
print(f"Responce: {response.text}")
