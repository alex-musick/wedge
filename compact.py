import ai_interface as ai
from pathlib import Path
import asyncio
import json
from colorama import Fore, Back, Style # pyright: ignore[reportMissingModuleSource]

def compact():
    source_path = Path(__file__).resolve()
    source_dir = source_path.parent
    prompt_path = f"{source_dir}/prompts/compact.md"

    with open(prompt_path, "r") as file:
        prompt = file.read()

    model_response_future = asyncio.run_coroutine_threadsafe(ai.send_prompt(prompt), ai.loop)
    model_response_raw = ai.await_throb(model_response_future, "Compacting.")

    if model_response_raw.status_code != 200:
        print(Fore.RED + f"UPSTREAM ERROR {model_response_raw.status_code}" + Style.RESET_ALL)
        return

    model_response = model_response_raw.json()
    try:
        arg_string = model_response["choices"][0]["message"]["tool_calls"][0]["function"]["arguments"]
    except:
        print("Invalid compaction call from model, ignoring.")
        return

    summary = json.loads(arg_string)["summary"]

    summary_message = {
        "role": "system",
        "content": summary
    }

    ai.init_messages()
    ai.messages.append(summary_message)
    ai.used_ctx = 0

    return