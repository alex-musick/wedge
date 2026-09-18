import sys
from pathlib import Path

source_path = Path(__file__).resolve()
source_dir = source_path.parent
sys.path.insert(0, f"{source_dir}/tools")

import httpx
import tool
import asyncio
import threading
import requests
import settings
import tool_safety_wrapper
import compact
from colorama import Fore, Back, Style # pyright: ignore[reportMissingModuleSource]
from time import sleep

# ====== Init Global Values / Constants / Tools ======= #

loop = asyncio.new_event_loop()
threading.Thread(target=loop.run_forever, daemon=True).start()

settings = settings.settings()
model_name = settings.default_model
tools = tool.tools
model_url = settings.base_url + "/v1/chat/completions"
used_ctx = 0
total_ctx = 0

with open(f"{source_dir}/prompts/main.md", "r") as prompt:
    system_prompt = prompt.read()

def getTotalContext():
    global settings
    global model_name
    # This is specific to llama-swap. Will always fail safely with warning if using an incompatible proxy
    upstream_props_url = f"{settings.base_url}/upstream/{model_name}/props"
    try:
        response = requests.get(upstream_props_url)
        response.raise_for_status()
    except:
        return -1

    data = response.json()
    return data["default_generation_settings"]["n_ctx"]

def change_model(new_model_name):
    global model_name
    global used_ctx
    global total_ctx
    global settings

    model_name = new_model_name

    total_ctx = getTotalContext()
    if total_ctx == -1:
        print("WARNING: Failed to get ctx size. Invalid model ID?")
        total_ctx = 999999999

    return

headers = {
    "Content-Type": "application/json"
}

# ====== Set up working data and functions ====== #

messages = []
def init_messages():
    global messages
    messages = [
        {
            "role": "system",
            "content": system_prompt
        }
    ]

    agents = ""
    try:
        with open("AGENTS.md", "r") as file:
            agents = file.read()
            agents = "The following instructions are specific to this repository and provided by the AGENTS.md file. Keep them in mind while you work on this repository.\n" + agents
    except:
        pass

    if agents != "":
        messages.append(
            {
                "role": "user",
                "content": agents
            }
        )

    return
init_messages()

def build_payload():
    global model_name
    global messages
    tool_schemas = []

    for tool in tools.values():
        tool_schemas.append(tool.get_schema())

    payload = {
        "model": model_name,
        "messages": messages,
        "tools": tool_schemas
    }

    return payload

async def send_prompt(prompt, tool_call_id="", role_override=""):
    global used_ctx
    global messages
    global headers

    role = "user"
    if tool_call_id != "":
        role = "tool"

    if role_override != "":
        role = role_override

    if role == "tool":
        messages.append(
            {
                "role": role,
                "tool_call_id": tool_call_id,
                "content": prompt
            }
        )
    else:
        messages.append(
            {
                "role": role,
                "content": prompt
            }
        )

    payload = build_payload()
    # print(payload)
    try:
        client = httpx.AsyncClient(timeout=None)
        response = await client.post(model_url, json=payload, headers=headers)
        # response = requests.post(model_url, json=payload, headers=headers)
    except requests.exceptions.ConnectionError:
        print(Fore.RED + "Connection Error" + Style.RESET_ALL)
        return -1
    except asyncio.CancelledError:
        raise

    if response.status_code == 200:
        data = response.json()
        messages.append(data["choices"][0]["message"])
        used_ctx = data["usage"]["total_tokens"]

    return response

def await_throb(future, text="Working."):
    print(text, end="", flush=True)

    while not future.done():
        sleep(1)
        print(".", end="", flush=True)

    print(".")
    print()

    return future.result()

def enter_work_loop(prompt, safety_mode):
    global messages
    global total_ctx
    global used_ctx

    if (total_ctx - used_ctx) <= settings.get_compact_threshold(total_ctx):
        compact.compact()

    model_response_future = asyncio.run_coroutine_threadsafe(send_prompt(prompt), loop)
    try:
        model_response_raw = await_throb(model_response_future)
    except KeyboardInterrupt:
        model_response_future.cancel()
        print()
        return

    first_loop = True
    done = False

    while not done:
        if not first_loop:
            print(Fore.LIGHTBLUE_EX + f"Context: {used_ctx} / {total_ctx}" + Style.RESET_ALL)
        first_loop = False

        if (total_ctx - used_ctx) <= settings.get_compact_threshold(total_ctx):
            compact.compact()

        if model_response_raw == -1:
            return

        if model_response_raw.status_code != 200:
            print(Fore.RED + f"UPSTREAM ERROR {model_response_raw.status_code}" + Style.RESET_ALL)
            done = True
            continue

        model_response = model_response_raw.json()
        finish_reason = model_response["choices"][0]["finish_reason"]
        message = model_response["choices"][0]["message"]
        messages.append(message)

        if message["content"] != "":
            print()
            print(message["content"])
            print()
        
        if finish_reason != "tool_calls":
            done = True
            continue
        else:
            tool_output = tool_safety_wrapper.safe_tool_call(message, safety_mode)
            model_response_future = asyncio.run_coroutine_threadsafe(send_prompt(tool_output, message["tool_calls"][0]["id"]), loop)
            try:
                model_response_raw = await_throb(model_response_future)
            except KeyboardInterrupt:
                model_response_future.cancel()
                print()
                return
            continue

    return