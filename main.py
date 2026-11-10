import argparse
import json
import os
import sys

from dotenv import load_dotenv
from openai import OpenAI
from openai.types.chat import ChatCompletion, ChatCompletionMessageParam

from call_function import available_functions, call_function
from config import *
from prompts import system_prompt


def main():

    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    load_dotenv()
    api_key = os.environ.get("OPENROUTER_API_KEY")
    if api_key is None:
        raise RuntimeError("api key wasn't found")

    messages: list[ChatCompletionMessageParam] = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": args.user_prompt},
    ]

    client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=api_key)

    for i in range(MAX_MESSAGES):
        response: ChatCompletion = client.chat.completions.create(
            model="openrouter/free",
            messages=messages,
            temperature=0.0,
            tools=available_functions,
        )

        if response.usage is None:
            raise RuntimeError("api request likely failed")

        message = response.choices[0].message
        messages.append(message)

        if args.verbose:
            print(f"User prompt: {args.user_prompt}")
            print(f"Prompt tokens: {response.usage.prompt_tokens}")
            print(f"Response tokens: {response.usage.completion_tokens}")

        if message.tool_calls is not None:
            for tool_call in message.tool_calls:
                function_args = json.loads(tool_call.function.arguments)
                function_name = tool_call.function.name
                result_message = call_function(tool_call, args.verbose)
                messages.append(result_message)
                if result_message["content"] is None:
                    raise Exception("Nothing returned from a tool call")
                if args.verbose:
                    print(f"-> {result_message['content']}")
        else:
            print("Response:")
            print(message.content)
            break
        if i == MAX_MESSAGES - 1:
            print("Error: Maximum number of messages used")
            sys.exit(1)


if __name__ == "__main__":
    main()
